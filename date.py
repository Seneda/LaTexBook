from datetime import datetime as dt


def suffix(d):
    return "\\textsuperscript{%s}" % ('th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th'))

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def makeDate(format, datestring):
    d = dt.strptime(datestring, "%Y-%m-%d")
    return custom_strftime(format, d)