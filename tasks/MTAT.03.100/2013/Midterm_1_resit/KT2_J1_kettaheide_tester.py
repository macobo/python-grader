"""
Task description (in Estonian):

2. Kettaheide (10p)
1) Kirjuta funktsioon parimad_katsed, mis võtab argumendiks sõnastiku, kus 
võtmeks on kettaheitja nimi ja väärtuseks list tema edukate katsete tulemustega.
Funktsioon peab tagastama sellele sõnastikule vastava paaride hulga, kus iga
paari esimene element on sportlase nimi ja teine element tema parima katse
tulemus. 

Võib eeldada, et igal kettaheitjal on listis vähemalt üks tulemus.

Näiteks:
    parimad_katsed({
        'Peeter Pihlakas' : [12.4, 22.12], 
        'Gerd Kanter': [64.93, 66.24, 68.03]
    }) 
    peab tagastama {('Peeter Pihlakas', 22.12), ('Gerd Kanter', 68.03)}.

2) Programmi põhiosas tuleb küsida kasutajalt failinimi, ning lugeda seal olevad
kettaheite võistluse tulemused eelpool näidatud kujul olevasse sõnastikku. 
Võib eeldada, et fail on üles ehitatud samamoodi nagu Moodle'is olev fail
kettaheide.txt – st. iga võistleja nime järel tuleb eraldi ridadel tema 3 katse
andmed. 

Ebaõnnestunud katsed on märgitud sümboliga X - neid tuleb edukate katsete listi
koostamisel ignoreerida. Võib eeldada, et iga võistleja kohta on failis vähemalt
üks edukas katse. Saadud sõnastik tuleb salvestada muutujasse nimega tulemused. 

3) Kasutades eelpool defineeritud funktsiooni, tuleb selgitada välja iga
võistleja parima katse tulemus, ning väljastada see ekraanile. Viimasel real
tuleb väljastada info võistluse võitja ja teise koha omaniku kohta.

Võib eeldada, et parim tulemus esineb vaid ühel võistlejal ja ka paremuselt
teine tulemus esineb vaid ühel võistlejal. Väljund tuleb vormistada järgneva
näitesessiooni järgi (genereeritud faili kettaheide.txt põhjal, kasutaja sisend
on kursiivis, võistlejate järjekord ei ole tähtis):

    Sisesta failinimi: kettaheide.txt
    Gerd Kanter: 68.03
    Lawrence Okoye: 61.03
    Erik Cadee: 62.78
    Ehsan Hadadi: 68.18
    Virgilijus Alekna: 67.38
    Robert Harting: 65.13
    Parim oli Ehsan Hadadi
    Teine oli Gerd Kanter


Võimalikud lihtsustused:
Faili kettaheide.txt asemel loetakse andmed sisse failist kettaheide2.txt (-1p)
Teise koha omanikku ei arvutata (-1p)
Andmefailis asendatakse ebaõnnestunud katse märgid käsitsi tulemusega 0 (-1p)
Programm annab ekraanile korrektse tulemuse, aga puuduvad punktides 1 ja 2 
nõutud definitsioonid (-3p)
"""

from grader import *
from KT2_util import *

