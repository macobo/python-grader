"""
Täisnurkne kolmnurk

Kirjutage funktsioon, mis võtab argumentideks kolmnurga külgede pikkused ja tagastab True või False vastavalt sellele, kas tegemist oli täisnurkse kolmnurgaga või mitte.
"""

from grader import *

check_function("taisnurkne", [3, 4, 5], True)
check_function("taisnurkne", [1, 1, 1], False)
check_function("taisnurkne", [917.2102192315585, 561.3888059296613, 1075.3752729563455], True)
check_function("taisnurkne", [917.2102192315585, 561.3888059296613, 1075.2752729563455], False)