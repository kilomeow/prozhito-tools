from notes import ProzhitoNotes, ProzhitoNote
from random import randrange

notes = ProzhitoNotes()
notes.notes_list = [ProzhitoNote() for i in range(10)]

for n in notes.notes_list: n.date = (randrange(1800, 2000), randrange(1, 13), randrange(1, 31))
for n in notes.notes_list: n.text = ' '.join([chr(97+randrange(0,25)) for i in range(10)])
for n in notes.notes_list: n.ID, n.diary = randrange(0, 9999), randrange(0, 5)

notes.recalc_dates()

print(notes)
print()
print(notes[3:7])
print()
print(notes[:(1900,1,1)])
