"""
Kirjutage programm, mis küsib kasutajalt ridade arvu ning väljastab ekraanile vastava kõrgusega kujundid järgneva skeemi järgi:

# # # # # # #
#           #
#           #
#           #
#           #
#           #
# # # # # # #
*
* *
* * *
* * * *
* * * * *
* * * * * *
* * * * * * *
"""
from grader import *

def ruut(n):
    return "\n".join(["*"*n] + ['*'+' '*(n-2)+'*' for _ in range(n-2) ] + ["*"*n]) + "\n"

def kolmnurk(n):
    return "\n".join("*"*i for i in range(1, n+1)) + "\n"


io_test("7-ne ruut", [7], ruut(7))
io_test("6-ne kolmnurk", [6], kolmnurk(6))

io_test("1-ne kolmnurk", [1], kolmnurk(1))
io_test("1-ne ruut", [1], ruut(1))

io_test("8-ne ruut", [8], ruut(8))