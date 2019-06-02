import csv
import os.path
from datetime import datetime

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


class DumpWrapper:
    """ Interface for dump of Prozhito tables in csv. """    
    _NOTESFILENAME = 'notes.csv'
    _DIARIESFILENAME = 'diary.csv'
    _PERSONSFILENAME = 'persons.csv'

    def __init__(self, csvpath='', _delimiter=_OLDDELIMITER, _quotechar=_QUOTECHAR):
        self.csvpath = csvpath
        
        self._olddelimiter = _delimiter
        self._newdelimiter = _NEWDELIMITER
        self._quotechar = _quotechar
                
        self._notesfilename = DumpWrapper._NOTESFILENAME
        self._diariesfilename = DumpWrapper._DIARIESFILENAME
        self._personsfilename = DumpWrapper._PERSONSFILENAME

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
    
    def diaries(self):
        d = ProzhitoDiaries()
        d.load(self, self._diariesfilename)
        return d

    def persons(self):
        p = ProzhitoPersons()
        p.load(self, self._personsfilename)
        return p


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


class ProzhitoTableIterable:
    ...


class ProzhitoTableNode:
    def loadraw(self, rawlist):
        ...


class ProzhitoNotes(ProzhitoTable):
    def __iter__(self):
        return ProzhitoNotesIterable(self.csvreader, self.dumpwrap)

    def byDate(self, date):
        for n in self:
            if n.date == date: return n
    
    def searchDate(self, date):
        result = []        
        for n in self:
            if n.date == date: result.append(n)
        return result
    
    def searchInterval(self, startdate, enddate):
        result = []
        for n in self:
            if startdate <= n.date <= enddate:
                result.append(n)
        return result
    
    #def sortInterval(self, startdate, enddate):
    #    result = []        
    #    for i in range((enddate-startdate).days()):
    #        result.append([])
    #    for n in self:
    #        if startdate <= n.date <= enddate:
    #            i = (n.date-startdate).days()
    #            result[i].append(n)
    #    return result
    
    def searchByDateParams(self, paramfunc):
        result = []
        for n in self:
            if paramfunc(n.date):
                result.append(n)
        return result


class ProzhitoNotesIterable(ProzhitoTableIterable):
    def __init__(self, csvreader, dumpwrap):
        self.csvreader = csvreader
        self.csvreader.seek(0)
        self.ind = 0
        self.dw = dumpwrap
    
    def __next__(self):
        l = next(self.csvreader)
        n = ProzhitoNote(self.dw)
        n.loadraw(l)     
        self.ind += 1        
        return n


def datereader(datestring):
    try:
        return datetime.strptime(datestring, '%Y-%m-%d').date().timetuple()
    except ValueError:
        ds = datestring.split('-')
        return tuple(map(int, ds))
            


class ProzhitoNote(ProzhitoTableNode):
    def __init__(self, dumpwrap):
        self.raw = None
        self.dw = dumpwrap
    
    def loadraw(self, rawlist):
        self.raw = rawlist
        self.ID = int(rawlist[0])
        self.diary = int(rawlist[0])
        self.text = rawlist[2]
        self.date = datereader(rawlist[3])
        self.dateTop = datereader(rawlist[4])
        self.notDated = bool(int(rawlist[5]))
        self.julian_calendar = bool(int(rawlist[6]))
    
    def getDiary(self):
        return self.dw.diaries().byID(self.diary)

    def getAuthor(self):
        return self.getDiary().getAuthor()
    
    def __str__(self):
        return self.text


class ProzhitoDiaries(ProzhitoTable):
    ...


class ProzhitoDiary(ProzhitoTableNode):
    ...


class ProzhitoPerson:
    ...
