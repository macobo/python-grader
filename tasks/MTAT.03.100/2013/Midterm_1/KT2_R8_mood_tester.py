"""
Task description (in Estonian):

3. Arvude mood (5p)
Kirjuta funktsioon mood, mis võtab argumendiks täisarvujärjendi ja tagastab arvu,
mida leidub järjendis kõige rohkem (ehk moodi). Kui selliseid arve on mitu, siis
tuleb tagastada neist vähim.  

Näide: mood([-10, 17, 13, 17, -10, 21]) peab tagastama -10. 
"""

from grader import *
from KT2_util import make_checker
from random import *

def mood(lst):
    parim = 0
    parim_count = 0
    for el in lst:
        count = 0
        for a in lst:
            if a == el:
                count += 1
        if count > parim_count or (count == parim_count and el < parim):
            parim = el
            parim_count = count
    return parim

def rand_count(length, _seed=None, N = None):
    seed(_seed)
    if N is None: N = max(int(length / 5), 2)
    return [randint(-N, N) for _ in range(length)]

checker = make_checker(mood)

checker([1])
checker([1, 1, 1, 3])
checker([1, 2, 2, 3, 2, 1, -2, 3])
checker([-10, 17, 13, 17, -10, 21],
    description="Erijuht, võrdsete esinemiste arvu korral tagasta vähim - {function}({args}) == {expected}")
checker([17, -10, 13, -10, 17, 21],
    description="Erijuht, võrdsete esinemiste arvu korral tagasta vähim - {function}({args}) == {expected}")


for i in range(5):
    checker(rand_count(20, i))