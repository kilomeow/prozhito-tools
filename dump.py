from csvtools import DumpTable, _OLDDELIMITER, _QUOTECHAR, _NEWDELIMITER
import os
import os.path

from notes import ProzhitoNotes
#from author import ProzhitoAuthor

class Wrapper:
    """ Interface for dump of Prozhito tables in csv. """    
    _NOTESFILENAME = 'notes.csv'
    _DIARIESFILENAME = 'diary.csv'
    _PERSONSFILENAME = 'persons.csv'

    def __init__(self, csvpath='.', _delimiter=_OLDDELIMITER, _quotechar=_QUOTECHAR):
        self.csvpath = csvpath
        
        self._olddelimiter = _delimiter
        self._newdelimiter = _NEWDELIMITER
        self._quotechar = _quotechar
                
        self.notes_filename = Wrapper._NOTESFILENAME
        self.diaries_filename = Wrapper._DIARIESFILENAME
        self.persons_filename = Wrapper._PERSONSFILENAME
        
        self.notes = None
        self.authors = None
        
        if self.checkpath(): self.load()


    def checkpath(self):
        ls = os.listdir(self.csvpath)
        #return self.notes_filename   in ls and\
        #       self.diaries_filename in ls and\
        #       self.persons_filename in ls
        return True

    def open(self, csvpath):
        self.csvpath = csvpath
        self.load()
    
    def load(self):
        notes_table = DumpTable(self, self.notes_filename)
        self.notes = ProzhitoNotes()
        self.notes.load(notes_table.csvreader, self.csvpath)
        #self.authors = 
