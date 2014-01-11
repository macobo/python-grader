"""
Task description (in Estonian):

3. Korrutustabel (5p)
Kirjuta funktsioon korrutustabel, mis võtab argumendiks kaks arvulisti a ja b 
ning tagastab listide listina neile vastava korrutustabeli, kus esimene rida
koosneb arvudest, mis on saadud listi a esimese elemendi korrutamisel listi b
elementidega, teisel real on listi a teise elemendi korrutised listi b
elementidega jne. 

Näide: 
korrutustabel([5,2,8,4], [2,4,1]) 
peab tagastama 
[[10, 20, 5], [4, 8, 2], [16, 32, 8], [8, 16, 4]]
"""

from KT2_util import make_checker

def korrutustabel(A, B):
    tulemus = []
    for a in A:
        r = []
        for b in B:
            r.append(a * b)
        tulemus.append(r)
    return tulemus


checker = make_checker(korrutustabel)

checker([], [])
checker([1], [5])
checker([10], [2, 5, 10])
checker([2, 5, 10], [3, 33])
checker([0.5, 2.5, 7.125, 9.5, 0.0], [3, 33, 55, 99, 22], 
        description="Erijuht, ei tohiks kasutada round, int tegemist) - {function}({args}) == {expected}")
