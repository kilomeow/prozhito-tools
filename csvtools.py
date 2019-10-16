import csv
import os.path
from datetime import datetime, timedelta

_OLDDELIMITER = ',#'
_NEWDELIMITER = '§'
_QUOTECHAR    = '"'

DUMPWRAP = None

class CSV_Iterator:
    """ This is a special input wrapper to change delimiter to OK format for python csv module."""
    def __init__(self, f, oldstr, newstr):
        self.f = f
        self.oldstr = oldstr
        self.newstr = newstr
    
    def __iter__(self):
        return self
    
    def __next__(self):
        l = next(self.f)
        return l.replace(self.oldstr, self.newstr)


class CSV_Translater:
    """ This is a special output wrapper to change delimiter to OK format for python csv module."""
    def __init__(self, f, oldstr, newstr):
        self.f = f
        self.oldstr = oldstr
        self.newstr = newstr
    def write(self, s):
        self.f.write(s.replace(self.oldstr, self.newstr))
    def close(self):
        self.f.close()
    def flush(self):
        self.f.flush()


class ProzhitoTable:
    def __init__(self):
        self.dumpwrap = None
        self.filename = ''
        self.csvfile = None
        self.csvreader = None

    def load(self, dumpwrap, filename):
        filepath = os.path.join(dumpwrap.csvpath, filename)
        f = open(filepath, newline='', encoding='UTF-8')
        fi = CSV_Iterator(f, dumpwrap._olddelimiter, dumpwrap._newdelimiter)
        fr = csv.reader(fi, delimiter=dumpwrap._newdelimiter, quotechar=dumpwrap._quotechar)
        self.csvfile = f
        self.dumpwrap = dumpwrap
        self.filename = filename        
        self.csvreader = fr
    
    def seek(self, n):
        self.csvfile.seek(n)
    
    def byID(self, noteid):
        for n in self:
            if n.ID == noteid: return n
