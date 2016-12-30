import subprocess
import shutil
import os
import platform
import tarfile
import argparse
import time
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def build_on_linux(linux_address, linux_username, linux_password):
    process = subprocess.Popen(["fab",
                                "-H", linux_address,
                                "-p", linux_password,
                                "-u", linux_username,
                                "build"])
    process.wait()
    process = subprocess.Popen(["fab",
                                "-H", linux_address,
                                "-p", linux_password,
                                "-u", linux_username,
                                "fetch"])
    process.wait()


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-l", "--build-linux", action="store_true",
                            help="Build on the remote Linux system specified in the configuration. "
                                 "Primarily used for building on a Windows computer")
    return arg_parser.parse_args()


def archive_dir(path_to_dist_dir, zip_filename_base, method):
    path_to_files = os.path.sep.join([path_to_dist_dir, zip_filename_base])
    handle = shutil.make_archive(zip_filename_base, method, root_dir=path_to_files)
    shutil.move(handle, path_to_dist_dir)
    shutil.rmtree(path_to_files)


def zip_dir(path_to_dist_dir, zip_filename_base):
    print("Zipping files")
    archive_dir(path_to_dist_dir, zip_filename_base, method="zip")


def gzip_dir(path_to_dist_dir, gzip_filename_base):
    print("tarring and gzipping releases")
    archive_dir(path_to_dist_dir, gzip_filename_base, method="gztar")


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
        binary_basename = binary.rsplit(".")[0]
        platform_basename = binary_basename
        if platform.system() == "Windows":
            platform_basename += '_win'
        elif platform.system() == "Linux":
            platform_basename += "_linux"
        main_args = ["pyinstaller", binary_path, "--log-level", "ERROR", "-n", platform_basename]

        # Add the no-console flag to pyinstaller if the build is on Windows for the gui version
        extra_args = []
        if platform.system() == "Windows" and binary.find("gui") != -1:
            extra_args += ["-w"]

        # Run the pyinstaller commands for both onedir and onefile
        onedir_distpath_args = ["--distpath", path_to_platform_dist]
        onedir_args = main_args + onedir_distpath_args + extra_args
        logger.debug("Onedir build command line: " + " ".join(onedir_args))
        process = subprocess.Popen(onedir_args)
        process.wait()
        print("Building " + binary + " onefile")
        onefile_distpath_args = ["--distpath", os.path.sep.join([path_to_platform_dist, "executables"])]
        onefile_args = main_args + ["-F"] + onefile_distpath_args + extra_args
        logger.debug("Onefile build command line: " + " ".join(onefile_args))
        process = subprocess.Popen(onefile_args)
        process.wait()
        if platform.system() == "Windows":
            zip_dir(path_to_dist_dir=path_to_platform_dist, zip_filename_base=platform_basename)
        elif platform.system() == "Linux":
            gzip_dir(path_to_dist_dir=path_to_platform_dist, gzip_filename_base=platform_basename)

    if args.build_linux:
        import creds

        print("Starting build on remote Linux machine")
        build_on_linux(creds.LINUX_ADDRESS, creds.LINUX_USERNAME, creds.LINUX_PASSWORD)

    # Prepare all files for release
    print("Preparing release")
    for root, dirs, files in os.walk(top=path_to_dist):
        release_dir = os.path.join(os.getcwd(), "release")
        if not os.path.exists(release_dir):
            os.mkdir(release_dir)
        for file in files:
            shutil.move(os.path.join(root, file), release_dir)
        shutil.move(release_dir, path_to_dist)

    print("Finished")
    # Add dist files to git
    # print("Adding dist files to git")
    # process = subprocess.Popen(["git", "add", "-A", "dist"])
    # process.wait()