testSets = {
    "näide": {
        'Ehsan Hadadi': [67.94, 66.47, 68.18],
        'Erik Cadee': ['X', 62.78, 60.41],
        'Gerd Kanter': [64.93, 66.24, 68.03],
        'Lawrence Okoye': [59.6, 61.03, 60.87],
        'Robert Harting': [64.21, 65.13, 'X'],
        'Virgilijus Alekna': [67.38, 'X', 'X']
    },
    "näide-edukas": {
        'Ehsan Hadadi': [67.94, 66.47, 68.18],
        'Erik Cadee': ['X', 62.78, 60.41],
        'Gerd Kanter': [64.93, 66.24, 68.03],
        'Lawrence Okoye': [59.6, 61.03, 60.87],
        'Robert Harting': [64.21, 65.13, 60.30],
        'Virgilijus Alekna': [67.38, 66.30, 65.20]
    },
    "ainult-edukad-katsed": {
        'Al Oerter': [68.76, 67.9, 69.46],
        'Aleksander Tammert': [70.82, 67.93, 68.48],
        'Andy Bloom': [67.46, 67.32, 67.25],
        'Anthony Washington': [69.08, 71.14, 68.94],
        'Art Burns': [71.18, 70.98, 69.88],
        'Art Swarts': [69.4, 68.32, 67.28],
        'Ben Plucknett': [71.32, 70.82, 71.14],
        'Ehsan Hadadi': [69.32, 69.12, 68.52],
        'Erik de Bruin': [67.5, 67.58, 67.16],
        'Frank Casañas': [67.74, 67.91, 67.25],
        'Frantz Kruger': [69.96, 70.32, 69.97],
        'Gejza Valent': [68.36, 69.36, 67.9],
        'Georgiy Kolnootchenko': [68.98, 69.44, 69.08],
        'Gerd Kanter': [72.02, 73.38, 71.88],
        'Ian Waltz': [68.9, 67.85, 67.98],
        'Imrich Bugár': [70.26, 71.26, 70.72],
        'Jarred Rome': [67.76, 68.37, 68.44],
        'John Godina': [69.05, 69.91, 68.32],
        'John Powell': [69.98, 69.08, 71.26],
        'Juan Martinez Brito': [70.0, 69.32, 68.4],
        'Jürgen Schult': [70.46, 74.08, 69.74],
        'Ken Stadel': [69.26, 68.4, 67.9],
        'Knut Hjeltnes': [69.62, 68.9, 69.5],
        'Lars Riedel': [70.6, 71.5, 71.06],
        'Luis Mariano Delís': [71.06, 70.2, 70.0],
        'Mac Wilkins': [70.98, 70.86, 70.66],
        'Mario Pestano': [68.34, 69.5, 68.61],
        'Markku Tuokko': [67.5, 67.98, 67.78],
        'Michael Möllenbeck': [67.42, 67.64, 67.2],
        'Mike Buncic': [68.88, 68.98, 68.92],
        'Piotr Malachowski': [71.84, 69.83, 69.15],
        'Richard Bruch': [71.0, 71.26, 70.48],
        'Robert Harting': [69.91, 69.75, 70.66],
        'Rolf Danneberg': [67.38, 67.52, 67.38],
        'Romas Ubartas': [68.56, 68.18, 68.22],
        'Róbert Fazekas': [70.83, 71.25, 71.7],
        'Svein Inge Valvik': [68.0, 67.9, 67.7],
        'Vaclovas Kidykas': [68.44, 67.9, 67.54],
        'Virgilijus Alekna': [71.56, 71.25, 73.88],
        'Wolfgang Schmidt': [71.16, 70.92, 70.24],
        'Yuriy Dumchev': [71.86, 70.3, 69.16] 
    }
}

SAFE_DATA_SET = testSets["näide-edukas"]

# test-related
def file_contents_normal(test_data):
    return "\n".join(name + " : " + "; ".join(map(str,values)) for name, values in test_data.items())

def file_contents_simple(test_data):
    return "\n".join(name + "\n" + "\n".join(map(str, values)) for name, values in test_data.items())

def without_failures(test_data):
    return dict((name, filter(lambda x: isinstance(x, float), values)) for name, values in test_data.items())

def maximals(test_data):
    return dict((name, max(values)) for name, values in without_failures(test_data).items())

def best(test_data):
    results = maximals(test_data)
    return sorted(test_data.keys(), key=lambda k: results[k], reverse=True)[:2]

# test parts
def enter_filename(filename):
    def inner(m):
        m.stdout.reset()
        m.stdin.write(filename)
    return inner

def checkfunction_exists(function_name):
    def inner(m):
        assert hasattr(m, 'module'), "Programmi täitmine ei lõppenud. Failis ei tohiks olla ülearuseid input() käske"
        assert hasattr(m.module, function_name), "Peab leiduma funktsioon nimega {name}!".format(name=function_name, dict=m.module.__dict__)

def check_function_results(function_name, args, expected):
    args_str = ", ".join(map(repr, args))
    def inner(m):
        function = getattr(m.module, function_name)
        result = function(*args)
        assertEquals(result, expected,
            "{function_name}({args_str}) peaks tagastama {expected} aga tagastas {result}",
            expected=expected,
            result=result,
            function_name=function_name,
            args_str=args_str)
    return inner

def checker(test_set, test_set_name):
    EMPTY = lambda x: x
    create_file_dec = create_temporary_file('kettaheide.txt', file_contents_normal(test_set))

    # parimad_katsed test_data peal, iosse läheb näiteandmete fail
    t1 = do(enter_filename("kettaheide.txt")).\
        then(check_function_exists('parimad_katsed'))
    t1.as_test("Set "+test_set_name+": function 'parimad_katsed' exists").\
        add_decorator(create_file_dec)

    expected = parimad_katsed(without_failures(test_set))
    do(check_function_results('parimad_katsed', [test_set], expected)).after(t1).\
        as_test("Set "+test_set_name+": parimad_katsed({}) returns {}"
            .format(repr(test_set), expected)).\
        add_decorator(create_file_dec)

    # tulemus muutujasse salvestatakse tulemused
    