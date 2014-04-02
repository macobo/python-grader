from grader import *


def yhisosa(a, b):
    return list(frozenset(a) & frozenset(b))

@test_cases(
    [
        ([], []),
        ([2,5], [6,2]),
        ([4,4], [4,4,5]),
        ([2,2,3,4,4], [])
    ],
    expected=yhisosa,
    description="yhisosa({0}, {1}) == {expected} (järjekord pole oluline)"
)
def testi(m, a, b, expected):
    a_c, b_c = a.copy(), b.copy()
    #assert "yhisosa" in m.module, "Ei leidnud funktsiooni 'yhisosa'"
    solution = m.module.yhisosa(a, b)

    assert sorted(expected) == sorted(solution), (
        "Tulemus ei vastanud oodatule.\n"
        "Ootasime {}, Saime {}"
    ).format(expected, solution)

    assert id(a_c) != id(a) or id(b_c) != id(b), (
        "Funktsioon muutis argumendiks antud järjendit."
    )
