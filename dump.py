from csvtools import ProzhitoTable, _OLDDELIMITER, _QUOTECHAR, _NEWDELIMITER
import os.path

from notes import ProzhitoNotes
#from author import ProzhitoAuthor

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
                
        self.notes_filename = Wrapper._NOTESFILENAME
        self.diaries_filename = Wrapper._DIARIESFILENAME
        self.persons_filename = Wrapper._PERSONSFILENAME
        
        self.notes = None
        self.authors = None
        
        if self.chekpath(): self.


    def checkpath(self):
        ls = os.path.listdir(self.csvpath)
        return self.notes_filename   in ls and\
               self.diaries_filename in ls and\
               self.persons_filename in ls

    def open(self, csvpath):
        self.csvpath = csvpath
        self.load()
    
    def load(self):
        notes_table = DumpTable(self, self.notes_filename)
        self.notes = notes.ProzhitoNotes()
        
        #self.authors = 
    
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
