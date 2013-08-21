import sys
import os
from textwrap import dedent
from functools import wraps
from collections import defaultdict

from .code_runner import runCode

CURRENT_FOLDER = os.path.dirname(__file__)

settings = defaultdict(lambda:None)
testcases = {}
testcase_names = []

def reset():
    " resets settings and loaded tests "
    global settings, testcases, testcase_names  
    settings = defaultdict(lambda:None)
    testcases = {}
    testcase_names = []

def configure(**extra_settings):
    global settings
    settings.update(**extra_settings)
    if settings["user_program_module"] is None and len(sys.argv) > 1:
        settings["user_program_module"] = os.path.splitext(sys.argv[1])[0]
    if settings["tester_module"] is None:
        settings["tester_module"] = os.path.splitext(sys.argv[0])[0]


def test(test_function):
    " decorator for tests "
    name = test_function.__name__
    testcases[name] = test_function
    testcase_names.append(name)

    @wraps(test_function)
    def wrapper(module, *args, **kwargs):
        if module.caughtException:
            raise module.caughtException
        result = test_function(module, *args, **kwargs)
        if module.caughtException:
            raise module.caughtException
        return result
    return wrapper


def runTest(test_function_name, **extra_settings): 
    """ Runs the test, returning a tuple of (success, results).
        Success is a boolean flag indicating if the test was a success,
        results is a dictionary containing stdout and stderr of run.

        If tester_module is not provided, current program is used. """
    
    configure(**extra_settings)
    assert test_function_name in testcases, "no test named "+test_function_name

    with open(os.path.join(CURRENT_FOLDER, "execution_base.py")) as f:
        code = f.read()

    code += dedent("""
    
    try:
        from {tester_module} import {test_function_name}
    except ImportError as e:
        sys.__stderr__.write("Is {test_function_name} global and importable?\\n")
        raise

    m = Module("{user_program_module}")
    {test_function_name}(m)

    sys.__stdout__.write("Test {test_function_name} completed successfully.\\n")
    """)
    code = code.format(
        user_program_module=settings["user_program_module"],
        test_function_name=test_function_name,
        tester_module=settings["tester_module"]
    )
    results = runCode(code, settings["working_dir"])
    results["success"] = bool(1-results["status"])
    return results["success"], results


def allTestResults():
    for test_name in testcase_names:
        yield test_name, runTest(test_name)

# initialize settings, reset tests
reset()