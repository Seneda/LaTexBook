import json
import os
import subprocess
from os import path

import datetime

from python.date import makeDate
from python.dateslist import get_dates


class book(object):
    def __init__(self, filename):
        self.filename = filename
        self._text = ""
        self.addSettings()

    def addSettings(self):
        self.addLine("\documentclass[a5paper,9pt]{memoir}")
        self.addLine("")
        self.addLine("\chapterstyle{bianchi}")


        self.addLine("\OnehalfSpacing")
        self.addLine("\openany")
        self.addLine("\\usepackage{titletoc}")
        self.addLine("\dottedcontents{section}[1.2in]{}{1.0in}{10pt}")
        self.addLine("\setlrmarginsandblock{0.6in}{1.0in}{*}")
        self.addLine("\setulmarginsandblock{0.7in}{0.75in}{*}")
        self.addLine("\checkandfixthelayout")
        self.addLine("\pagestyle{plain}")
        self.addLine("\\renewcommand{\chapternumberline}[1]{}")
        self.addLine("")



        self.addLine("\\usepackage{xparse}")
        self.addLine("\DeclareDocumentCommand{\column}{mm}{")
        self.addLine("	\\renewcommand{\\thesection}{#1}")
        self.addLine("	\section{#2}")
        self.addLine("}")
        self.addLine("")
        self.addLine("\\begin{document}")

    def addTableOfContents(self):
        self.addLine("\\begin{KeepFromToc}")
        self.addLine("\\tableofcontents")
        self.addLine("\\end{KeepFromToc}")

    def fix_string(self, string):
        string = string.replace("&", "\&")
        string = string.replace("%", "\%")
        string = string.replace("’", "'")
        string = string.replace(" \"", " ``")
        string = string.replace("$", "\$")
        return string


    def addLine(self, string):
        self._text += "\n" + self.fix_string(string)


    def addChapter(self, title):
        self.addLine("\\chapter*{%s}" % title)
        self.addLine("\\addcontentsline{toc}{chapter}{%s}" % title)

    def addIntro(self, title, text):
        self.addChapter(title)
        self.addLine(text)

    def addColumn(self, date, title, text):
        self.addLine("\\Needspace{10\\baselineskip}")
        self.addLine("\column{%s}{%s}" % (date, titleCase(title)))
        self.addLine(stripDateAtStart(text))


    def endDocument(self):
        self.addLine("\end{document}")


    def generatePDF(self):
        with open(path.join("latex", self.filename+".tex"), "w") as tex:
            tex.write(self._text)
        p = subprocess.Popen(["/usr/local/texlive/2016/bin/x86_64-linux/pdflatex", self.filename], cwd="latex")
        p.communicate()
        p = subprocess.Popen(["/usr/local/texlive/2016/bin/x86_64-linux/pdflatex", self.filename], cwd="latex")
        p.communicate()
        p = subprocess.Popen(["mupdf", self.filename+".pdf"], cwd="latex")


import re


def titleCase(string):
    smallwords = ["a", "an", "the", "at", "by", "for", "in", "of", "on",
                  "to", "up", "and", "as", "but", "or", "and", "nor", "for"]

    def repl_func(m):
        """process regular expression match groups for word upper-casing problem"""
        return m.group(1) + m.group(2).upper()

    words = re.sub("(^|\s)(\"\S|\S)", repl_func, string)
    words = words.split()
    r = words[:1]
    for word in words[1:]:
        if word.lower() in smallwords:
            r.append(word.lower())
        else:
            r.append(word)
    return " ".join(r)


def stripDateAtStart(string):
    print(repr(string[:10]))
    string = string.strip("\ufeff")
    string = string.strip()
    print(repr(string[:10]))
    end_of_first_bit = re.search("\.|\n", string).start()
    first_bit = string[:end_of_first_bit]
    print("Looking for date")
    print(first_bit)
    if (len([a for a in first_bit if a.isdigit()]) >= 3) or ("’0" in first_bit):
        # print(string[:60])
        # print([a for a in first_bit if a.isdigit()])
        print("Found date line: %d %s" % (end_of_first_bit, first_bit))
        return string[end_of_first_bit:]
    else:
        return string

def get_file(prefix, filesdir):
    for root, dir, files in os.walk(filesdir):
        for f in files:
            if f.startswith(prefix):
                return open(path.join(root, f))
    else:
        raise Exception("COuldnt find a file starting with {} in {}".format(prefix, filesdir))

def main():
    b = book("book")
    b.addTableOfContents()
    text_files_dir = "/home/seneda/PycharmProjects/latexbook/doc_files/txts"

    b.addIntro("Ian Pettyfer Brief Background",
               open(path.join(text_files_dir, "Ian Pettyfer Brief Background.txt")).read())

    # For each file in the dir

    # Add a column
    year = 0
    for root, dir, files in os.walk(text_files_dir):
        for f in sorted(files):
            try:
                print(f)
                date = datetime.datetime.strptime(f[:10], "%Y-%m-%d")
                if date.year != year:
                    year = date.year
                    b.addChapter(year)

                title = titleCase(f.split(".")[0][10:].strip())


                print(date)
                print(title)
                b.addColumn(date.strftime("%B %-d"), title, open(path.join(root,f)).read())
            except Exception as e:
                print("\n\n\nFailed on "+f+" "+str(e)+"\n\n\n")
    b.endDocument()
    b.generatePDF()



if __name__ == "__main__":
    main()
