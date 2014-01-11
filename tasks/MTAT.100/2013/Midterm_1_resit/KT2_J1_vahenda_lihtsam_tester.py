"""
Task description (in Estonian):

3. Alternatiivne, lihtsam variant (-2p)
Lihtsama variandi valimisel tuleb funktsiooni nimeks panna vähenda_lihtsam.
Siin esialgse ülesandega võrreldes erinevus selles, et tulemusmaatriksi
elemendid on lihtsalt esialgse maatriksi 4-elemendiliste plokkide ülemised,
vasakpoolsed elemendid:

See tähendab, et 
    vähenda_lihtsam([
        [1,5,2,6,3,6], 
        [1,3,2,7,3,3], 
        [4,8,5,1,1,6], 
        [4,4,9,5,6,1]
    ]) 
peab tagastama
    [[1, 2, 3], 
     [4, 5, 1]].
"""

from grader import *
from KT2_util import make_checker

def vähenda_lihtsam(maatriks):
    return [[maatriks[r][c] for c in range(0, len(maatriks[r]), 2)] for r in range(0, len(maatriks), 2)]

checker = make_checker(vähenda_lihtsam)

checker([[1, 2], [3, 4]],
    description="Ruudukujuline 2x2 maatriks- {function}({args}) == {expected}")
checker([[1, 2, 3, 4], [5, 6, 7, 8]],
    description="Mitte-ruudukujuline maatriks - {function}({args}) == {expected}")
checker([[1,5,2,6,3,6], [1,3,2,7,3,3], [4,8,5,1,1,6], [4,4,9,5,6,1]])
checker([[1,5,2,6,3,6], [1,3,2,7,3,3], [4,8,5,1,1,6], [4,4,9,5,6,1]])
checker([], 
    description="Erijuht, tühi maatriks- {function}({args}) == {expected}")

random_tests = [
    [[7, 5, 2, 6, 6, 9], [2, 8, 6, 3, 8, 7]],

    [[3, 1, 0, 9], [0, 5, 1, 7]],

    [[4, 4], [0, 8], [4, 9], [3, 0], [3, 6], [8, 2]],

    [[9, 4, 6, 5, 4, 6],
    [3, 8, 7, 1, 2, 5],
    [8, 9, 8, 5, 0, 2],
    [2, 7, 2, 4, 3, 5],
    [2, 6, 8, 0, 2, 9],
    [7, 4, 6, 4, 8, 2]],

    [[-1, -3], [-6, 6], [5, -6], [1, 0]],

    [[-5, -10, 6, -1], [-8, -10, -5, 7], [-7, 9, -5, -5], [-8, -7, -10, 8]],

    [[-3, 6, -3, 6], [4, -6, 3, 8], [-9, -6, 7, -6], [6, 6, 4, -3]],

    [[1, 6], [2, -6]]
]

for test_case in random_tests:
    checker(test_case)