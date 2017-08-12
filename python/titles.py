import json
import os
from pprint import pprint

import datetime

import shutil

from os.path import join

from python.dateslist import get_dates

t = json.load(open("/home/seneda/PycharmProjects/latexbook/doc_files/WMNclaims/titles"))

t2 = {}

t2 = {datetime.datetime.strptime(k, "%d.%m.%y").strftime("%Y-%m-%d") : v for k,v in t.items()}
t3 = dict.fromkeys(get_dates(), "")
t3.update(t2)
pprint(t3)
print(len(t3))

for root, dirs, files in os.walk("/home/seneda/PycharmProjects/latexbook/doc_files/txts"):
    for file in files:
        name, ext = file.split(".")[0], ".txt"
        # print(name, ext)
        if name in t3:
            shutil.copyfile(join(root, file),
            join(root, name + " " + t3[name] + ".txt"))
