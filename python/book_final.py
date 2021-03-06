import json
import os
import subprocess
from os import path

import datetime
from os.path import abspath
from pprint import pprint

from dateslist import get_dates


class book(object):
    def __init__(self, filename):
        self.filename = filename
        self._text = ""
        self.addPreamble()

    def beginDocument(self):
        self.addLine("\\begin{document}")

    def addPreamble(self):
        self.addRawLine(open(path.join(path.dirname(__file__), "preamble.tex")).read())
        return

    def addTableOfContents(self):
        # self.addLine("\chapterstyle{default}")
        self.addLine("\\tableofcontents*")
        # self.addLine("\chapterstyle{mychapter}")

    @staticmethod
    def fix_string(string):
        corrections = [
            ("&", "\&"),
            ("%", "\%"),
            (" '", "`"),
            ("’", "'"),
            ("‘", "`"),
            ("“", "``"),
            ("”", "\""),
            ("–", "--"),
            (" ?", "?"),
            ("é", "e"),
            # ("°", "\degree "),
            (" \"", " ``"),
            ("\n\"", "\n``"),
            ("{\"", "{``"),
            ("$", "\$"),
            ("£", "\\textsterling"),
            ("Defra", "DEFRA"),
            ("traveled", "travelled"),
            ("severly", "severely"),
            ("Chumleigh", "Chulmleigh"),
            ("Gilbard", "Gillbard")
        ]
        for a,b in corrections:
            string = string.replace(a, b)
        return string


    def addLine(self, string):
        self._text += "\n" + self.fix_string(string)

    def addRawLine(self, string):
        self._text += "\n" + string

    def addComm(self, string):
        self.addRawLine("\n%"+string+"\n")


    def addChapter(self, title):
        self.addLine("\\chapter*[%s]{%s}" % (title,title))
        self.addLine("\\addcontentsline{toc}{chapter}{%s}" % title)

    def addSection(self, title):
        self.addLine("\\monthsec{%s}" % title)
        # self.addLine("\\section*{%s}" % (title))
        # self.addLine("\\addcontentsline{toc}{section}{%s}" % title)

    def addIntro(self, title, text):
        self.addChapter(title)
        self.addLine(text)

    def addColumn(self, date, title, text):
        print("Adding column {}".format(title))
        self.addLine("\\Needspace{10\\baselineskip}")
        title = titleCase(title)
        long_date = dtStylish(date, "%B {th}")
        short_date = dtStylish(date, "%b {th}")
        day = dtStylish(date, "{th}")
        self.addLine("\column{%s}{%s}{%s}{%s}" % (long_date, short_date, title, day))
        if text:
            text = text[:]

        self.addLine(stripDateAtStart(text))
        self.addLine("\\nowidow[3]")

    def makeGlossary(self, dir):
        glossary = open(path.join(dir, "glossary2.txt")).read()
        glossary = [g.split(' - ') for g in glossary.splitlines()]
        pprint(glossary)
        glossary = sorted(glossary, key=lambda x: x[1].upper())
        pprint(glossary)

        for i, g in enumerate(glossary):
            if len(g) == 3:
                if int(g[0]) > 2:
                    if i < (len(glossary)-1):
                        self.addLine("\longnewglossaryentry{%s}{name=%s}{%s \\vspace{2.1 mm}}" % (g[1], g[1], g[2]))
                    else:
                        self.addLine("\longnewglossaryentry{%s}{name=%s}{%s}" % (g[1], g[1], g[2]))



    def addGlossary(self):
        # self.addLine("\printglossary{type=acronym}")
        self.addLine("\\begingroup")
        self.addLine("\chapterstyle{mychaptersmall}")
        self.addLine("\clearpage")
        self.addLine("\glsaddallunused")
        self.addLine("\printglossary[title={Glossary of Farming Acronyms}]")
        self.addLine("\endgroup")

    def endDocument(self):
        self.addLine("\end{document}")

    def generatePDF(self):
        with open(path.join("latex", self.filename+".tex"), "w") as tex:
            tex.write(self._text)
        # p = subprocess.Popen(["/usr/local/texlive/2016/bin/x86_64-linux/pdflatex", self.filename], cwd="latex")
        p = subprocess.Popen(["/usr/bin/pdflatex", self.filename], cwd="latex")
        p.communicate()
        p = subprocess.Popen(["ls", self.filename], cwd="latex")
        p.communicate()
        # p = subprocess.Popen(["/usr/local/texlive/2016/bin/x86_64-linux/makeglossaries", self.filename], cwd="latex")
        p = subprocess.Popen(["/usr/bin/makeglossaries", self.filename], cwd="latex")
        p.communicate()

        # p = subprocess.Popen(["/usr/local/texlive/2016/bin/x86_64-linux/pdflatex", self.filename], cwd="latex")
        p = subprocess.Popen(["/usr/bin/pdflatex", self.filename], cwd="latex")
        p.communicate()
        # p = subprocess.Popen(["/usr/local/texlive/2016/bin/x86_64-linux/pdflatex", self.filename], cwd="latex")
        # p.communicate()
        # p = subprocess.Popen(["/usr/local/texlive/2016/bin/x86_64-linux/pdflatex", self.filename], cwd="latex")
        # p.communicate()

        p = subprocess.Popen(["mupdf", self.filename+".pdf"], cwd="latex")


