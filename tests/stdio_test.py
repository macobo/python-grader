import sys
import os
directory = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, directory)
sys.path.insert(0, os.path.dirname(directory))
from grader import get_module

def test_module_creation():
    module, stdin, stdout = get_module("fibo")
    
def test_stdin_write():
    module, _in, _out = get_module("fibo")
    _in.write("1234")
    assert module.echo() == "1234"
    #_in.write("something-else")
    assert module.echo() == "something-else"