from csvtools import ProzhitoTable, _OLDDELIMITER, _QUOTECHAR, _NEWDELIMITER
import notes

DUMPWRAP = None

class Wrapper:
    """ Interface for dump of Prozhito tables in csv. """    
    _NOTESFILENAME = 'notes.csv'
    _DIARIESFILENAME = 'diary.csv'
    _PERSONSFILENAME = 'persons.csv'

    def __init__(self, csvpath='', _delimiter=_OLDDELIMITER, _quotechar=_QUOTECHAR):
        self.csvpath = csvpath
        
        self._olddelimiter = _delimiter
        self._newdelimiter = _NEWDELIMITER
        self._quotechar = _quotechar
                
        self._notesfilename = Wrapper._NOTESFILENAME
        self._diariesfilename = Wrapper._DIARIESFILENAME
        self._personsfilename = Wrapper._PERSONSFILENAME
        
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
            n = notes.ProzhitoNotes()
            n.load(self, self._notesfilename)
            n.sortDates()
            self._notes = n
            self.is_notes = True
        return self._notes
    
    #def diaries(self):
    #    d = ProzhitoDiaries()
    #    d.load(self, self._diariesfilename)
    #    return d

    #def persons(self):
    #    p = ProzhitoPersons()
    #    p.load(self, self._personsfilename)
    #    return p
