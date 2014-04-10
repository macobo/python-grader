"""
Task description (in Estonian):

2. Erinevus (4p)
Ülesandeks on kirjutada rekursiivne funktsioon erinevus, mis võtab argumendiks
kaks täisarvude listi ja tagastab nende põhjal koostatud kolmanda listi, mis
koosneb sellistest arvudest, mis esinevad esimeses argumentlistis aga ei esine
teises. Võib eeldada, et kummaski argumentlistis ei leidu korduvaid väärtusi.

Listioperatsioonidest on lubatud kasutada vaid indekseerimist, viilutamist,
funktsiooni len, elemendiks oleku kontrolli (operaatorit in) ja kahe listi
ühendamist (operaatorit +). Tsükleid kasutada ei või.

Näited:
    erinevus([1,2,3,4,5], [2,4]) peab tagastama [1, 3, 5]
    erinevus([1,2,3,4,5], [7,8]) peab tagastama [1, 2, 3, 4, 5]
    erinevus([1,2,3,4,5], [3,1,4,5,2]) peab tagastama []

Lihtsustus (-2p): võib kasutada ka tsüklit.
"""

from grader import *
from KT2_util import *

def erinevus(a, b):
    if a == []:
        return []
    elif a[0] in b:
        return erinevus(a[1:], b)
    else:
        return [a[0]] + erinevus(a[1:], b)


check = make_checker(erinevus)
check([1,2,3,4,5], [2,4])
check([1,2,3,4,5], [7,8])
check([1,2,3,4,5], [3,1,4,5,2])
check([1,2,3,4,5], [1,2,3,4,5])
check([1,2,3,4,5], [1,7,3,4,5])
check([],[])
check([],[-3,45])
check([-1], [])
check([3], [3])

l1 = [-30, 2, -28, 37, 38, 7, 9, 10, 39, 13, 19, 20, 21, 22, -7, -38, -4]
l2 = [0, 1, 3, 4, 6, 8, 9, 10, -2, -1]
l3 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -1, -2]

check(l1, l2)
check(l2, l1)
check(sorted(l2), sorted(l3))
check(sorted(l2)[::-1], sorted(l3))
check(sorted(l2)[::-1], sorted(l3)[::-1])


if __name__ == "__main__":
    from random import randint

    print(list(set([randint(-2,10) for _ in range(30)])))
