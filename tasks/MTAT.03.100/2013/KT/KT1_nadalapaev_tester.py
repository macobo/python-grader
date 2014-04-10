"""
Task description (in Estonian):

1. Nädalapäev (3p)
2014. aasta 1. september on esmaspäev. Kirjuta funktsioon nädalapäev, mis võtab
argumendiks täisarvu, mis tähistab mõnda 2014. a. septembri päeva, ning tagastab
sellele päevale vastava nädalapäeva nime. 

Näiteks nädalapäev(3) peab tagastama "kolmapäev" ja nädalapäev(13) peab 
tagastama "laupäev". Kui mainitud kuus pole sellist päeva, siis tuleb tagastada
"Viga!".

Demonstreeri funktsiooni tööd kasutajalt küsitud päevaga. 
Funktsiooni tagastusväärtus tuleb väljastada ekraanile täislausega kujul 
<päeva number>. september 2014 on <nädalapäeva nimi>. Näiteks: 13. september 
2014 on laupäev. 

Kui funktsioon tagastab "Viga!" (nt. kui kasutaja sisestab 45),  siis tuleb ka
ekraanile kuvada lihtsalt Viga! (mitte 45. september 2014 on Viga!.).

Vihje: Proovi väärtustada avaldised 12 % 10 ja 22 % 10.
Alternatiiv (-1p). Lahenda sama ülesanne ilma funktsiooni kasutamata.
"""

from grader import *

def solution(kp):
    j = (kp - 1) % 7
    if kp < 1 or kp > 30: return "Viga!"
    elif j == 0: return "esmaspäev"
    elif j == 1: return "teisipäev"
    elif j == 2: return "kolmapäev"
    elif j == 3: return "neljapäev"
    elif j == 4: return "reede"
    elif j == 5: return "laupäev"
    elif j == 6: return "pühapäev"

def io_solution(kp):
    ans = solution(kp)
    if ans == "Viga!":
        return ans
    return str(kp)+". september 2014 on "+ans

# paev = int(input("Sisesta päev "))
# print(str(paev)+". september 2014 on "+nadalapaev(paev))


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


def checker(kp):
    description = "IO test - päev: {} => {}".format(
        kp, io_solution(kp))
    
    io_test(description, [kp], str(io_solution(kp)))
    function_test("nädalapäev", [kp], solution(kp))

checker(1)
checker(15)
checker(16)
checker(17)
checker(18)
checker(26)
checker(27)
checker(28)
checker(30)

checker(0)
checker(50)
checker(31)