import csv
import os.path
from datetime import datetime, timedelta

_OLDDELIMITER = ',#'
_NEWDELIMITER = '§'
_QUOTECHAR    = '"'

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


class DumpTable:
    def __init__(self, dumpwrap):
        self.dw = dumpwrap
        
        self._olddelimiter = dumpwrap._olddelimiter
        self._newdelimiter = dumpwrap._newdelimiter
        self._quotechar    = dumpwrap._quotechar
        
        self.filename = None
        self.csvfile = None
        self.table_iterator = None

    def load(self, filename):
        filepath = os.path.join(self.dw.csvpath, filename)
        f = open(filepath, newline='', encoding='UTF-8')
        fi = CSV_Iterator(f, self.dw._olddelimiter, self.dw._newdelimiter)
        fr = csv.reader(fi, delimiter=self.dw._newdelimiter, quotechar=self.dw._quotechar)
        
        self.filename = filename
        self.csvfile = f
        self.table_iterator = fr
    
    def cleanload(self, filepath):
        with open(filepath) as f:
            self.csvfile = f
            self.table_iterator = csv.reader(f)
        self.filename = os.path.split(filepath)[-1]

    def __repr__(self):
        l = len(self)
        els = list()
        if l <= 4:
            els.extend(map(repr, self))
        else:
            els.extend(map(repr, self[:3]))
            els.extend(['...', repr(self[-1])])
        return '[ {0} ]'.format(' ,\n  '.join(els))

    def dump(self, fn):
        with open(fn, 'w') as f:
            w = csv.writer(f)
            for n in self:
                w.writerow(n.raw)
    
    def seek(self, n):
        self.csvfile.seek(n)
    
    def byID(self, noteid):
        for n in self:
            if n.ID == noteid: return n
