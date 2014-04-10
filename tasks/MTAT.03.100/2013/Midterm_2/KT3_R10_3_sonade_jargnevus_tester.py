"""
3. Sõnade järgnevus (11p)
Kirjuta funktsioon sõnade_järgnevus, mis võtab argumendiks sõnena mingi teksti
ning tagastab sõnastiku, mis näitab, millised sõnad järgnevad millistele
sõnadele – sõnastiku kirje võtmeks on mingi sõna ja  väärtuseks hulk temal
järgnevatest sõnadest.

Suurtel ja väikestel tähtedel vahet mitte teha, tulemuseks antud sõnastikus
kasutada ainult suurtähti. 
Võib eeldada, et 
    1) kirjavahemärkidest esinevad tekstis ainult punkt, koma, küsimärk ja 
        hüüumärk.
    2) kirjavahemärgid järgnevad alati eelnevale sõnale vahetult
    3) iga kahe sõna vahel on vähemalt üks tühik.

Näiteks
    sõnade_järgnevus("Tere Madis! Tere Tere, kuidas läheb?") 
peaks andma tulemuseks
    {'TERE'  : {'MADIS', 'TERE', 'KUIDAS'},
     'MADIS' : {'TERE'},
     'KUIDAS': {'LÄHEB'},
     'LÄHEB' : set()}

Funktsiooni töö demonstreerimiseks tuleb argumenttekst lugeda sisse failist
tekst.txt (kodeeringus UTF-8).

Funktsiooni poolt tagastatud sõnastik tuleb salvestada muutujasse sõnade_info,
selle põhjal tuleb ekraanile kuvada need sõnad, mis on tekstis esinenud mitu
korda järjest (iga selline sõna eraldi reale). 

Antud näite korral peaks ekraanile ilmuma TERE.
"""

from grader import *
from KT2_util import *

def sõnade_järgnevus(tekst):
    sonad = [sona.strip(".,?!").upper() for sona in tekst.split()]
    tulemus = {}
    for sona in sonad:
        tulemus[sona] = set()
    for i in range(len(sonad)-1):
        tulemus[sonad[i]].add(sonad[i+1])
    return tulemus

def double_words(contents):
    words = sõnade_järgnevus(contents)
    return set(word for word in words if word in words[word])

## Function tests
def create_file_make_checker(sample_function, contents):
    decorator = create_temporary_file('tekst.txt', contents)
    checker = make_checker(sample_function)
    return lambda *a, **kw: decorator(checker(*a, **kw))

def function_tests(contents):
    function_checker = create_file_make_checker(sõnade_järgnevus, contents)
    function_checker("TERE MADIS")
    function_checker("Tere tore ole")
    function_checker("Tere. tore ole")
    function_checker("Tere, tore kasPOLE? Ilm on kOle.")


def description(d):
    def inner(f):
        setDescription(f, d)
        return f
    return inner

def variable_tests(contents):
    variable_name = "sõnade_info"
    function_name = "sõnade_järgnevus"

    @test
    @description("Sisu {} - Muutuja {} peab olema defineeritud".format(repr(contents), variable_name))
    @create_temporary_file('tekst.txt', contents)
    def variable_exists(m):
        assert hasattr(m, 'module'), "Programmi täitmine ei lõppenud. Failis ei tohiks olla üle input() käski"
        assert hasattr(m.module, variable_name), "Peab leiduma funktsioon nimega {name}!".format(name=variable_name, dict=m.module.__dict__)
        return getattr(m.module, variable_name)
    
    @test
    @description("Sisu {} - Muutuja {} peab olema sõnastik".format(repr(contents), variable_name))
    @create_temporary_file('tekst.txt', contents)
    def variable_type(m):
        variable = variable_exists(m)
        assert isinstance(variable, dict), "Muutuja {} peaks olema sõnastik aga oli {}".format(variable_name, type(variable))

    @test
    @description("Sisu {} - Muutuja {} sisaldab sama mida funktsioon tagastas".format(repr(contents), variable_name))
    @create_temporary_file('tekst.txt', contents)
    def variable_contents(m):
        variable = variable_exists(m)
        assert hasattr(m, 'module'), "Programmi täitmine ei lõppenud. Failis ei tohiks olla üle input() käski"
        assert hasattr(m.module, function_name), "Peab leiduma funktsioon nimega {name}!".format(name=function_name, dict=m.module.__dict__)
        user_function = getattr(m.module, function_name)

        expected_value = user_function(contents)
        assert variable == expected_value, "Muutuja {} peaks sisaldama {}({})={}, aga sisaldas {}".\
                    format(variable_name, function_name, contents, expected_value, variable) 


def IO_tests(contents):
    double = double_words(contents)
    
    @test
    @description("Sisu {} - peaks väljastama kõik sõnad hulgast {}".format(repr(contents), double))
    @create_temporary_file('tekst.txt', contents)
    def io_words(m):
        output = m.stdout.read()
        words = output.split()
        assert all(x in words for x in double), \
            "Kõik sõnad hulgast {} peaksid esinema väljundis. Väljundis olevad sõnad: {}".format(double, words)
        return words

    @test
    @description("Sisu {} - peaks väljastama ainult sõnasid hulgast {} ilma kordusteta".format(repr(contents), double))
    @create_temporary_file('tekst.txt', contents)
    def io_exact(m):
        words = io_words(m)
        assert len(words) == len(double), "Väljastama peaks sama palju sõnu kui on topelt. Väljastatud sõnad: {}".format(words)
        assert set(words) == double, "Väljundis tohiks olla ainult sõnad hulgast {}. Väljastatud sõnade hulk: {}".format(double, set(words))

SAMPLE_TEST = "Tere Madis! Tere Tere, kuidas läheb?"

function_tests(SAMPLE_TEST)
variable_tests(SAMPLE_TEST)

TESTS = [
    SAMPLE_TEST,
    "LAUSE ILMA VAHEMÄRKIDETA ON TORE TORE ILUS ILUS JA LUND LUND SAJAB",
    "lause! väikeste väikeste. tähtedega, pole pole ka ka? paha",
    "Vahel pole ühtegi kordust, ei ühtegi kordust."
]
for testcase in TESTS:
    IO_tests(testcase)