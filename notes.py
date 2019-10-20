import pickle
import os.path

class ID:
    def __init__(self, i):
        self.i = i

class ProzhitoNotes:
    def __init__(self):
        self.notes_list = list()
        self.dates = list()
    
    def load(self, table_iterator, datespath=''):
        # checking are dates already sorted and dumped
        self.dates_filename = os.path.join(datespath, 'dates.pkl')
        add_dates = not self.check_dates()
        
        # loading all the data
        c = 0
        for i in table_iterator:
            n = ProzhitoNote()
            n.loadraw(i)
            self.notes_list.append(n)
            if add_dates: self.dates.append((n.date, c))
            c += 0
        
        # if no dates are dumped, sorting collected dates
        if add_dates:
            self.dates.sort()
            self.dump_dates()
        else:
            self.load_dates()
        
    
    def check_dates(self):
        return os.path.exists(self.dates_filename)
    
    def load_dates(self):
        with open(self.dates_filename, 'rb') as f:
            self.dates = pickle.load(f)

    def dump_dates(self):
        with open(self.dates_filename, 'wb') as f:
            pickle.dump(self.dates, f)

    def get_note_by_date(self, di):
        return self.notes_list[di[1]]

    def get_note_by_date_index(self, i):
        return self.get_note_by_date(self.dates[i])

    def __iter__(self):
        return iter(map(self.get_note_by_date, self.dates))

    def slice(self, s):
        ns = ProzhitoNotes()
        d = self.dates[s]
        ns.dates = list(zip(map(lambda di: di[0], d), range(len(d))))
        ns.notes_list = list(map(self.get_node_by_date, d))
        return ns
    
    def find_id(self, i):
        ...
    
    def find_date(self, date):
        ...
        
    def find_interval(self, date1, date2, day_step=1):
        ...

    def __getitem__(self, k):
        if type(k) == int:
            return self.get_note_by_date_index(k)
        #elif type(k) == ID:
        #    return self.find_id(k.i)
        elif type(k) == tuple:
            return self.find_date(k)
        elif type(k) == slice:
            if type(k.start) == tuple or\
               type(k.stop)  == tuple:
                return self.find_interval(k.start, k.stop, k.end if type(k.end) == int else 1)
            elif type(k.start) == int or\
                 type(k.stop)  == int or\
                 type(k.step)  == int:
                return self.slice(k)
        
        # if nothing of these had matched
        raise TypeError
    
    def __repr__(self):
        l = len(self.dates)
        els = list()
        if l <= 4:
            els.extend(map(repr, self))
        else:
            els.extend(map(repr(self[:3])))
            els.extend(['...', repr(self[-1])])
        return '[ {0} ]'.format(' ,\n  '.join(els))

    # def byDate(self, date):
    #     notes_this_date = list()
    #     for d, i in self.dates:
    #         if d == date:
    #             notes_this_date.append(self.notes_list[i])
    #     return notes_this_date
    
    # def searchDate(self, date):
    #     result = []        
    #     for n in self:
    #         if (n.date[0], n.date[1], n.date[2]) == (date[0], date[1], date[2]):
    #             result.append(n)
    #     return result
    
    # def searchInterval(self, startdate, enddate):
    #     result = []
    #     for n in self:
    #         if startdate <= n.date <= enddate:
    #             result.append(n)
    #     return result
    
    # def sortInterval(self, startdate, enddate):
    #     result = []
    #     sd = datetime(*startdate)
    #     ed = datetime(*enddate)
    #     for i in range((ed-sd).days+1):
    #         idate = (sd+timedelta(i)).timetuple()[:3]
    #         result.append((idate, list()))
    #     for n in self:
    #         if startdate <= n.date <= enddate:
    #             i = (datetime(*n.date)-sd).days
    #             result[i][1].append(n)
    #     return result
    
    # def searchByDateParams(self, paramfunc):
    #     result = []
    #     for n in self:
    #         if paramfunc(n.date):
    #             result.append(n)
    #     return result


# class ProzhitoNotesIterable:
#     def __init__(self, csvfile, csvreader, dumpwrap):
#         self.csvfile = csvfile
#         self.csvfile.seek(0)
#         self.csvreader = csvreader
#         self.ind = 0
#         self.dw = dumpwrap
    
#     def __next__(self):
#         l = next(self.csvreader)
#         n = ProzhitoNote()
#         n.loadraw(l)     
#         self.ind += 1        
#         return n


def datereader(datestring):
    ds = datestring.split('-')
    return tuple(map(int, ds))


class ProzhitoNote:
    def __init__(self):
        self.raw = None
    
    def loadraw(self, rawlist):
        self.raw = rawlist
        self.ID = int(rawlist[0])
        #self.author = author.find_author(author_id)
        self.diary = int(rawlist[1])
        self.text = rawlist[2]
        self.date = datereader(rawlist[3])
        self.dateTop = datereader(rawlist[4])
        self.notDated = bool(int(rawlist[5]))
        self.julian_calendar = bool(int(rawlist[6]))
        #self.tags = list()
    
    def getDiary(self):
        return self.dw.diaries().byID(self.diary)

    def getAuthor(self):
        return self.getDiary().getAuthor()
    
    def __str__(self):
        return self.text
		
    def __repr__(self):
        return '#{0} "{1}..." @{2} [{3}]'.format(self.ID, ' '.join(self.text.split()[:3]), 
                                                 self.diary, self.date)
        
note.author.notes
