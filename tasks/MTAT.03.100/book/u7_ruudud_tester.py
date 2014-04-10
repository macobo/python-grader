from grader import *
from helpers import *

@test_generator("Ruudud kuni {0}")
def create_test(m, ylemine, on_range=False):
    m.stdout.reset()
    m.stdin.put(ylemine)
    
    output = m.stdout.read()
    
    for i in range(1, ylemine+1):
        assert str(i**2) in output, (
            "Number {} peaks esinema väljundis.\n"
            "Programmi väljund:\n{}"
        ).format(i**2, output)
        
    if ylemine < 1:
        assert output.strip() == "", (
            "Väljund peaks olema tühi, oli:\n{}"
            .format(output))
            
create_test(10)
create_test(1)
create_test(100)
create_test(-1)
