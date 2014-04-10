"""
Task description (in Estonian):

2. Eurole üleminek (10p)
Kuna Läti läheb 1. jaanuaril 2014 üle eurole, siis on vaja koostada programm,
mis konverteerib failis kontod.txt olevad LVL-kontod eurokontodeks. Kui samal
inimesel on raha mitmes erinevas valuutas, siis on see välja toodud erinevatel
ridadel. Kui inimesel on nii LVL-konto, kui eurokonto, tuleks latid
konverteerida eurodeks ning liita saadud summa tema eurokontole. Lõpusumma tuleb
ümardada 2 komakohani.

Andmed uute kontoseisude kohta tuleb kirjutada faili uued_kontod.txt

Teisendused tuleb teha järgneva kursiga: 1 EUR = 0.702804 LVL

Fail kontod.txt:
    Valdis Birkavs: EUR 1700.0
    Guntars Krasts: LVL 1900.0
    Ivars Godmanis: USD 1600.0
    Valdis Birkavs: LVL 3200.0
    Ivars Godmanis: LVL 1600.0
    Valdis Birkavs: USD 1000.0

Programmi käivitamisel peaks tekkima uus fail uued_kontod.txt, milles on
järgnevad read (võivad olla teises järjekorras):
    Ivars Godmanis: USD 1600.0
    Guntars Krasts: EUR 2703.46
    Valdis Birkavs: USD 1000.0
    Ivars Godmanis: EUR 2276.59
    Valdis Birkavs: EUR 6253.19

Võimalik lihtsustus (-2p): Muuda algset faili kontod.txt nii et, alles jäävad
ainult EUR ja LVL kontod.
"""

# Tricky parts to test - rounding errors by rounding at the wrong time!

from grader import *
from KT2_util import *

def create_text(accounts):
    return "\n".join("{}: {} {}".format(a, b, round(c, 2)) for a, b, c in accounts)

def after_conversion(accounts):
    sums = {}
    for name, type, s in accounts:
        s = float(s)
        if type == "LVL":
            s = s / 0.702804
            type = "EUR"
        if (name, type) not in sums:
            sums[name, type] = 0.0
        sums[name, type] += s
    return [(name, type, round(sum, 2)) for (name, type), sum in sums.items()]

BASE_TEMPLATE = "Algsed kontod: {accounts}, oodatav tulemus: {result_accounts}"
def checker(accounts, description = None):
    if description is None:
        description = BASE_TEMPLATE

    expected = after_conversion(accounts)
    expected_lines = [create_text([acc]) for acc in expected]
    description = description.format(accounts=accounts, result_accounts=expected)

    @test
    @create_temporary_file('kontod.txt', create_text(accounts))
    @after_test(delete_file('uued_kontod.txt'))
    def test_function(m):
        #from time import sleep
        #assert False, [open('kontod.txt').read()]
        import os
        assert os.path.exists('uued_kontod.txt'), "Lahendus peab looma faili uued_kontod.txt"
        with open('uued_kontod.txt') as f:
            contents = f.read()
        #assert False, contents.split("\n")
        #assert contents, [contents]
        lines = list(filter(lambda x:x, contents.split("\n")))
        for line in lines:
            assertOneContains(line, expected_lines)
        assert len(lines) == len(expected_lines), "{S}/{O}Ridade arv failis ei klapi, saime: {lines}, ootasime {expected_lines}".format(S=len(lines), O=len(expected_lines), lines=lines, expected_lines=expected_lines)
    setDescription(test_function, description)


checker([("MingiNimi Perenimi", "EUR", 30.0)])
checker([("Muunimi Perenimi", "LVL", 30.0)])
checker([("Troll A", "USD", 50.0)], description="Eritüüpi konto jäetakse alles. "+BASE_TEMPLATE)
checker([("Voll B", "EEK", 50.0)], description="Eritüüpi konto jäetakse alles. "+BASE_TEMPLATE)

checker([("Mart Sander", "EUR", 90.0), ("Mart Sander", "LVL", 30.0)],
    description="Mitu kontot samal nimel. "+BASE_TEMPLATE)
checker([("ABC E", "EUR", 33.5)], description="Tavalisel konverteerimisel ei tohiks int() kasutada. "+BASE_TEMPLATE)
checker([("efg H", "LVL", 33.5)], description="LVL konverteerimisel ei tohiks int() kasutada. "+BASE_TEMPLATE)

checker([("Valdis Birkavs", "EUR", 1700.0),
        ("Guntars Krasts", "LVL", 1900.0),
        ("Ivars Godmanis", "USD", 1600.0),
        ("Valdis Birkavs", "LVL", 3200.0),
        ("Ivars Godmanis", "LVL", 1600.0),
        ("Valdis Birkavs", "USD", 1000.0)])

checker([("MingiNimi", "EUR", 40.0)], description="Nimi ei pea olema kaheosaline. "+BASE_TEMPLATE)
checker([("Jaanika Maarika Mardikas", "EUR", 40.0)], description="Nimi ei pea olema kaheosaline. "+BASE_TEMPLATE)

checker([], description="Erijuht, fail tühi")

checker([("Mart Sander", "LVL", 1.0),
         ("Mart Sander", "LVL", 1.0)],
        description="Erijuht, ühel inimesel mitu LVL kontot, ümardatakse liiga vara. "+BASE_TEMPLATE)