import re


def titleCase(string):
    smallwords = ["a", "an", "the", "at", "by", "for", "in", "of", "on", "to", "up", "and", "as", "but", "or", "and",
                  "nor", "for", "is", "it", "be", "are"]

    def repl_func(m):
        """process regular expression match groups for word upper-casing problem"""
        return m.group(1) + m.group(2).upper()

    words = re.sub("(^|\s)(\"\S|\S)", repl_func, string)
    words = words.split()
    r = words[:1]
    for word in words[1:-1]:
        if word.lower() in smallwords:
            r.append(word.lower())
        else:
            r.append(word)
    r.append(words[-1])
    return " ".join(r)

def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def dtStylish(dt,f):
    return dt.strftime(f).replace("{th}", ord(dt.day))

def stripDateAtStart(string):
    if string == "":
        return string
    print(repr(string[:10]))
    string = string.strip("\ufeff")
    string = string.strip()
    print(repr(string[:10]))
    end_of_first_bit = re.search("\.|\n", string).start()
    first_bit = string[:end_of_first_bit]
    print("Looking for date")
    print(first_bit)
    if (len(first_bit) < 20) and ((len([a for a in first_bit if a.isdigit()]) >= 3) or ("’0" in first_bit)):
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

def fixPars(text):
    # text = text.split("\n\n")
    # text = "\looseness=-1\n\n".join(text)
    return text


def main():
    b = book("book")

    text_files_dir = "/home/seneda/latexbook/doc_files/txts"
    b.makeGlossary(text_files_dir)
    b.beginDocument()
    b.addLine("""
    \\vspace*{12em}
    {
    \HUGE  
    \centerline{\\textbf{The View from}} 
    \centerline{\\textbf{South Emlett}}
 \\thispagestyle{empty}

     }
    """)
    b.addLine("\\newpage")
    b.addRawLine("""\mbox{}
\\thispagestyle{empty}
\\newpage""")
    b.addLine("\includepdf{titlepage}")
    b.addRawLine("""\mbox{}
\\thispagestyle{empty}
\\newpage""")
    b.addLine("\pagenumbering{roman}")
    b.addLine("\includepdf{dedicationpage}")

    b.addRawLine("""\mbox{}
\\thispagestyle{empty}
\\newpage""")
    b.addLine("\setcounter{page}{1}")
    b.addTableOfContents()
    b.addLine("\cleardoublepage")
    # b.addIntro("Ian Pettyfer Brief Background",
    #            open(path.join(text_files_dir, "Ian Pettyfer Brief Background.txt")).read())

    # For each file in the dir

    # Add a column
    year = 0
    month = 0
    # for root, dir, files in os.walk(text_files_dir):
    #     for f in sorted(files):
    for datestr in get_dates()[:]:
            try:
                # print(f)
                date = datetime.datetime.strptime(datestr, "%Y-%m-%d")
                if date.year != year:
                    year = date.year
                    b.addChapter(year)
                    if year == 2002:
                        b.addLine("\pagenumbering{arabic}")
                        b.addLine("\setcounter{page}{1}")
                if date.month != month:
                    month = date.month
                    b.addSection(date.strftime("%B"))
                file = get_file(datestr, text_files_dir)
                print("Filename:",file.name)

                filename = ".".join(file.name.split(".")[:-1])
                print("Filename:",filename)
                title = titleCase(filename.split(datestr)[1]).strip()
                if "NO ARTICLE" in title.upper():
                    continue

                print(date)
                print(title)

                # if "\n\n" not in file.read().strip():
                #     input(date)
                b.addColumn(date, title, fixPars(file.read()))

            except Exception as e:
                print("\n\n\nFailed on "+datestr+" "+str(e)+"\n\n\n")
                raise
    b.addGlossary()
    b.endDocument()
    b.generatePDF()



if __name__ == "__main__":
    main()
