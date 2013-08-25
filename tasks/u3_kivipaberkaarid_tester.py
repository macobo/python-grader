"""
7. Kivi-paber-käärid

Kirjutage programm, mis väljastab iga ENTER-klahvi vajutuse peale ühe juhuslikult 
valitud sõna loetelust “kivi”, “paber”, “käärid”. 
Programmi töö lõpetamiseks tuleb kasutajal enne ENTERi vajutamist sisestada “aitab”.
"""

from grader import *

SIGNS = ["kivi", "paber", "käärid"]

def find_used(collection, input):
    return [el for el in collection if el in input]

def assert_contains_n(input, collection, times):
    used = find_used(collection, input)
    if len(used) == times: return
    message = """Input should only contain {times} items from collection.
input: 
{input}
found items: {used}
collection: {collection}
""".format(**locals())
    raise AssertionError(message)

@test
def one(m):
    " Pärast ENTERi vajutamist tuleks väljastada kas 'kivi', 'paber', 'käärid' "
    m.stdout.reset()
    m.stdin.write("\n") #ENTER
    assert_contains_n(m.stdout.new(), SIGNS, 1)


io_test("Pärast aitab sisestamist peab programm lõpetama", 
    ["\n", "\n", "\n", "\n", "aitab"], "")

@test
def many(m):
    """Pärast 300 ENTERit peaks kõiki väljastatud olema vähemalt 10 korda 
    (kasuta randomit!)"""
    response_counts = { s: 0 for s in SIGNS }
    for _ in range(300):
        m.stdout.reset()
        m.stdin.write("\n") #ENTER
        response = m.stdout.new()
        assert_contains_n(response, SIGNS, 1)
        response_counts[find_used(SIGNS, response)[0]] += 1
    assert all(count >= 10 for count in response_counts.values())
