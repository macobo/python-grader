"""
Task description (in Estonian):

2. Listidesse paigutamine (3p)
Kirjuta funktsioon paiguta, mis võtab argumendiks mittenegatiivse täisarvu n ja
tagastab ühe- või mitmetasemelise listi, milles (otseselt või kaudselt) esineb n
korda väärtus True. 

Kitsenduseks on see, et üheski listis (ükskõik millisel tasemel) ei tohi olla
(otseselt) rohkem kui kaks elementi.

Näited:
paiguta(2) puhul on sobiv vastus näiteks [True, True],
paiguta(3) puhul on sobiv vastus näiteks [[True, True], True],
paiguta(0) puhul on sobiv vastus näiteks [],
paiguta(5) puhul on sobiv vastus näiteks [[True, True], [[True, True], True]].

NB! Pane tähele, et ülesande tekst ei nõua täpselt samasugust paigutust nagu
näidetes toodud – võimalusi on veel.
"""

from grader import *

def loenda_true(a):
    tulemus = 0
    for el in a:
        if el == True:
            tulemus += 1
        elif isinstance(el, list):
            tulemus += loenda_true(el)

    return tulemus

def maksimaalne_aste(a):
    tulemus = len(a)
    for el in a:
        if isinstance(el, list):
            m_aste = maksimaalne_aste(el)
            if m_aste > tulemus:
                tulemus = m_aste

    return tulemus

def register_test(n):
    @test
    def paiguta_checker(m):
        function_name = "paiguta"
        assert hasattr(m, 'module'), "Programmi täitmine ei lõppenud. Failis ei tohiks olla input() käsku"
        assert hasattr(m.module, function_name), "Peab leiduma funktsioon nimega paiguta!"
        user_function = getattr(m.module, function_name)
        result = user_function(n)

        assert isinstance(result, list), (
            "Tulemuseks ei olnud list.\n"
            "Ootasime et vastuses esineks True {} korda, saime aga vastuseks {}"
            .format(n, result))

        true_arv = loenda_true(result)
        assert true_arv == n, (
            "Tulemuses esineb True {} korda, aga peaks esinema {} korda.\n"
            "Kasutaja funktsioon tagastas {}"
            .format(true_arv, n, result))

        maks_aste = maksimaalne_aste(result)
        assert maks_aste <= 2, (
            "Tulemuses leidus liste, milles oli {} elementi.\n"
            "Kasutaja funktsioon tagastas {}"
            .format(maks_aste,  result))

    setDescription(paiguta_checker, "paiguta(" + str(n)+")") 
    #return paiguta_checker
                                 
register_test(0)
register_test(1)
register_test(2)
register_test(3)
register_test(16)
register_test(17)

"""
def paiguta(n):
    if n == 0:
        return []
    elif n == 1:
        return [True]
    elif n == 2:
        return [True, True]
    else:
        return [paiguta(n//2), paiguta(n - n//2)]


# järgmisele võimalusele näidetes ei viidata, aga ülesande tekst lubab
def paiguta2(n):
    if n == 0:
        return []
    else:
        return [True, paiguta2(n-1)]

"""
