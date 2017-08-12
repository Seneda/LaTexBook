import datetime
import json
from os.path import abspath, join

import os
from pprint import pprint


def get_dates(start=(2002,7,24), count=371):
    startdate = datetime.datetime(*start)

    next = startdate + datetime.timedelta(7)

    datetimes = [startdate + datetime.timedelta(7*i) for i in range(0, count)]
    datesStr = [d.strftime("%Y-%m-%d") for d in datetimes]
    return datesStr

def get_doc_files(dir=abspath(join(abspath(__file__),"../../doc_files/txts"))):

    docfiles = []
    # print(dir)
    for root, dirs, files in os.walk(dir):
        # print(root,dirs, files)
        docfiles += [(f, len(open(join(dir,f)).read().split())) for f in files]


    return sorted(docfiles)

def check():
    dates = get_dates()
    files = get_doc_files()

    r = dict.fromkeys(dates)
    for k in r.keys():
        r[k] = []

    for d in dates:
        r[d] += [f for f in files if f[0].startswith(d)]
        files = [f for f in files if not f[0].startswith(d)]


    # for k, v in sorted(r.items()):
        # if len(v) > 1:
        #     if abs(v[0][1]-v[1][1]) >100:
        #         print(k, v, abs(v[0][1]-v[1][1]))
            # else:
            #     print(k, v, abs(v[0][1]-v[1][1]))
        # elif len(v) <=1:
        #     print(k, v)

    print(pprint(r))

    print("Left :", "\n".join([str(f) for f in files]))

if __name__ == "__main__":
    check()