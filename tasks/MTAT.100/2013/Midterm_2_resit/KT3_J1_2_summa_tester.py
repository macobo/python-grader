"""
Task description (in Estonian):

2. Loetelu summa (2+2p)
Ükskõik kui pikki loetelusid on võimalik moodustada kasutades ainult
kaheelemendilisi liste.

Näiteks loetelu 1, 2, 3, 4, 5 saaksime kaheelemendiliste listide abil esitada
nii: [1, [2, [3, [4, 5]]]].

Kirjuta funktsioonid summa1 ja summa2, mis võtavad argumendiks taoliselt
esitatud täisarvude loetelu, ning tagastavad loetelu elementide summa. Seejuures
ei tohi funktsioonis summa1 kasutada tsüklit ja funktsioonis summa2 ei tohi
kasutada rekursiooni. 

Võib eeldada, et etteantud andmestruktuur koosneb ainult täisarvudest ja
kaheelemendilistest listidest ja iga listi esimene element on täisarv.

Näited:
    >>> summa1([1, [2, [3, [4, 5]]]])
    15
    >>> summa2([1, [2, [3, [4, 5]]]])
    15
    >>> summa1([1, [-32, 0]])
    -31
    >>> summa1([1, 2])
    3

Vihje:
    >>> isinstance(123, list)
    False
    >>> isinstance([4,5], list)
    True
    >>> isinstance([4,[5,6]], list)
    True
    >>> isinstance(123, int)
    True
"""

from grader import *
from KT2_util import *
import ast

def summa(a):
    if isinstance(a[1], int):
        return a[0] + a[1]
    else:
        return a[0] + summa(a[1])

# --- ast walking functions --- #
def collect(tree, is_relevant_node = None, depth=0, **kwargs):
    if is_relevant_node is None:
        is_relevant_node = lambda *a, **kw: True

    result = is_relevant_node(tree, depth=depth, **kwargs)
    if result:
        yield tree

    if isinstance(tree, ast.AST):
        for field, child in ast.iter_fields(tree):
            yield from collect(child, is_relevant_node, depth=depth+1, **kwargs)
    if isinstance(tree, list):
        for child in tree:
            yield from collect(child, is_relevant_node, depth=depth+1, **kwargs)

def walk(tree, is_relevant_node, **kwargs):
    return list(collect(tree, is_relevant_node, **kwargs))

def is_loop(tree, depth):
    return tree.__class__ in [ast.While, ast.For]

def function_definition(tree, depth, function_name):
    return tree.__class__ == ast.FunctionDef and tree.name == function_name

# checkers

def count_loops(tree, function_name):
    function = walk(tree, function_definition, function_name=function_name)
    assert len(function) == 1, (
        "Peaks leiduma täpselt 1 funktsioon nimega {}. Leidsime {}"
        .format(function_name, function)
    )
    loops = walk(function, is_loop)
    return len(loops)

def call_counter(function):
    def _inner(*args):
        _inner.call_count += 1
        return function(*args)
    _inner.call_count = 0
    return _inner

@test
@expose_ast
def check_for_loops(m, AST):
    "Funktsioonis summa1 ei tohi sisaldada tsükleid. (eksperiment)"
    loops = count_loops(AST, "summa1")
    assert loops == 0, (
        "Funktsioonis summa1 ei tohiks esineda tsükleid. Leidsime {}".format(loops))

def function_test(function_name, args, expected, should_be_recursive=None):
    # if should_be_recursive is something other than True or False, it is
    # ignored. Otherwise, call count is checked (it should be greater than 1)
    args_str = ", ".join(map(repr, args))
    description = "Test - {function}({args}) == {expected}"
    if should_be_recursive is True:
        description += ", lisaks on rekursiivne"
    if should_be_recursive is False:
        description += ", lisaks ei ole rekursiivne"
    description = description.format(
        function=function_name, 
        args=args_str, 
        expected=repr(expected))

    @test
    def test_function(m):
        assert hasattr(m, 'module'), "Programmi täitmine ei lõppenud. Failis ei tohiks olla üleliigseid input() käski"
        assert hasattr(m.module, function_name), "Peab leiduma funktsioon nimega {name}!".format(name=function_name, dict=m.module.__dict__)
        user_function = call_counter(getattr(m.module, function_name))
        setattr(m.module, function_name, user_function)
        #assert False, user_function

        result = user_function(*args)
        assertEquals(result, expected,
            "{function_name}({args_str}) peaks tagastama {expected} aga tagastas {result}",
            expected=expected,
            result=result,
            function_name=function_name,
            args_str=args_str)

        if should_be_recursive is False:
            assert user_function.call_count == 1, (
                "Funktsiooni {function_name} kutsus end välja {n} korda, "
                "järelikult on tegu rekursiivse funktsiooniga!"
                .format(function_name=function_name, n=user_function.call_count)
            )

    setDescription(test_function, description)
    return test_function

def check(*args):
    function_test("summa1", args, summa(*args))
    function_test("summa2", args, summa(*args), should_be_recursive=False)

check([1, 2])
check([6, 7])
check([3, [2, 9]])
check([1, [-32, 0]])
check([-9, [1, [4, [2, [9, -100]]]]])
check([-7, [-2, [3, [5, [7, [9, [7, [-10, -6]]]]]]]])
check([-7, [2, [2, [-7, [3, -7]]]]])
check([4, [8, [4, [-3, -8]]]])