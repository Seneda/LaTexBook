import datetime
import os

from os.path import join

import subprocess


def rename(path, file):
    try:
        print("Renaming %s" % file)
        name, ext = file.split(".")
        if ext != "txt":
            print("Converting {} to {}".format(join(path, file), join(path, name+".txt")))
            cmd = ["catdoc", join(path, file)]
            textfile = join(path, name+".txt")
            subprocess.Popen(cmd, stdout=open(textfile, 'w'))
    except Exception as e:
        print(e)


def renameFiles(path="files/originals/"):
    for root, dirs, files in os.walk(path):
        for file in files:
            rename(root, file)

if __name__ == "__main__":
    renameFiles()
