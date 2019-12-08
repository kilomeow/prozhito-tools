from csvtools import DumpTable
from notes import ProzhitoNotes

class ProzhitoAuthors(DumpTable):
    def __init__(self, dumpwrapper):
        super().__init__(dumpwrapper)
        self.authors_list = list()
    
    def load(self, filename):
        super().load(filename)
        for i in self.table_iterator:
            a = ProzhitoAuthor(self.dw)
            a.loadraw(i)
            self.authors_list.append(a)

    def get_by_id(self, ID):
        for a in self.authors_list:
            if a.ID == ID: return a

    def __getitem__(self, k):
        return self.authors_list[k]
    
    def __len__(self):
        return len(self.authors_list)


class ProzhitoAuthor:
    def __init__(self, dumpwrap):
        self.raw = None
        self.dw = dumpwrap
        # todo sasha

    def loadraw(self, r):
        self.raw = r
        self.ID = int(r[0])
        self.first_name = r[1]
        self.last_name = r[2]
        self.second_name = r[3]
        # todo sasha

    @property
    def diaries(self):
        authors_diary = filter(lambda diary: diary.author_ID == self.ID,
                               self.dw.diaries.diaries_list)
        return list(authors_diary)

    @property
    def notes(self):
        diaries_id = list(map(lambda diary: diary.ID, self.diaries))
        author_notes = filter(lambda note: note.diary_ID in diaries_id, self.dw.notes)
        return ProzhitoNotes.new_from_list(self.dw, author_notes)

    @property
    def name(self):
        return "{0} {1} {2}".format(self.first_name, self.second_name, self.last_name)

    def __repr__(self):
       return '#{0} {1} {2} {3}'.format(self.ID, self.first_name,
                                        self.second_name, self.last_name)
