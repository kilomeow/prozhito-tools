import csv
import os.path
from datetime import datetime, timedelta

_OLDDELIMITER = ',#'
_NEWDELIMITER = '§'
_QUOTECHAR    = '"'

DUMPWRAP = None

from bisect import bisect_left

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
        
        self._notes = None
        self.is_notes = False
        
        global DUMPWRAP
        DUMPWRAP = self

    def dumpopen(self, csvpath):
        self.csvpath = csvpath
    
    def csvopen(self, csvfilename):
        t = ProzhitoTable()
        t.load(self, csvfilename)
        return t.csvreader
    
    def notes(self):
        if not self.is_notes:
            n = ProzhitoNotes()
            n.load(self, self._notesfilename)
            n.sortDates()
            self._notes = n
            self.is_notes = True
        return self._notes
    
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
    def __init__(self):
        self.notes_list = list()
        self.dates = list()
    
    def load(self, dumpwrap, filename):
        super().load(dumpwrap, filename)
        c = 0
        for i in self.csvreader:
            n = ProzhitoNote()
            n.loadraw(i)
            self.notes_list.append(n)
            self.dates.append((n.date, c))
            c += 1
    
    def __iter__(self):
        return ProzhitoNotesIterable(self.csvfile, self.csvreader, self.dumpwrap)

    def sortDates(self):
        self.dates.sort()

    def byDate(self, date):
        notes_this_date = list()
        for d, i in self.dates:
            if d == date:
                notes_this_date.append(self.notes_list[i])
        return notes_this_date
    
    def searchDate(self, date):
        result = []        
        for n in self:
            if (n.date[0], n.date[1], n.date[2]) == (date[0], date[1], date[2]):
                result.append(n)
        return result
    
    def searchInterval(self, startdate, enddate):
        result = []
        for n in self:
            if startdate <= n.date <= enddate:
                result.append(n)
        return result
    
    def sortInterval(self, startdate, enddate):
        result = []
        sd = datetime(*startdate)
        ed = datetime(*enddate)
        for i in range((ed-sd).days+1):
            idate = (sd+timedelta(i)).timetuple()[:3]
            result.append((idate, list()))
        for n in self:
            if startdate <= n.date <= enddate:
                i = (datetime(*n.date)-sd).days
                result[i][1].append(n)
        return result
    
    def searchByDateParams(self, paramfunc):
        result = []
        for n in self:
            if paramfunc(n.date):
                result.append(n)
        return result


class ProzhitoNotesIterable(ProzhitoTableIterable):
    def __init__(self, csvfile, csvreader, dumpwrap):
        self.csvfile = csvfile
        self.csvfile.seek(0)
        self.csvreader = csvreader
        self.ind = 0
        self.dw = dumpwrap
    
    def __next__(self):
        l = next(self.csvreader)
        n = ProzhitoNote()
        n.loadraw(l)     
        self.ind += 1        
        return n


def datereader(datestring):
    ds = datestring.split('-')
    return tuple(map(int, ds))


class ProzhitoNote(ProzhitoTableNode):
    def __init__(self):
        self.raw = None
    
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
		
    def __repr__(self):
        return self.text


class ProzhitoDiaries(ProzhitoTable):
    ...


class ProzhitoDiary(ProzhitoTableNode):
    ...


class ProzhitoPerson:
    ...
