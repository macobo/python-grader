"""
Tagurpidi

Kirjutage rekursiivne funktsioon tagurpidi, mis võtab argumendiks järjendi ja tagastab selle elemendid uue järjendina vastupidises järjestuses. Nt. tagurpidi("stressed") peaks tagastama sõne "desserts". Ülesanne tuleks lahendada ilma tsükleid kasutamata. NB! see funktsioon peaks töötama ka tühja järjendi puhul!
"""

from grader import *

check_function("tagurpidi", ["ab"], "ba")
check_function("tagurpidi", ["tagurpidi"], "idiprugat")
check_function("tagurpidi", [""], "")
check_function("tagurpidi", ["tõnis"], "sinõt")