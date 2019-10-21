class ProzhitoAuthors:
    def __init__(self):
        self.authors_list = list()
    
    def load(self, table_iterator):
        for i in table_iterator:
            a = ProzhitoAuthor()
            a.loadraw(i)
            self.authors_list.append(a)

    def get_by_id(self, ID):
        ...
        # todo sasha

    def __getitem__(self, k):
        return self.get_by_id(k)


class ProzhitoAuthor:
    def __init__(self):
        ...
        # todo sasha

    def loadraw(self, r):
        ...
        # todo sasha

    def __repr__(self):
       return 'meow' # todo sasha
