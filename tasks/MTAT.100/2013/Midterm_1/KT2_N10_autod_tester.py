"""
Task description (in Estonian):

2. Autode andmed (10p)
Failis autod.zip on tekstifail autod.csv (kodeeringus UTF-8), kus on Eestis 
registreeritud autode arvud auto margi, tehniliste näitajate, väljalaskeaasta ja
maakonna järgi. 

Kirjuta programm, mis küsib kasutajalt aastanumbri ja väljastab ekraanile 
automargi ja mudeli, mida sel aastal väljalastud autode hulgas esineb kõige 
sagedamini. NB! Väljastada tuleb ainult mark ja mudel, mis on omavahel tühikuga
eraldatud nt. Opel Kadett.

Kui antud väljalaskeaastaga autosid ei leidu, siis tuleb väljastada tekst Ei leidu.

Kui antud aasta kohta on andmetes mitu kõige populaarsemat automudelit, siis 
tuleb väljastada neist ainult üks (vabal valikul).

NB! Soovitame programmi esialgu testida väiksema failiga (autod_vaiks em.csv, so.
sama struktuuri ja kodeeringuga nagu autod.csv).
"""

from grader import *
from KT2_util import *

def car_choices(yearno, filename):
    counts = {}
    with open(filename, encoding="utf-8") as f:
        f.readline()
        for line in f:
            parts = line.split(';')
            mark, model, count, year = parts[1], parts[2], int(parts[8]), int(parts[4])
            if year != yearno: continue
            if (mark, model) not in counts:
                counts[mark, model] = 0
            counts[mark, model] += int(count)
    if not counts: return set()
    best = max(counts.values())
    return set(a+" "+b for (a, b), value in counts.items() if value == best)

def checker(yearno, filename="_autod_vaiksem.csv", description=None):
    if description is None:
        description = "Fail {filename}, aasta {year} on üks järgnevatest: {result}"
    expected = car_choices(yearno, filename)
    if not expected:
        expected = set(["Ei leidu"])

    description = description.format(
        filename = filename,
        year = yearno,
        result = expected)

    contents = open(filename).read()

    @test
    @create_temporary_file('autod.csv', contents)
    @create_temporary_file('autod_vaiksem.csv', contents)
    @timeout(3)
    def test_function(m):
        m.stdout.reset() # ignore year query
        m.stdin.write(yearno)
        assertOneContains(m.stdout.read(), expected)

    setDescription(test_function, description)

checker(20000)
checker(2004)
for i in range(1990, 2010):
    checker(i)

checker(2005, '_autod.csv', "Suur test - fail {filename}, aasta {year} on üks järgnevatest: {result}")
checker(2000, '_autod.csv', "Suur test - fail {filename}, aasta {year} on üks järgnevatest: {result}")