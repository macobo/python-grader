"""
Task description (in Estonian):

1. Nädalapalga arvutamine (3p)
Kui inimene töötab nädalas 40 tundi või vähem, siis nende tundide eest saab ta
palga vastavalt oma tavalisele tunnitasule. Kui inimene töötab rohkem kui 40
tundi, siis ületundide eest on tunnitasu 50% kõrgem.

Kirjuta funktsioon nädalapalk, mis võtab 2 argumenti: töötundide arvu nädalas ja
tavalise tunnitasu ning tagastab vastava nädalapalga arvestades ka ületundidega,
kui neid on. 

Näited funktsiooni kasutamisest:
    >>> nädalapalk(20, 10)
    200.0
    >>> nädalapalk(40, 10)
    400.0
    >>> nädalapalk(60, 10)
    700.0

Demonstreeri funktsiooni tööd küsides algandmed kasutajalt ja salvestades 
vastuse faili nimega palk.txt.

Alternatiiv (-1p). Lahenda sama ülesanne ilma funktsiooni kasutamata. 
Lihtsustus (-1p). Kuva tulemus faili kirjutamise asemel ekraanile.
"""

from grader import *

def nädalapalk(tunde, tavapalk):
    tulemus = tunde * tavapalk
    if tunde > 40:
        tulemus = tulemus + (tunde - 40) * tavapalk / 2
    return tulemus


def assertEquals(a, b, template = "Expected {a} but got {b}"):
    if a != b:
        raise AssertionError(template.format(a=repr(a), b=repr(b)))


def function_test(function_name, args, expected, IO=None):
    if IO is None:
        IO = list(map(str, args)) * 2
    args_str = ", ".join(map(repr, args))
    description = "Function test - {}({}) == {}".format(
        function_name, args_str, expected)

    @test
    def test_function(m):
        for line in IO*2: 
            m.stdin.write(line)
        assert hasattr(m, 'module'), "Programmi täitmine ei lõppenud. Failis ei tohiks olla üle {} input käsu. Meie sisendread: {}".format(len(IO), IO)
        assert hasattr(m.module, function_name), "Peab leiduma funktsioon nimega {}! {}".format(function_name, m.module.__dict__)
        user_function = getattr(m.module, function_name)
        result = user_function(*args)
        assertEquals(result, expected,
            "{function_name}({args_str}) peaks tagastama {expected} aga tagastas {result}".format(
                expected=expected,
                result=result,
                function_name=function_name,
                args_str=args_str))

    setDescription(test_function, description)
    return test_function

def file_test(filename, IO, expected):
    description = "IO test, väljund faili - Sisend: {} => failis {} on {}".format(
        IO, filename, repr(expected))

    @test
    @after_test(delete_file(filename))
    def test_function(m):
        import os
        assert os.path.exists(filename), "fail {} peab eksisteerima".format(filename)
        with open(filename) as f:
            contents = f.read()
        require_contains(contents, expected, "Failis peab leiduma {what}. Faili sisu oli {input}")
    setDescription(test_function, description)


def checker(a, b):
    description = "IO test - tunde: {}, palk: {}=> {}".format(
        a, b, nädalapalk(a, b))
    
    io_test(description, [a, b], str(nädalapalk(a, b)))
    function_test("nädalapalk", [a, b], nädalapalk(a, b))
    file_test("palk.txt", [a, b], str(nädalapalk(a, b)))


checker(0, 10)
checker(20, 10)
checker(40, 10)
checker(40, 70)
checker(60, 10)
checker(100, 1.5)
checker(1, 0.5)