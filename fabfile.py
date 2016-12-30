import os
from fabric.api import run, cd, settings, get


def build():
    code_dir = "/tmp/QuackTest"
    with settings(warn_only=True):
        if run("test -d {}".format(code_dir)).failed:
            print("Source code not found. Cloning into directory {}".format(code_dir))
            run("git clone https://github.com/terrabitz/QuackTest/ {}".format(code_dir))
    with cd(code_dir):
        print("Pulling updated code")
        run("git pull")
        print("Building distribution")
        run("python build_dist.py")
        print("Copying to local machine")


def fetch():
    get("/tmp/QuackTest/dist/linux/",
        local_path=os.path.join(os.getcwd(), "dist"))
