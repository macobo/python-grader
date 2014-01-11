"""
Task description (in Estonian):

1. Faili lugemine (3p)
Kirjuta funktsioon arvuta, mis võtab 3 argumenti: sõnena antud arvutustehte 
sümboli (see võib olla "+", "-", "*" või "/") ning kaks arvu, ja tagastab
vastavalt nende arvude summa, vahe, korrutise või jagatise. 
Näited funktsiooni kasutamisest:
    >>> arvuta("/", 26, 4)
    6.5
    >>> arvuta("+", 1, 1)
    2

Demonstreeri funktsiooni tööd lugedes funktsiooni argumendid failist 
algandmed.txt, mille sisu on järgnev:
    +
    14
    7

Alternatiiv (-1p): Lahenda sama ülesanne ilma funktsiooni kasutamata. 
Lihtsustus (-1p). Demonstreeri funktsiooni tööd küsides algandmed kasutajalt 
failist lugemise asemel. 
"""

from grader import *

def solution(tehe, a, b):
    if tehe == '+': return a+b
    if tehe == '-': return a-b
    if tehe == '/': return a/b
    if tehe == '*': return a*b


def assertEquals(a, b, template = "Expected {a} but got {b}"):
    if a != b:
        raise AssertionError(template.format(a=repr(a), b=repr(b)))


def function_test(function_name, args, expected, IO=None):
    if IO is None:
        IO = list(map(str, args))
    args_str = ", ".join(map(repr, args))
    description = "Function test - {}({}) == {}".format(
        function_name, args_str, expected)

    @test
    def test_function(m):
        for line in IO: m.stdin.write(line)
        assert hasattr(m, "module") and hasattr(m.module, function_name), \
                    "Peab leiduma funktsioon nimega {}!".format(function_name)
        user_function = getattr(m.module, function_name)
        result = user_function(*args)
        assertEquals(result, expected,
            "{function_name}({args_str}) peaks tagastama {expected} aga tagastas {result}".format(
                expected=expected,
                result=result,
                function_name=function_name,
                args_str=args_str))

    setDescription(test_function, description)
    return test_function


def io_file_test(filename, contents, expected_print):
    if not isinstance(contents, str):
        contents = "\n".join(map(str, contents))
    description = "Input file ({}): {}, Expected output: {}".format(
        filename, repr(contents), repr(expected_print))

    @test
    @create_temporary_file(filename, contents)
    def test_function(m):
        require_contains(
            m.stdout.read(), 
            expected_print, 
            "Väljundis peaks sisalduma {what}.\nVäljund oli: {input}")

    setDescription(test_function, description)


def checker(tehe, a, b):
    data = [tehe, a, b]
    description = "IO test - tehe: {}, a: {}, b: {} => {}".format(
        tehe, a, b, solution(*data))
    
    io_test(description, data, str(solution(*data)))
    io_file_test('algandmed.txt', data, str(solution(*data)))
    f = function_test("arvuta", data, solution(*data))
    # lisame igaks juhuks sama sisuga algandmed.txt
    create_temporary_file('algandmed.txt', data)(f)

checker('+', 1, 2)
checker('/', 26, 4)
checker('-', 1, 2)
checker('*', 5, 7)
checker('+', 23, 78)
checker('+', 0.5, 0.05)