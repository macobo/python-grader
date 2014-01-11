"""
Task description (in Estonian):

1. Korduvad tähed (5p)
Kirjuta funktsioon loenda, mis võtab argumendiks sõne ja tagastab arvulisti, kus
iga element tähistab ühte lõiku antud sõnes, kus kõik tähed on samad. Elemendi
väärtus näitab, mitmest samasugusest sümbolist antud lõik koosnes.

Näide:
loenda("kaaapsauusssss") peab tagastama [1, 3, 1, 1, 1, 2, 5].
"""

from grader import *
from KT2_util import make_checker
from random import *
from string import *

def loenda(sone):
    if sone == "":
        return []
    tulemus = []
    count = 0
    prev_taht = sone[0]
    for taht in sone:
        if taht == prev_taht:
            count += 1
        else:
            tulemus.append(count)
            count = 1
            prev_taht = taht
    tulemus.append(count)
    return tulemus

def suvaline_sona(length, _seed=None):
    seed(_seed)
    return "".join(choice(ascii_lowercase) * randrange(1, 20) for _ in range(length))

checker = make_checker(loenda)

checker("tere")
checker("ttttt")
checker("kaaapsauussssss")
checker("3332219999999994444")
checker("", description="Erijuht, tühi sõne - {function}({args}) == {expected}")

for i in range(4):
    checker(suvaline_sona(10, i))