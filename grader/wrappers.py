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



def test_cases(test_args, description=None, **arg_functions):
    """ Decorator for generating multiple tests with additional arguments.

        `test_args` - list of lists - each element of the outer list should be
                        extra arguments to call decorated function with.
        `description` - String or function, gets passed in keywords and arguments.
        `arg_functions` - function. Gets called with a value from test_args and the
                        returned value is added as a keyword to test and description.

        Example usage:

        @test_cases(
            [[1, 2], [3, 4]],
            expected=lambda x, y: x+y,
            description="Adding {0} and {1} should yield {expected}
        )
        def t(m, a, b, expected):
            # a and b are either 1 and 2 or 3 and 4
            assert a + b == expected
    """

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
            if is_function(description):
                test_desc = description(*args, **kw)
            else:
                test_desc = description.format(*args, **kw)

            @test
            @set_description(test_desc)
            def _inner(m, *extra_args, **extra_kw):
                _kw = dict(list(kw.items()) + list(extra_kw.items()))
                _args = list(args) + list(extra_args)
                function(m, *_args, **_kw)
            return _inner

        tests = []
        for args in test_args:
            if not isinstance(args, list) and not isinstance(args, tuple):
                args = [args]
            kw = calc_function_kwargs(args)
            tests.append(make_f(args, kw))
        return tests

    return _inner
