import os
import json
import inspect
#from textwrap import dedent
from functools import wraps
from collections import OrderedDict
from .code_runner import runTester
from .utils import beautifyDescription

CURRENT_FOLDER = os.path.dirname(__file__)

testcases = OrderedDict()

def reset():
    " resets settings and loaded tests "
    testcases = OrderedDict()


def test(test_function):
    """ Decorator for a test. The function should take a single argument which
        is the object containing stdin, stdout and module (the globals of users program).

        The function name is used as the test name, which is a description for the test 
        that is shown to the user. If the function has a docstring, that is used instead.

        Raising an exception causes the test to fail, the resulting stack trace is
        passed to the user. """
    name = test_function.__name__
    if inspect.getdoc(test_function):
        name = beautifyDescription(inspect.getdoc(test_function))
    testcases[name] = test_function

    @wraps(test_function)
    def wrapper(module, *args, **kwargs):
        if module.caughtException:
            raise module.caughtException
        result = test_function(module, *args, **kwargs)
        if module.caughtException:
            raise module.caughtException
        return result
    return wrapper


def test_module(tester_module, user_module, print_result = False, working_dir = None):
    results = runTester(tester_module, user_module, working_dir)
    if print_result:
        print(json.dumps(results, indent=4))
    return results
