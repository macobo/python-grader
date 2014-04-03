""" Wrappers to make writing tests easier """

#from macropy.tracing import macros, require
from .core import *
from .utils import *
from .assertions import *
from .decorators import *


def io_test(description, writes_list, expected_read):
    """ Tests whether after writing each element of writes_list to stdin we
        can find expected_read in the resulting output.

        Note that this also tests whether the program is waiting for before
        each write and that it's not after the last one. """
    
    def f(module):
        for i, write in enumerate(writes_list):
            assert not module.finished, \
                "Did you forget to use input()? Writes so far: %s" % writes_list[:i]
            module.stdout.reset()
            module.stdin.write(write)
        require_contains(module.stdout.new(), expected_read)
        assert module.finished, \
            "Make sure there isn't a stray input() after your code"
    setDescription(f, description)
    return test(f)


def check_function(function_name, args, expected_result, description=None):
    """ Tests that calling function with the given name exists and calling it
        with args gives expected_result.

        If description is given, it is used as test name, else the description
        will before similar to "Check add(1, 2, 3) == 6" """

    def f(m):
        assert hasattr(m, "module"), "Do not use input() in this solution"
        assert hasattr(m.module, function_name), \
            "Please define the function with name " + function_name
        function = getattr(m.module, function_name)
        assertEquals(function(*args), expected_result)

    if description is None:
        description = "Check " + function_name + \
            "(" + ", ".join(map(repr, args)) + ") == " + repr(expected_result)
    setDescription(f, description)
    return test(f)


def set_description(d):
    def inner(f):
        setDescription(f, d)
        return f
    return inner


def test_cases(test_args, description=None, **arg_functions):
    if description is None:
        description = ", ".join(str(i)+"={"+key+"}" for i, key in enumerate(test_args[0]))

    def calc_function_kwargs(values):
        out = {}
        for k, fun in arg_functions.items():
            out[k] = fun(*values)
        return out

    def _inner(function):
        # remove from tests if there
        def make_f(args, kw):
            @test
            @set_description(description.format(*args, **kw))
            def _inner(m):
                function(m, *args, **kw)

        for args in test_args:
            if not isinstance(args, list) and not isinstance(args, tuple):
                args = [args]
            kw = calc_function_kwargs(args)
            make_f(args, kw)
    return _inner
