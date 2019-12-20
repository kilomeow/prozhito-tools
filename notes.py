from .csvtools import DumpTable

import pickle
import os.path


class ID:
    def __init__(self, i):
        self.i = i


class ProzhitoNotes(DumpTable):
    def __init__(self, dumpwrap):
        super().__init__(dumpwrap)
        self.notes_list = list()
        self.dates = list()
    
    def load(self, filename):
        super().load(filename)
        self._load()

    @classmethod
    def new_from_list(cls, dumpwrap, notes_iter):
        notes = cls(dumpwrap)
        notes.notes_list = list(notes_iter)
        notes.recalc_dates()
        return notes
    
    def _load(self):
        # checking are dates already sorted and dumped
        self.dates_filename = os.path.join(self.dw.csvpath, 'dates.pkl')
        add_dates = not self.check_dates()
        
        # loading all the data
        c = 0
        for i in self.table_iterator:
            n = ProzhitoNote(self.dw)
            try:
                n.loadraw(i)
            except:
                continue
            else:
                self.notes_list.append(n)
                if add_dates: self.dates.append((n.date, c))
                c += 1
	    
        
        # if no dates are dumped, sorting collected dates
        if add_dates:
            self.dates.sort()
            self.dump_dates()
        else:
            self.load_dates()
        
    def recalc_dates(self):
        for i in range(len(self.notes_list)):
            n = self.notes_list[i]
            self.dates.append((n.date, i))
        self.dates.sort()
    
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
        ns = ProzhitoNotes(self)
        d = self.dates[s]
        ns.dates = list(zip(map(lambda di: di[0], d), range(len(d))))
        ns.notes_list = list(map(self.get_note_by_date, d))
        return ns
    
    def find_id(self, i):
        ...
    
    # the two above implementations of find_date and find_interval is stupid and slow,
    # it should be rewritten using binary search on sorted dates list
    
    def find_date(self, date):
        for d, i in self.dates:
            if d == date:
                return self.notes_list[i]
        
    def find_interval(self, date1, date2, day_step=1):
        ns = ProzhitoNotes(self)
        c = 0
        for d, i in self.dates:
            if date1 <= d <= date2:
                ns.notes_list.append(self.notes_list[i])
                ns.dates.append((d, c))
                c += 1
            elif d > date2:
                break
        return ns

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
                return self.find_interval(k.start if k.start else (0, 0, 0), 
                                          k.stop if k.stop else (9999, 99, 99),
                                          k.step if type(k.step) == int else 1)
            elif type(k.start) == int or\
                 type(k.stop)  == int or\
                 type(k.step)  == int:
                return self.slice(k)
        
        # if nothing of these had matched
        raise TypeError
    
    def __len__(self):
        return len(self.dates)


def datereader(datestring):
    ds = datestring.split('-')
    return tuple(map(int, ds))


class ProzhitoNote:
    def __init__(self, dw):
        self.ID = None
        self.text = ''
        self.date = (0, 0, 0)
        self.dw = dw
    
    def loadraw(self, rawlist):
        self.raw = rawlist
        self.ID = int(rawlist[0])
        self.diary_ID = int(rawlist[1])
        self.text = rawlist[2]
        self.date = datereader(rawlist[3])
        self.dateTop = datereader(rawlist[4])
        self.notDated = bool(int(rawlist[5]))
        self.julian_calendar = bool(int(rawlist[6]))
        #self.tags = list()

    @property
    def diary(self):
        return self.dw.diaries.get_by_id(self.diary_ID)

    @property
    def author(self):
        return self.diary.author
    
    def __str__(self):
        return self.text
		
    def __repr__(self):
        return '#{0} "{1}..." @{2} [{3}]'.format(self.ID, ' '.join(self.text.split()[:3]), 
                                                 self.diary_ID, '-'.join(map(str, self.date)))

    @property
    def meta(self):
        return '#{0} @{1} {3} (@{2}) [{4}]'.format(self.ID, self.diary_ID,
                                                   self.author.ID, self.author.name,
                                                   '{0}.{1}.{2}'.format(*self.date))
