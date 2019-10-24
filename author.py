from csvtools import DumpTable


class ProzhitoAuthors(DumpTable):
    def __init__(self, dumpwrapper):
        super().__init__(dumpwrapper)
        self.authors_list = list()
    
    def load(self, filename):
        super().load(filename)
        for i in self.table_iterator:
            a = ProzhitoAuthor()
            a.loadraw(i)
            self.authors_list.append(a)

    def get_by_id(self, ID):
        print('trying to find author with ID', ID)
        for a in self.authors_list:
            if a.ID == ID: return a

    def __getitem__(self, k):
        return self.authors_list[k]
    
    def __len__(self):
        return len(self.authors_list)


class ProzhitoAuthor:
    def __init__(self):
        self.raw = None
        # todo sasha

    def loadraw(self, r):
        self.raw = r
        self.ID = int(r[0])
        self.first_name = r[1]
        self.last_name = r[2]
        self.second_name = r[3]
        # todo sasha

    def __repr__(self):
       return '#{0} {1} {2} {3}'.format(self.ID, self.first_name,
                                        self.second_name, self.last_name)
