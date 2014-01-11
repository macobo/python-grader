"""
Task description (in Estonian):

1. Poolte summa (4p)
Kirjuta funktsioon teine_pool_suurem, mis tagastab True, kui argumendiks antud
listi teise poole elementide summa on suurem kui listi esimese poole elementide
summa, vastasel juhul False. 

Kui listis on paaritu arv elemente, tuleks lugeda keskmine element listi esimese
poole hulka. 

Näiteks teine_pool_suurem([2, 3, -1, 4, 1]) peab tagastama True.
"""

from grader import *
from KT2_util import make_checker

def teine_pool_suurem(arr):
    kesk = len(arr) // 2
    if len(arr) % 2 == 1: kesk += 1
    return sum(arr[kesk:]) > sum(arr[:kesk])


checker = make_checker(teine_pool_suurem)

checker([2, 3, -1, 4, 1])
checker([2, 3, 1, 4, 1])
checker([2, 2, 2, 3])
checker([2, 2, 2, 2],
    description="Test, poolte summad võrdsed - {function}({args}) == {expected}")
checker([1, 2, 3, 4, 2],
    description="Test, poolte summad võrdsed - {function}({args}) == {expected}")
checker([2, 2, 2, 2, 2])
checker([10],
    description="Erijuht, tühja teise poole summa on 0 - {function}({args}) == {expected}")
checker([-10],
    description="Erijuht, tühja teise poole summa on 0 - {function}({args}) == {expected}")
checker([1.3, 3.2, 2.2, 2.3, 3.1, 1.4],
    description="Funktsioon peaks toime tulema ka ujukomaarvudega - {function}({args}) == {expected}")

randomTests = [
    [0, -17, 16, 10, -1, -13, -6],
    [5, 17, 16, 3, -14, -17, 18, -2],
    [17, -18, -16, 6, 13, 7, -13, -19, 18],
    [13, -12, -5, 12, -7, 10, -4, -3],
    [-18, -19, 17, -18, -18, -17, -11],
    [-3, -4, 16, -8, -9, -11],
    [-18, 18, -6, 3, 3, -4, 17, 14],
    [-7, 18, 12, 2, 0, 1, -18, 18]
]

for testdata in randomTests:
    checker(testdata)