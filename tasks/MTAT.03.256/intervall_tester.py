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


@test_cases(
    [(0, 5), (2, 2), (-3, -1), (88, 100), (5, 100)],
    description="Vahemik [{0}, {1}]"
)
def test_interval(m, low, high):
    m.stdin.put(str(low))
    m.stdin.put(str(high))

    output = m.stdout.read()
    lines = output.strip().split('\n')

    expected = list(map(str, range(low, high + 1)))

    assert lines == expected or expected==[] and lines==[""], (
        "Ootasime:\n{}\n----\nSaime:\n{}"
        .format("\n".join(expected), output.strip()))
