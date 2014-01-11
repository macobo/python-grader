"""
Task description (in Estonian):

1. Sõne laiendamine (5p)
Kirjuta funktsioon laienda, mis võtab argumendiks sõne ja sama pika 
naturaalarvulisti, ning tagastab uue sõne, kus igat esialgse sõne sümbolit on
korratud vastavalt samal positsioonil olevale arvule etteantud arvulistis.

Võib eeldada, et etteantud sõne ja listi pikkused on võrdsed.

Näide:
laienda("hernes", [1,2,0,3,1,1]) peab tagastama "heennnes".
"""

from grader import *
from KT2_util import make_checker

def laienda(sone, korduseid):
    assert(len(sone) == len(korduseid))
    return "".join(taht * x for taht, x in zip(sone, korduseid))


checker = make_checker(laienda)

checker("hernes", [1, 2, 0, 3, 1, 1])
checker("KaPsa hautis ", [3, 4, 1, 1, 0, 5, 1, 2, 1, 2, 1, 2, 1])
checker("T", [5])
checker("a", [0])
checker("TeReMaaIlm", list(range(10, 20)))
checker("", [],
    description="Erijuht, tühi sõne - {function}({args}) == {expected}")