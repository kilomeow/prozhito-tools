# Installation

Just go with
`git clone https://github.com/destabilizer/prozhito-tools`

# Usage
Start with loading dump
```
import dump
dw = dump.Wrapper(csvpath='/path/to/prozhito-dump/')
```

Then you have access to prozhito tables, for example to notes
```
dw.notes
```
*Output:*
> [ #463400 "Воскресенье. Вчера приехал..." @2950 [0-0-0] ,
>   #465445 "Ночью мы достигли..." @2268 [0-0-0] ,
>   #430743 "Суббота. Москва. Еду..." @795 [0-12-21] ,
>   ... ,
>   #31036 "a..." @82 [2959-3-9] ]

You can take slices of your notes 
```
august_notes = dw.notes[(1991, 8, 1) : (1991, 8, 31)]
august_notes
```
> [ #62200 "Четверг. Буш сегодня..." @320 [1991-8-1] ,
>   #112334 "Депутаты на каникулах...." @437 [1991-8-1] ,
>   #368278 "в поезде. Я,..." @967 [1991-8-1] ,
>   ... ,
>   #365647 "Суббота. Лена с..." @1060 [1991-8-31] ]

The slice is notes object again, so we can take slices again and take
elements via key.
```
august_notes[18]
```
> #186927 "Не поспеваю за..." @559 [1991-8-4]

We can inspect note, e.g. read the whole text
```
august_notes[18].text
```
> 'Не поспеваю за жизнью! Брокеры, дилеры, что там еще? Когда успелось? 
> Умер Каганович. 97 лет. Безобидный старичок в доме на Фрунзенской
> набережной. Выписывал газеты. Пенсия 150 р. В последний год стал
> понемногу принимать репортеров.'

Also any notes object could be saved to csv file via
dump method.
```
august_notes.dump('aug91.csv')
```
And we will get `aug91.csv` file in current directory.
