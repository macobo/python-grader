"""
Task description (in Estonian):

2. Töötajate arv (2p)
Kirjuta funktsioon töötajate_arv, mis võtab argumendiks info firma struktuuri
kohta ning tagastab firma töötajate arvu.

Firma struktuur on esitatud kaheelemendilise ennikuga, kus esimesel positsioonil
on juhi nimi ja teise positsioonil on list tema otseste alluvatega. Iga alluv on
esitatud samamoodi kaheelemendilise ennikuga – esimesel positsioonil on nimi ja
teisel positsioonil on tema otseste alluvate list, jne. 

Võib eeldada, hieararhias mingeid anomaaliaid ei ole, nt. keegi ei ole otseselt
ega kaudselt iseenda ülemus.

Näiteks, kui firma struktuur on

siis sellele vastav andmestruktuur oleks
('Toomas', [
    ('Anu', [('Kalle', []), ('Tõnu', []), ('Tiina', [])]),
    ('Heiki', [])
])

Sellise argumendiga peaks töötajate_arv tagastama 6."""

from KT2_util import *

def töötajate_arv(info):
    arv = 1
    for alluv in info[1]:
        arv += töötajate_arv(alluv)
    return arv

check = make_checker(töötajate_arv)
check(('Toomas', [
    ('Anu', [('Kalle', []), ('Tõnu', []), ('Tiina', [])]),
    ('Heiki', [])
]))
check(('Eno', []))
check(('Eno', [('Tiit', [])]))
check(('Eno', [('Tiit', []), ('Palle', []), ('Kalle', [])]))
check(('Eno', [('Tiit', []), ('Palle', []), ('Kalle', []), ('Malle', [])]))
check(('Eno', [('Tiit', [('Kadri', [])])]))

def osakond(suffix):
    return ('A'+suffix, [
        ('B'+suffix, []),
        ('C'+suffix, [('C1'+suffix, []), ('C2'+suffix, []), ('C3'+suffix, []), ('C4'+suffix, [])]),
        ('D'+suffix, [('D1'+suffix, [])]),
        ('E'+suffix, []),
        ('F'+suffix, []),
        ])
            
check(('Boss', [osakond('X'), ('Y', []), osakond('Z')]))
check(('Boss2', [osakond('X')]))
check((osakond('X')))
