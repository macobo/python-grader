# abiline.py
from grader import *

def _create_generator(tester, default_description):
    def _register(*args, description = default_description):
        description = description.format(*args)
        
        @test
        @set_description(description)
        def testcase(m):
            tester(m, *args)
            
    return _register
        

def test_generator(description):
    def _register(tester):
        return _create_generator(tester, description)
    return _register