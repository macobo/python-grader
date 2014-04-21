from grader import *
from random import seed, randint
seed(0)

def ühisosa(a, b):
    return list(frozenset(a) & frozenset(b))

def randomArray(size, _range=(0, 10)):
    return [randint(*_range) for _ in range(size)]

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
        (randomArray(20, (-10, 10)), randomArray(20, (-10, 10)))
    ],
    expected=ühisosa,
    description="ühisosa({0}, {1}) == {expected} (järjekord pole oluline)"
)
def testi(m, a, b, expected):
    a_c, b_c = a.copy(), b.copy()
    assert hasattr(m.module, 'ühisosa'), "Ei leidnud funktsiooni 'ühisosa'"
    solution = m.module.ühisosa(a, b)

    assert sorted(expected) == sorted(solution), (
        "Tulemus ei vastanud oodatule.\n"
        "Ootasime {}, Saime {}"
    ).format(repr(expected), repr(solution))

    assert id(a_c) != id(a) or id(b_c) != id(b), (
        "Funktsioon muutis argumendiks antud järjendit."
    )
