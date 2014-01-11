"""
Task description (in Estonian):

1. Prinditavad leheküljed (5p)
Kirjuta funktsioon leheküljenumbrid, mis võtab argumendiks täisarvude listi,
milles on paarisarv elemente ja mis paarikaupa tähistavad leheküljenumbrite
intervalle. Esimesel, kolmandal jne. kohal on intervallide algused, järgmisel (teisel, 
neljandal jne.) kohal on vastava intervalli lõpp. 

Võib eeldada, et ühegi paari puhul pole paari teine komponent esimesest väiksem.
Samuti võib eeldada, et intervallidel ei ole ühiseid elemente. 
Funktsioon peab tagastama uue listi, mis sisaldab kõiki leheküljenumbreid, mis
sisalduvad näidatud intervallides. Numbrite järjekord peab vastama etteantud
intervallide järjekorrale. NB! Iga üheleheküljelise intervalli (nt. ...,1,1,...)
kohta peab tulemuslistis olema ainult üks leheküljenumber!

Näide:
leheküljenumbrid([1, 1, 2, 5, 13, 15, 9, 10]) peab tagastama 
leheküljenumbrid 1..1, 2..5, 13..15 ja 9..10, st 
[1, 2, 3, 4, 5, 13, 14, 15, 9, 10].
"""

# TODO: Add a test confirming the function even exists
#       Notify if function test fails because some error was caught in blah.
from grader import *
from KT2_util import function_test

def leheküljenumbrid(a):
    tulemus = []
    for j in range(len(a)//2):
        i = j * 2
        for x in range(a[i], a[i+1]+1):
            tulemus.append(x)

    return tulemus


def checker(numbers):
    function_test('leheküljenumbrid', [numbers], leheküljenumbrid(numbers))

checker([])
checker([1, 1])
checker([1, 6])
checker([1, 5, 5, 10])
checker([1, 1, 2, 5, 13, 15, 9, 10])
checker([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 9, 9])