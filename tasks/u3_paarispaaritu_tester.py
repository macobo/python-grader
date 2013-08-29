"""
1. Paaris või paaritu

Koostage tekstifail (nimega arvud.txt), mis sisaldab täisarve erinevatel ridadel. 
Kirjutage programm, mis loeb antud failist ükshaaval arve ning kuvab iga arvu kohta 
ekraanile info, kas tegemist oli paaris või paaritu arvuga.
"""

from grader import *
from random import randrange



def paarispaaritu(numbers):
    return ["paaris" if x % 2 == 0 else "paaritu" for x in numbers]

def checker(numbers):
    expected = paarispaaritu(numbers)
    test_function = line_match_test(str(numbers), [], expected)
    # add an hook to create and delete the temporary file.
    # TODO: nicer syntax.
    test_function = create_temporary_file('arvud.txt', numbers)(test_function)

    #print("c!", test_function, test_function.__before_hooks__)

checker(list(range(1,5)))
checker(list(range(-1, -6, -1)))
checker([0])
checker([randrange(-5000, 5001) for _ in range(100)])