from .notes import ProzhitoNotes
from .csvtools import DumpTable

class ProzhitoDiaries(DumpTable):
    def __init__(self, dumpwrapper):
        super().__init__(dumpwrapper)
        self.diaries_list = list()
        self.diaries_dict = dict()

    def load(self, filename):
        super().load(filename)
        for i in self.table_iterator:
            d = ProzhitoDiary(self.dw)
            d.loadraw(i)
            self.diaries_list.append(d)
            self.diaries_dict[d.ID] = d

    def __getitem__(self, k):
        if type(k) == int or type(k) == slice:
            return self.diaries_list[k]
        elif type(k) == 'str' and k.startswith('@'):
            return self.diaries_dict[int(k.lstrip('@'))]

    def get_by_id(self, ID):
        return self.diaries_dict[ID]

    def __len__(self):
        return len(self.diaries_list)


class ProzhitoDiary:
    def __init__(self, dw):
        self.dw = dw
        self.raw = None

    def loadraw(self, r):
        self.raw = r
        self.ID = int(r[0])
        self.author_ID = int(r[1])

    @property
    def author(self):
        return self.dw.authors.get_by_id(self.author_ID)

    @property
    def notes(self):
        notes_of_diary = filter(lambda note: note.diary_ID == self.ID, self.dw.notes)
        return ProzhitoNotes.new_from_list(self.dw, notes_of_diary)

    def __repr__(self):
        return '@{0} raw {1}'.format(self.ID, self.raw)
