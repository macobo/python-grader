from macropy.tracing import macros, require
from .core import *
from .feedback_utils import *

def io_test(description, writes, expected_read):
    def f(module):
        for write in writes:
            module.stdout.reset()
            module.stdin.write(write)
        require_contains(module.stdout.new(), expected_read)
    f.__doc__ = description
    return test(f)

def check_function(function_name, args, expected_result, description=None, check_globals=False):
    def f(m):
        assert hasattr(m, "module"), "Do not use input() in this solution"
        assert hasattr(m.module, function_name), "Please define the function with name "+function_name
        function = getattr(m.module, function_name)
        import sys; sys.__stdout__.write(str(dir(m.module)))
        require[function(*args) != expected_result]

    if description is None:
        description = function_name + "(" + ", ".join(map(repr,args)) + ") == "+repr(expected_result)
    f.__doc__ = description
    return test(f)