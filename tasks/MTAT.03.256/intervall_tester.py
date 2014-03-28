"""
Task description (in Estonian):
Kirjutage programm, mis küsib sisendiks 2 täisarvu ning väljastab ekraanile
arvud alates esimesest antud täisarvust ja kuni teise täisarvuni (kaasaarvatud).
Kui antud täisarvud on võrdsed, siis tuleb väljastada ainult üks täisarv.
Kui esimene arv on suurem, siis ärge väljastage midagi.

NB! Selleks, et mitte olla väljundi kontrollimisel ülemäära range, otsib
    kontrollija arve kogu teie programmi väljundist. Seejuures tuleb aga arvestada,
    et ka kasutajale esitatud küsimused on programmi väljund. Seetõttu ärge
    kirjutage input käsu argumendis arve. Kui te kirjutate kasutajale nt.
    "Sisesta 1. arv", siis ka seda arvu 1 loeb kontrollija vastuse hulka.
"""

from grader import *


def set_description(d):
    def inner(f):
        setDescription(f, d)
        return f
    return inner


def test_with_args(description=None, **kwargs):
    if description is None:
        keys = sorted(kwargs.keys())
        description = ", ".join(key+"={"+key+"}" for key in keys)

    pair_each_element_with = lambda key, lst: [(key, v) for v in lst]
    # generate list of args to test
    paired = [pair_each_element_with(key, value) for key, value in kwargs.items()]
    test_kwargs = list(map(dict, zip(*paired)))

    def _inner(function):
        # remove from tests if there
        for kw in test_kwargs:
            @test
            @set_description(description.format(**kw))
            def tested_fun(m):
                function(m, **kw)
    return _inner


@test_with_args(
    description="Vahemik [{low}, {high}]",
    low=[0, 2, -3, 88], high=[5, 2, -1, 100])
def test_interval(m, low, high):
    m.stdin.put(str(low))
    m.stdin.put(str(high))

    output = m.stdout.read()
    lines = output.strip().split('\n')

    expected = list(map(str, range(low, high+1)))

    assert lines == expected, (
        "Ootasime:\n{}\n----\nSaime:\n{}".format("\n".join(expected), output.strip()))
