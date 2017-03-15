import json
import subprocess

from os import path


class book(object):
    def __init__(self, filename):
        self.filename = filename
        self._text = ""
        self.addSettings()

    def addSettings(self):
        self.addLine("\documentclass[a5paper,9pt]{memoir}")
        self.addLine("")
        self.addLine("\chapterstyle{bringhurst}")
        self.addLine("\OnehalfSpacing")
        self.addLine("")
        self.addLine("\setlrmarginsandblock{0.6in}{1.0in}{*}")
        self.addLine("\setulmarginsandblock{0.7in}{0.75in}{*}")
        self.addLine("\checkandfixthelayout")
        self.addLine("\pagestyle{plain}")
        self.addLine("")
        self.addLine("")
        self.addLine("\\usepackage{xparse}")
        self.addLine("\DeclareDocumentCommand{\column}{mm}{")
        self.addLine("	\\renewcommand{\\thesection}{#1}")
        self.addLine("	\section{#2}")
        self.addLine("}")
        self.addLine("")
        self.addLine("\\begin{document}")

    def addTableOfContents(self):
        self.addLine("\\tableofcontents")

    def fix_string(self, string):
        string = string.replace("&", "\&")
        string = string.replace("%", "\%")
        return string

    def addLine(self, string):
        self._text += "\n" + self.fix_string(string)

    def addChapter(self, title):
        self.addLine("\\chapter{%s}" % title)

    def addColumn(self, date, title, text):
        self.addLine("\column{%s}{%s}" % (date, title))
        self.addLine(text)

    def endDocument(self):
        self.addLine("\end{document}")

    def generatePDF(self):
        with open(self.filename+".tex", "w") as tex:
            tex.write(self._text)
        p = subprocess.Popen(["/usr/local/texlive/2016/bin/x86_64-linux/pdflatex", self.filename])
        p.communicate()
        p = subprocess.Popen(["/usr/local/texlive/2016/bin/x86_64-linux/pdflatex", self.filename])
        p.communicate()
        p = subprocess.Popen(["mupdf", self.filename+".pdf"])


def main():
    b = book("book")
    b.addTableOfContents()
    text_files_dir = "/media/seneda/USB Stick/Book/cols/renamed/textfiles"
    columnsbyyear = json.load(open("titles.json"))
    for year, columns in sorted(columnsbyyear.items()):
        b.addChapter(year)
        for date, title in list(columns.items())[:5]:
            b.addColumn(date, title, open(path.join(text_files_dir, date+".txt")).read() )
    b.endDocument()
    b.generatePDF()

if __name__ == "__main__":
    main()