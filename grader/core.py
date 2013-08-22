import os
import inspect
from textwrap import dedent
from functools import wraps
from collections import defaultdict, OrderedDict

from .code_runner import runCode

CURRENT_FOLDER = os.path.dirname(__file__)

settings = defaultdict(lambda:None)
testcases = OrderedDict()

def reset():
    " resets settings and loaded tests "
    global settings, testcases, testcase_names  
    settings = defaultdict(lambda:None)
    testcases = OrderedDict()


def configure(**extra_settings):
    settings.update(**extra_settings)


def test(test_function):
    " decorator for tests "
    name = test_function.__name__
    if inspect.getdoc(test_function):
        name = inspect.getdoc(test_function)
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


def runTest(test_function_name, **extra_settings): 
    """ Runs the test, returning a tuple of (success, results).
        Success is a boolean flag indicating if the test was a success,
        results is a dictionary containing stdout and stderr of run.

        If tester_module is not provided, current program is used. """
    
    configure(**extra_settings)
    assert settings["user_program_module"] is not None
    assert settings["tester_module"] is not None
    assert test_function_name in testcases, "no test named "+test_function_name

    with open(os.path.join(CURRENT_FOLDER, "execution_base.py")) as f:
        code = f.read()

    code += dedent("""
    import grader
    import {tester_module}

    m = Module("{user_program_module}")
    #sys.__stdout__.write(str(grader.testcases))
    grader.testcases["{test_function_name}"](m)

    #sys.__stdout__.write("Test {test_function_name} completed successfully.\\n")
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
    for test_name in testcases:
        yield test_name, runTest(test_name)