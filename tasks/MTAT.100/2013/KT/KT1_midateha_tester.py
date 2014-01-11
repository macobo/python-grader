"""
Task description (in Estonian):

1. Mida teha? (3p)
Kirjuta funktsioon nimega mida_teha, mis võtab argumentideks kuu numbri ning 
nädalapäeva lühendi (nt. "E" või "P") ja tagastab sõne, mis ütleb, mida võiks 
sellisel kuul ja sellisel nädalapäeval teha. Tegevuste soovitused tuleks valida 
järgnevate reeglite põhjal:

    Kõigil pühapäevadel tuleb soovitada "puhka"
    Muudel päevadel tuleb soovitus anda vastavalt kuule:
    kevadkuudel on soovituseks "külva redist"
    suvekuudel on soovituseks "rauta rege"
    sügiskuude soovituseks on "riisu lehti"
    talvekuudel tuleb soovitada "küta ahju".

Võib eeldada, et funktsiooni kasutatakse ainult sobivate argumentidega. 
Funktsioon peab andma sama tulemuse hoolimata sellest, kas kasutaja sisestab 
nädalapäeva lühendi suure või väikse tähega. NB! Funktsioon peab soovitused 
tagastama väikeste tähtedega! Näited funktsiooni kasutamisest:
    >>> mida_teha(2, 'P')
    'puhka'
    >>> mida_teha(2, 'p')
    'puhka'
    >>> mida_teha(2, 'K')
    'küta ahju'
    >>> mida_teha(6, 'T')
    'rauta rege'

Funktsiooni töö demonstreerimiseks tuleb kasutajalt küsida kuu number ja 
nädalapäeva lühend, anda need funktsioonile argumendiks. Saadud tagastusväärtuse
esimene täht tuleb teisendada suurtäheks, sõne lõppu lisada hüüumärk ja 
väljastada tulemus ekraanile. Võib eeldada, et kasutaja sisestab alati 
sobivad sisendandmed. 

Näide programmi võimalikust kasutamisest:
    Sisesta kuu number: 9
    Sisesta nädalapäeva lühend: k
    Riisu lehti!

Vihje: Proovi väärtustada avaldis "rauta rege".capitalize().
Alternatiiv (-1p). Lahenda sama ülesanne ilma funktsiooni kasutamata.
"""

from grader import *

def solution(month, weekday):
    weekday = weekday.lower()
    if weekday == 'p': 
        return 'puhka'
    elif 3 <= month < 6: 
        return 'külva redist'
    elif 6 <= month < 9: 
        return 'rauta rege'
    elif 9 <= month < 12: 
        return 'riisu lehti'
    else: 
        return 'küta ahju'

def io_solution(month, weekday):
    return solution(month, weekday).capitalize() + "!"

def checker(month, weekday):
    description = "IO test - Kuu: {}, Nädalapäev: {} => '{}'".format(
        month, weekday, io_solution(month, weekday))
    io_test(description, [month, weekday], io_solution(month, weekday))
    function_checker(month, weekday)

def assertEquals(a, b, template = "Expected {a} but got {b}"):
    if a != b:
        raise AssertionError(template.format(a=repr(a), b=repr(b)))

def function_checker(month, weekday, IO=['2', 'P']):
    description = "Function test - mida_teha({}, {}) == {}".format(
        month, weekday, io_solution(month, weekday))
    function_name = "mida_teha"

    @test
    def test_function(m):
        for line in IO: m.stdin.write(line)
        from time import sleep
        sleep(0.01)
        assert hasattr(m, 'module'), "Programmi täitmine ei lõppenud. Failis ei tohiks olla üleliigseid input() käski"
        assert hasattr(m.module, function_name), "Peab leiduma funktsioon nimega {name}!".format(name=function_name, dict=m.module.__dict__)

        mida_teha = m.module.mida_teha
        tulemus = mida_teha(month, weekday)
        assertEquals(tulemus, solution(month, weekday),
            "mida_teha("+str(month)+", "+weekday+") peaks tagastama {b} aga tagastas {a}")

    setDescription(test_function, description)

checker(2, 'P')
checker(2, 'p')
checker(2, 'K')
checker(6, 'T')
checker(1, 'e')
checker(10, 'l')
checker(1, 'l')
checker(12, 'L')
checker(3, 'R')