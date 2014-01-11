"""
Task description (in Estonian):

2. Sõnade otsimine (10p)
Failis sonad.txt (kodeering UTF-8) on nimekiri eestikeelsete sõnadega. Kirjuta
progamm, mis küsib kasutajalt mingi sõna alguse ja üritab väljastada sellele
vastava sõna, mis leidub mainitud failis. 

Kui antud prefiksile vastab täpselt üks sõna, siis tuleb see sõna lihtsalt
ekraanile kuvada ja programmi töö lõpetada.

Kui antud prefiksiga sõnu ei leidu, tuleb väljastada Sellist sõna ei leidu.

Kui antud prefiksiga leidub rohkem, kui 1 sõna, siis tuleb kuvada märkus 
    Leidub mitu sellise algusega sõna: 
ja selle alla kõik sobivad sõnad (selles järjekorras nagu nad failis esinevad).

Mõlemal juhul tuleb sõna küsimise ja otsimise protsessi korrata, kuni sisestatud
prefiksile vastab täpselt 1 sõna.

Näide (kasutaja poolt sisestatud tekst on kursiivis):
    Sisesta sõna algus: kalap
    Leidub mitu sellise algusega sõna:
    kalapaat
    kalapall
    kalapraad
    kalapulk
    kalapüügikunst
    kalapüügivarustus
    kalapüük
    Sisesta sõna algus: kalapr
    kalapraad
"""

from grader import *
from KT2_util import *

def prefix_matches(prefix, filename):
    with open(filename) as f:
        results = [line.strip() for line in f if line[:len(prefix)] == prefix]
    if not results:
        return ['Sellist sõna ei leidu.']
    return results

def end_of_input(matches):
    return len(matches) == 1 and matches != ['Sellist sõna ei leidu.']

BASE_TEMPLATE = "Otsingutele {prefixes} failist {filename} peaks vastuseks olema vastavalt {expected}"
def checker(prefixes, check_end=False, filename="_sonad.txt", description=BASE_TEMPLATE):
    description = description.format(
        prefixes=prefixes,
        filename=filename,
        expected=[prefix_matches(p, filename) for p in prefixes]
    )

    @test
    @create_temporary_file('sonad.txt', open(filename).read())
    @timeout(3)
    def test_function(m):
        from time import sleep
        for prefix in prefixes:
            sleep(0.1) # hack!
            m.stdout.reset()
            m.stdin.write(prefix)
            answer = m.stdout.read()
            user_lines = [line for line in answer.split('\n') if line and "sisesta " not in line.lower()]

            matches = prefix_matches(prefix, 'sonad.txt')

            if len(matches) > 1:
                matches = ['Leidub mitu sellise algusega sõna:'] + matches
            #assertEquals(len(matches), len(user_lines))
            assert len(matches) == len(user_lines), "Pikkused ei klapi. Saime järgmised read: {}, ootasime {}".format(user_lines, matches)

            for line, expected_line in zip(user_lines, matches):
                assert expected_line in line, "Oodatud rea ({}) asemel saime ({}).\nVäljund: \n{}\nOodatud väljund:\n{}".format(expected_line, line, answer, "\n".join(matches))

            if check_end and end_of_input(matches):
                assert not m.stdin.waiting, "Programm peaks töö lõpetama kui 1 vastusega sõna leitud. Väljund: \n{}\nOodatud väljund:\n{}".format(answer, "\n".join(matches))


    setDescription(test_function, description)

checker(['abc'], description="Vastuseta otsing. "+BASE_TEMPLATE)
checker(['vastusetaotsing'], check_end=True, description="Vastuseta otsing, kontrollime kas lõppeb. "+BASE_TEMPLATE)
checker(['vastutama'])
checker(['automaatselt'], check_end=True, description="1 vastusega täissõna otsing, kontrollime lõppemist. "+BASE_TEMPLATE)
checker(['koomil'])
checker(['koomik'])
checker(['aatomip'], check_end=True)
checker(['kaasa', 'kaasae', 'kaasaelamine'], check_end=True)