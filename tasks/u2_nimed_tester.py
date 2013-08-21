"""
Nimede korrastamine

Modifitseerige veelkord kasutaja tervitamise programmi, kus kasutaja sisestab 
eraldi ees- ja perenime ning programm tervitab teda täisnimega.

Seekord peaks programm vastama alati selliselt, et nii eesnimi, kui perenimi 
algavad suure tähega ja ülejäänud tähed on väikesed, hoolimata sellest, kuidas 
nimi sisestati (olgu ainult väikeste tähtedega, ainult suurtega või segamini).
"""

from grader import *

@test
def program_asks_input_twice(module):
    for name in ['maRI', 'kUUsK']:
        assert module.is_waiting_input()
        module.stdin.write(name)
    assert not module.is_waiting_input()


def name_test(name, description = None):
    correct_name = name.title()
    if description is None:
        description = name + " => " + correct_name
    io_test(description, name.split(), correct_name)

name_test("Mari Kuusk", "Don't change correct name (Mari Kuusk)")
name_test("maRT Laaremägi")
name_test("tIiNa KuKK")
name_test("MarKuS pAJu")
name_test("laura jõgi")
name_test("mARi-lIIS kASK")