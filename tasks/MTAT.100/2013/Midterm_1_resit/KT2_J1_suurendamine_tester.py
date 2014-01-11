"""
Task description (in Estonian):

"""

from grader import *
from KT2_util import make_checker

def suurenda(maatriks): # kole kood
    tulemus = []
    for rida in maatriks:
        uus_rida = []
        for element in rida:
            uus_rida.append(element)
            uus_rida.append(element)
        tulemus.append(uus_rida)
        tulemus.append(uus_rida)
    return tulemus

checker = make_checker(suurenda)

checker([[1,2,3], [4,5,6]])
checker([[]])
checker([[1]])

checker([[1,2.5,3], [5, 3, 1], [4, 4, 1] ])

random_tests = [
    [[1, 8]],
    [[2]],
    [[4, 2], [1, 4]],
    [[8, 6]],
    [[5, 6, 8, 6], [3, 3, 1, 2], [2, 2, 7, 1], [6, 4, 9, 3]],
    [[5, 5, 3], [7, 8, 2], [9, 7, 3]]
]

for test_case in random_tests:
    checker(test_case)