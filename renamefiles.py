import datetime
import os

from os.path import join


def rename(path, file):
    try:
        print("Renaming %s" % file)
        name, ext = file.split(".")
        d = datetime.datetime.strptime(name, "%y %b %d")
        print("Renaming %s to %s" % (join(path,file), join(path,d.strftime("%Y-%m-%d."+ext))))
        os.rename(join(path,file), join(path,d.strftime("%Y-%m-%d."+ext)))
    except Exception as e:
        print(e)


def renameFiles(path="files/originals/"):
    for root, dirs, files in os.walk(path):
        for file in files:
            rename(root, file)

if __name__ == "__main__":
    renameFiles()
