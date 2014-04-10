"""
Task description (in Estonian):

3. Korduvate summa (5p)

Kirjuta funktsioon korduvate_summa, mis võtab argumendiks täisarvujärjendi ja
tagastab selliste arvude summa, mis esinevad antud järjendis rohkem kui üks kord,
kusjuures korduv element tuleb arvesse võtta nii mitmes eksemplaris, nagu teda
järjendis esineb. 

Näide: korduvate_summa([1, 0, -4, 2, 3, 5, -5, 2, -2, 5, 1, 5, 4]) peab
tagastama 21, sest arvud, mis esinevad näidatud jadas rohkem kui üks kord on
1, 2, 5 ja 1 + 1 + 2 + 2 + 5 + 5 + 5 = 21. 
"""

from grader import *
from KT2_util import make_checker
from random import *

def korduvate_summa(array):
    return sum(filter(lambda x: array.count(x) > 1, array))

def rand_count(length, _seed=None, N = None):
    seed(_seed)
    if N is None: N = max(int(length / 5), 2)
    return [randint(-N, N) for _ in range(length)]

checker = make_checker(korduvate_summa)

checker([1, 1, 1, 1])
checker([1, 1, 1, 1, 2, 2, 3])
checker([1, 0, -4, 2, 3, 5, -5, 2, -2, 5, 1, 5, 4])
checker([],
    description="Erijuht, tühi järjend - {function}({args}) == {expected}")
checker([1, 2, 3, 4],
    description="Erijuht, korduvaid pole - {function}({args}) == {expected}")

for i in range(5):
    checker(rand_count(20, i))