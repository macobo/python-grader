from grader import *
from random import seed, randint
seed(0)

def ühisosa(a, b):
    return list(sorted(frozenset(a) & frozenset(b)))

def randomArray(size, _range=(0, 10)):
    return [randint(*_range) for _ in range(size)]

def test_description(a, b, expected):
    if len(a) < 100 and len(b) < 100:
        return "ühisosa({a}, {b}) == {expected}".format(**locals())
    return "ühisosa leidmine suurtel järjenditel. n={}".format(max(len(a), len(b)))

@test_cases(
    [
        ([], []),
        ([2,5], [6,2]),
        ([4,4], [4,4,5]),
        ([2,3,3], [3,2]),
        ([2,2,3,4,4], []),
        ([], [2,2,3,4,4]),
        (randomArray(5), randomArray(6)),
        (randomArray(7), randomArray(3)),
        (randomArray(20, (-10, 10)), randomArray(20, (-10, 10))),
        (randomArray(100, (-1000, 1000)), randomArray(100, (-1000, 1000))),
        (randomArray(500, (-1000, 1000)), randomArray(500, (-1000, 1000))),
        (randomArray(50000, (-1000, 1000)), randomArray(50000, (-1000, 1000))),
    ],
    expected=ühisosa,
    description=test_description#"ühisosa({0}, {1}) == {expected} (järjekord pole oluline)"
)
def testi(m, a, b, expected):
    a_c, b_c = a.copy(), b.copy()
    assert hasattr(m.module, 'ühisosa'), "Ei leidnud funktsiooni 'ühisosa'"
    solution = m.module.ühisosa(a, b)
    
    assert sorted(expected) == sorted(solution), (
        "Tulemus ei vastanud oodatule.\n"
        "Ootasime {}, Saime {}"
    ).format(repr(expected), repr(solution))
    
    assert isinstance(solution, list), "Tulemus peab olema list!"

    assert a_c == a and b_c == b, (
        "Funktsioon muutis argumendiks antud järjendit."
    )
