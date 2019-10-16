from csvtools import ProzhitoTable

class ProzhitoNotes(ProzhitoTable):
    def __init__(self):
        self.notes_list = list()
        self.dates = list()
    
    def load(self, dumpwrap, filename):
        import pickle
        
        super().load(dumpwrap, filename)
        for i in self.csvreader:
            n = ProzhitoNote()
            n.loadraw(i)
            self.notes_list.append(n)
        with open('dates', 'rb') as f:
            self.dates = pickle.load(f)
    
    def __iter__(self):
        return ProzhitoNotesIterable(self.csvfile, self.csvreader, self.dumpwrap)

    def sortDates(self):
        self.dates.sort()

    def byDate(self, date):
        notes_this_date = list()
        for d, i in self.dates:
            if d == date:
                notes_this_date.append(self.notes_list[i])
        return notes_this_date
    
    def searchDate(self, date):
        result = []        
        for n in self:
            if (n.date[0], n.date[1], n.date[2]) == (date[0], date[1], date[2]):
                result.append(n)
        return result
    
    def searchInterval(self, startdate, enddate):
        result = []
        for n in self:
            if startdate <= n.date <= enddate:
                result.append(n)
        return result
    
    def sortInterval(self, startdate, enddate):
        result = []
        sd = datetime(*startdate)
        ed = datetime(*enddate)
        for i in range((ed-sd).days+1):
            idate = (sd+timedelta(i)).timetuple()[:3]
            result.append((idate, list()))
        for n in self:
            if startdate <= n.date <= enddate:
                i = (datetime(*n.date)-sd).days
                result[i][1].append(n)
        return result
    
    def searchByDateParams(self, paramfunc):
        result = []
        for n in self:
            if paramfunc(n.date):
                result.append(n)
        return result


class ProzhitoNotesIterable:
    def __init__(self, csvfile, csvreader, dumpwrap):
        self.csvfile = csvfile
        self.csvfile.seek(0)
        self.csvreader = csvreader
        self.ind = 0
        self.dw = dumpwrap
    
    def __next__(self):
        l = next(self.csvreader)
        n = ProzhitoNote()
        n.loadraw(l)     
        self.ind += 1        
        return n


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
        self.diary = int(rawlist[0])
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
        return self.text
        
note.author.notes