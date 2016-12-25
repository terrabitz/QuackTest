import subprocess
import shutil
import os
import platform
import zipfile
import gzip
import tarfile
import argparse
import time
import logging

logging.basicConfig(level=logging.DEBUG)


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-l", "--build_linux", action="store_true",
                            help="Build on the remote Linux system specified in the configuration. "
                                 "Primarily used for building on a Windows computer")
    return arg_parser.parse_args()


def zip_dir(path_to_dist_dir, zip_filename_base):
    path_to_files = os.path.sep.join([path_to_dist_dir, zip_filename_base])
    zip_file = zipfile.ZipFile(os.path.sep.join([path_to_dist_dir, zip_filename_base]) + ".zip", mode="w")
    for root, dirs, files in os.walk(path_to_files):
        for file in files:
            zip_file.write(os.path.sep.join([root, file]))


def gzip_dir(path_to_dist_dir, gzip_filename_base):
    print("tarring and gzipping releases")
    path_to_files = os.path.sep.join([path_to_dist_dir, gzip_filename_base])
    tar_file_name = path_to_files + ".tar.gz"
    with tarfile.open(name=tar_file_name, mode="w:gz") as tar_file:
        tar_file.add(path_to_files)


if __name__ == '__main__':
    args = parse_args()

    # Remove build directory if it exists
    path_to_build = os.path.sep.join([os.getcwd(), "build"])
    if os.path.isdir(path_to_build):
        print("Removing build directory")
        shutil.rmtree(path_to_build)

    # Remove dist directory if it exists
    path_to_dist = os.path.sep.join([os.getcwd(), "dist"])
    path_to_platform_dist = path_to_dist

    if platform.system() == "Windows":
        path_to_platform_dist = os.path.sep.join([path_to_dist, "win"])
    elif platform.system() == "Linux":
        path_to_platform_dist = os.path.sep.join([path_to_dist, "linux"])
    if os.path.isdir(path_to_dist):
        print("Removing dist directory: " + path_to_platform_dist)
        shutil.rmtree(path_to_dist)
    time.sleep(1)

    # Build binaries with the pyinstaller utility
    print("Starting local build on " + platform.system())
    path_to_bin = os.path.sep.join([os.getcwd(), "bin"])
    binaries_to_build = ["quacktest.py", "quacktest-gui.py"]
    for binary in binaries_to_build:
        print("Building " + binary + " onedir")
        binary_path = os.path.sep.join([path_to_bin, binary])
        main_args = ["pyinstaller", binary_path, "--log-level", "ERROR"]

        # Add the no-console flag to pyinstaller if the build is on Windows for the gui version
        extra_args = []
        if platform.system() == "Windows" and binary.find("gui") != -1:
            extra_args += ["-w"]

        # Run the pyinstaller commands for both onedir and onefile
        onedir_distpath_args = ["--distpath", path_to_platform_dist]
        onedir_args = main_args + onedir_distpath_args + extra_args
        logging.debug("Onedir build command line: " + " ".join(onedir_args))
        process = subprocess.Popen(onedir_args)
        process.wait()
        print("Building " + binary + " onefile")
        onefile_distpath_args = ["--distpath", os.path.sep.join([path_to_platform_dist, "executables"])]
        onefile_args = main_args + ["-F"] + onefile_distpath_args + extra_args
        logging.debug("Onefile build command line: " + " ".join(onefile_args))
        process = subprocess.Popen(onefile_args)
        process.wait()
        binary_basename = binary.rsplit(".", maxsplit=1)[0]

        if platform.system() == "Windows":
            zip_dir(path_to_dist_dir=path_to_platform_dist, zip_filename_base=binary_basename)
        elif platform.system() == "Linux":
            gzip_dir(path_to_dist_dir=path_to_platform_dist, gzip_filename_base=binary_basename)

    print("Finished")
    # Add dist files to git
    # print("Adding dist files to git")
    # process = subprocess.Popen(["git", "add", "-A", "dist"])
    # process.wait()
