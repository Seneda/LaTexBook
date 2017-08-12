import datetime
import os

from os.path import join


def rename(path, file):
    try:
        name, ext = file.split(".")
        if not (name.endswith('2003') or name.endswith('2002')):
            return
        print("Renaming %s" % file)
        d = datetime.datetime.strptime(name,
                                       "%d-%m-%Y")
        print("Renaming %s to %s" % (join(path,file), join(path,d.strftime("%Y-%m-%d."+ext))))
        os.rename(join(path,file), join(path,d.strftime("%Y-%m-%d."+ext)))
    except Exception as e:
        print(e)


def renameFiles(path="/home/seneda/PycharmProjects/latexbook/doc_files"):
    for root, dirs, files in os.walk(path):
        for file in files:
            print(file)
            rename(root, file)

if __name__ == "__main__":
    renameFiles()
