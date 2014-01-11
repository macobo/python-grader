"""
Task description (in Estonian):

2. Esimene ja viimane (3p)
Kirjuta funktsioon esimene_ja_viimane, mis võtab argumendiks listi, ning
tagastab sellise listi, kuhu on alles jäetud vaid algse listi esimene ja viimane
element, kui need olemas on. Tühja listi puhul tuleb tagastada koopia
argumendist. 

Kui esimene või viimane element on listid, siis tuleb ka neis vaid esimene ja
viimane element alles jätta jne. 

Võib eeldada, et kõikidel tasemetel olevates listides on paarisarv elemente.

Näide:
    >>> esimene_ja_viimane([1, 2, 3, 4, 5, 6])
    [1, 6]
    >>> esimene_ja_viimane([[1, 2, 3, [3, 3, 4, 5]], 6, 7, 7])
    [[1, [3, 5]],  7]
    >>> esimene_ja_viimane([[1, 2, 9, [3, 5]], []])
    [[1, [3, 5]],  []]

Vihje:
    >>> isinstance(123, list)
    False
    >>> isinstance([4,5], list)
    True
"""

from grader import *
from KT2_util import *

def esimene_ja_viimane(a):
    if not (isinstance(a,list)):
        return a
    elif a == []:
        return []
    else:
        return [esimene_ja_viimane(a[0]), esimene_ja_viimane(a[-1])]


    
check = make_checker(esimene_ja_viimane)
check([1, 2, 3, 4, 5, 6])
check([[1, 2, 3, [3, 3, 4, 5]], 6, 7, 7])
check([[1, 2, 9, [3, 5]], []])
check([[[], []], []])
check([])
check(['a','b'])
check(['a','b', 3, []])
check(['a','b', 3, [4, [], [], 'xasdf']])
