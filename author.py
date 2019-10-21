class ProzhitoAuthors:
    def __init__(self):
        self.authors_list = list()
    
    def load(self, table_iterator):
        for i in table_iterator:
            a = ProzhitoAuthor()
            a.loadraw(i)
            self.authors_list.append(a)


class ProzhitoAuthor:
    def __init__(self):
        ...
        # todo sasha

    def loadraw(self, r):
        ...

