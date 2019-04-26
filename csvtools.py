import csv
import os.path

_OLDDELIMITER = ',#'
_NEWDELIMITER = '§'
_QUOTECHAR    = '"'

class CSV_Iterator:
    """ Produce iterator interface for csv files with replacing characters """
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
    """ Output file-like object that translates characters. """
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


class DumpWrapper:
    """ Wrapper around dump of Prozhito tables in csv """    
    _NOTESFILENAME = 'notes.csv'
    ...

    def __init__(self, csvpath='', _delimiter=_OLDDELIMITER, _quotechar=_QUOTECHAR):
        self.csvpath = csvpath
        
        self._olddelimiter = _delimiter
        self._newdelimiter = _NEWDELIMITER
        self._quotechar = _quotechar
                
        self._notesfilename = DumpWrapper._NOTESFILENAME
        ...

    def dumpopen(self, csvpath):
        self.csvpath = csvpath
    
    def csvopen(self, csvfilename):
        t = ProzhitoTable()
        t.load(self, csvfilename)
        return t.csvreader
    
    def notes(self):
        n = ProzhitoNotes()
        n.load(self, self._notesfilename)
        return n


class ProzhitoTable:
    def __init__(self):
        self.dumpwrap = None
        self.filename = ''        
        self.csvreader = None

    def load(self, dumpwrap, filename):
        filepath = os.path.join(dumpwrap.csvpath, filename)
        f = open(filepath, newline='')
        fi = CSV_Iterator(f, dumpwrap._olddelimiter, dumpwrap._newdelimiter)
        fr = csv.reader(fi, delimiter=dumpwrap._newdelimiter, quotechar=dumpwrap._quotechar)
        self.dumpwrap = dumpwrap
        self.filename = filename        
        self.csvreader = fr


class ProzhitoNotes(ProzhitoTable):
    def dateOf(self, ind):
        return None

    def byDate(self, date):
        return None

    def byInterval(self, startdate, enddate):
        return None
