"""
Task description (in Estonian):

3. Järgnevusmaatriks (5p)
Kirjuta funktsioon järgnevusmaatriks, mis võtab argumendiks kaks sõne a ja b ja
tagastab kahemõõtmelise listi e. maatriksi m, kus m[i][j], näitab, kuidas on
omavahel seotud sümbolid a[i] ja b[j]. Kui a[i] == b[j], siis m[i][j] peab olema
0, kui a[i] paikneb tähestikus b[j]'st eespool, siis m[i][j] peab olema -1,
vastasel juhul peab m[i][j] olema 1. 

Sümbolite võrdlemisel tuleb suur- ja väiketähtede erinevust ignoreerida, st 
'a' ja 'A' tuleb lugeda võrdseteks ning arvestame, et 'a' on enne 'B'-d ja 'A' 
on enne 'b'-d.

Näiteks järgnevusmaatriks("kala", "uba")
peab tagastama 
[[-1, 1, 1], [-1, -1, 0], [-1, 1, 1], [-1, -1, 0]]

Vihje:
    >>> 'a' < 'b'
    True
"""

from grader import *
from KT2_util import make_checker

# Taivo Pungas
def järgnevusmaatriks(a, b):
    # teeme maatriksi valmis
    output = []
    for i in range(0, len(a)):
        listike = []
        for j in range(0, len(b)):
            listike.append(0)
        output.append(listike)
        
    # täidame maatriksi
    for i in range(0, len(a)):
        ca = a[i].lower()
        for j in range(0, len(b)):
            cb = b[j].lower()
            #print("%s - %s" % (ca, cb))
            if(ca < cb):
                output[i][j] = -1
                #print("%s[%d] < %s[%d]" % (ca, i, cb, j))
            elif(ca > cb):
                output[i][j] = 1
                #print("%s[%d] > %s[%d]" % (ca, i, cb, j))
            else:
                output[i][j] = 0
                #print("%s[%d] = %s[%d]" % (ca, i, cb, j))


    return output

checker = make_checker(järgnevusmaatriks)
checker("kala", "uba")
checker("KALA", "uba")
checker("uba", "KALA")
checker("bbb", "abc")
checker("BBB", "abc")
checker("a", "Z")
checker("", "")