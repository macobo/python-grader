"""
Task description (in Estonian):

1. Paarikaupa keskmised (5p)
Kirjuta funktsioon keskmised, mis võtab argumendiks täisarvude listi ja tagastab
listi, mis koosneb algse listi kõrvutiolevate elementide keskmistest.

Näiteks keskmised([2, 3, 6, 2, 5]) peab tagastama [2.5, 4.5, 4.0, 3.5]
"""

from grader import *
from KT2_util import make_checker
from random import *

def rand_count(length, _seed=None, N = None):
    seed(_seed)
    if N is None: N = max(int(length / 5), 2)
    return [randint(-N, N) for _ in range(length)]

def keskmised(jarjend):
    output = []
    for i in range(0,len(jarjend)):
        if i != len(jarjend) - 1:
            output.append(0.5 * (jarjend[i] + jarjend[i+1]))
    return output

checker = make_checker(keskmised)

checker([1, 1])
checker([300, 400])
checker([20, 21])
checker([1, 1, 3, 5, 9])
checker([1, 2, 30, 500])
checker([2.5, 1.5, 0.5, 0], 
    description="Erijuht, ei tohiks kasutada round'i - {function}({args}) == {expected}")
checker([], 
    description="Erijuht, järjend tühi - {function}({args}) == {expected}")
checker([1],
    description="Erijuht, järjendis 1 element - {function}({args}) == {expected}")

for i in range(3):
    checker(rand_count(20, i))