from csvtools import _OLDDELIMITER, _NEWDELIMITER, _QUOTECHAR
import os
import os.path

from notes import ProzhitoNotes
from author import ProzhitoAuthors
from diary import ProzhitoDiaries


class Wrapper:
    """ Interface for dump of Prozhito tables in csv. """    
    _NOTESFILENAME = 'notes.csv'
    _DIARIESFILENAME = 'diary.csv'
    _PERSONSFILENAME = 'persons.csv'

    def __init__(self, csvpath='.', load_at_init=True):
        self.csvpath = csvpath
        
        self.notes_filename = Wrapper._NOTESFILENAME
        self.diaries_filename = Wrapper._DIARIESFILENAME
        self.persons_filename = Wrapper._PERSONSFILENAME
        
        self._olddelimiter = _OLDDELIMITER
        self._newdelimiter = _NEWDELIMITER
        self._quotechar    = _QUOTECHAR
        
        self.notes = None
        self.authors = None
        
        if load_at_init and self.checkpath(): self.load()

    def checkpath(self):
        ls = os.listdir(self.csvpath)
        return self.notes_filename   in ls and\
               self.diaries_filename in ls and\
               self.persons_filename in ls

    def open(self, csvpath):
        self.csvpath = csvpath
        self.load()
    
    def load(self):
        self.notes = ProzhitoNotes(self)
        self.notes.load(self.notes_filename)
        self.authors = ProzhitoAuthors(self)
        self.authors.load(self.persons_filename)
        self.diaries = ProzhitoDiaries(self)
        self.diaries.load(self.diaries_filename)
    
    def opencsv(self, csvfp):
        n = ProzhitoNotes()
        n.cleanload(csvfp)
        n._load()
        return n
