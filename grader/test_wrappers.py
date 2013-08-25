from macropy.tracing import macros, require
from .core import *
from .feedback_utils import *

def io_test(description, writes_list, expected_read):
    """ Tests whether after writing each element of writes_list to stdin we can find 
        expected_read in the resulting output.

        Note that this also tests whether the program is waiting for before each write 
        and that it's not after the last one."""
    
    def f(module):
        for write in writes_list:
            assert module.is_waiting_input(), "Did you forget to use input()?"
            module.stdout.reset()
            module.stdin.write(write)
        require_contains(module.stdout.new(), expected_read)
        assert not module.is_waiting_input(), "Make sure there isn't a stray input() after your code"
    setDescription(f, description)
    return test(f)

def check_function(function_name, args, expected_result, description=None):
    """ Tests that calling function with the given name exists and calling it with
        args gives expected_result.

        If description is given, it is used as test name, else the description will before
        similar to "Check add(1, 2, 3) == 6" """

    def f(m):
        assert hasattr(m, "module"), "Do not use input() in this solution"
        assert hasattr(m.module, function_name), "Please define the function with name "+function_name
        function = getattr(m.module, function_name)
        #import sys; sys.__stdout__.write(str(dir(m.module)))
        require[function(*args) == expected_result]

    if description is None:
        description = "Check " + function_name + "(" + ", ".join(map(repr,args)) + ") == "+repr(expected_result)
    setDescription(f, description)
    return test(f)