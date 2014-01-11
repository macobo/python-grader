"""
Task description (in Estonian):

3. Lapsevanemad (11p)
Failis nimed.txt on igal real ühe inimese isikukood, tühik ja tema nimi. 
Võib eeldada, et korduvaid nimesid failis ei esine.

Failis lapsed.txt on igal real vanema isikukood, tühik ja lapse isikukood. Võib
eeldada, et iga failis lapsed.txt oleva isikukoodi jaoks on faili nimed.txt
välja toodud vastav nimi.

Kirjutada programm, mis nende failide põhjal koostab muutujasse lapsevanemad
sõnastiku, kus kirje võtmeks on lapsevanema nimi ja väärtuseks tema laste nimede
hulk. 

Faili nimed.txt põhjal loodud sõnastik peaks olema:
    {'Madli Peedumets': {'Robert Peedumets', 'Maria Peedumets'},
     'Peeter Peedumets': {'Robert Peedumets', 'Maria Peedumets'},
     'Kadri Kalkun': {'Liisa-Maria Jaaniste'},
     'Karl Peedumets': {'Peeter Peedumets'}}


Saadud sõnastiku põhjal tuleb väljastada ekraanile iga lapsevanema kohta üks
rida: tema nimi, koolon, tühik ning seejärel komade ja tühikutega eraldatuna
tema laste nimed.

Eespool toodud näitesõnastiku korral peaks ekraanile ilmuma järgnevad read
(lapsevanemate ega nende laste järjekord pole seejuures tähtis):
    Madli Peedumets: Robert Peedumets, Maria Peedumets
    Peeter Peedumets: Robert Peedumets, Maria Peedumets
    Kadri Kalkun: Liisa-Maria Jaaniste
    Karl Peedumets: Peeter Peedumets

Vihje:
    >>> "---".join({"kapsas", "uba", "hernes"})
    'kapsas---uba---hernes'

"""

from grader import *

def description(d):
    def inner(f):
        setDescription(f, d)
        return f
    return inner

def solution(nimede_fail, laste_fail):
    f = open(nimede_fail)
    nimed = {}
    for rida in f:
        osad = rida.split(maxsplit=1)
        nimed[osad[0]] = osad[1].strip()

    f.close()

    f = open(laste_fail)
    lapsevanemad = {}

    for rida in f:
        osad = rida.split()
        vanema_nimi = nimed[osad[0]]
        if not vanema_nimi in lapsevanemad:
            lapsevanemad[vanema_nimi] = set()

        lapsevanemad[vanema_nimi].add(nimed[osad[1]])

    return lapsevanemad

def my_split(text, separator, strict):
    if strict:
        return text.split(separator)
    else:
        parts = text.split(separator.strip())
        for i in range(len(parts)):
            parts[i] = parts[i].strip()
        return parts

def parse_output(txt, strict):
    """annab programmi väljundi põhjal vanemate sõnastiku,
    sellisel kujul, nagu ülesanne eespool nõudis"""
    
    read = txt.strip().splitlines()
    vanemad = {}
    for rida in read:
        osad = my_split(rida, ": ", strict)
        assert len(osad) == 2, (
            "Formaadi viga reas {}.\n"
            "\nKogu väljund:\n{}"
            .format(repr(rida), txt))
        vanema_nimi = osad[0]
        if osad[1].strip() != '':
            laste_nimed = my_split(osad[1], ", ", strict)
        else:
            laste_nimed = []
        assert len(laste_nimed) <= len(set(laste_nimed)), (
            "Reas {} laste nimed korduvad"
            "\nKogu väljund:\n{}"
            .format(repr(rida), txt))
        
        vanemad[vanema_nimi] = set(laste_nimed)

    return vanemad


VARIABLE = "muutuja 'lapsevanemad' kontroll"
STRICT_OUTPUT = "väljundi range kontroll"
SOFT_OUTPUT = "väljundi leebem kontroll (eraldajate järel ei pea olema tühikut)"

def make_test(nimede_fail, laste_fail, mode):
    
    @description("Nimede fail: {0}, laste_fail: {1}, režiim: {2}"
                 .format(nimede_fail, laste_fail, mode))
    @test
    @create_temporary_file('nimed.txt', open(nimede_fail).read())
    @create_temporary_file('lapsed.txt', open(laste_fail).read())
    def out_test(m):
        assert hasattr(m, 'module'), "Programmi täitmine ei lõppenud. Arvatavasti ootab sisendit"
                                                                                                 
        if mode == VARIABLE:
            assert hasattr(m.module, "lapsevanemad"), "Ei leidnud muutujat 'lapsevanemad'"
            sõnastik = m.module.lapsevanemad
        else:
            väljund = m.stdout.read()
            sõnastik = parse_output(väljund, mode == STRICT_OUTPUT)
            
        õige_sõnastik = solution(nimede_fail, laste_fail)
        if sõnastik != õige_sõnastik:
            raise AssertionError("Vastus erineb oodatust:\nSaime: {0}\nOotasime: {1}".format(sõnastik, õige_sõnastik))
        
        
make_test("KT3_N10_3_nimed.txt", "KT3_N10_3_lapsed.txt", VARIABLE)
make_test("KT3_N10_3_nimed.txt", "KT3_N10_3_lapsed.txt", STRICT_OUTPUT)
make_test("KT3_N10_3_nimed.txt", "KT3_N10_3_lapsed.txt", SOFT_OUTPUT)
make_test("KT3_N10_3_random_nimed_0.txt", "KT3_N10_3_random_lapsed_0.txt", VARIABLE)
make_test("KT3_N10_3_random_nimed_1.txt", "KT3_N10_3_random_lapsed_1.txt", VARIABLE)
make_test("KT3_N10_3_random_nimed_2.txt", "KT3_N10_3_random_lapsed_2.txt", VARIABLE)