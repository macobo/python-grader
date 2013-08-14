## TODO: How to we validate that our vital components arent 
## overwritten by user code?

import sys
import os
from textwrap import dedent
from functools import wraps

from .code_runner import runCode
from .feedback_utils import *

CURRENT_FOLDER = os.path.dirname(__file__)

class Tester:
    def __init__(self, user_program_module=None, tester_module=None, working_dir=None):
        if user_program_module is None and len(sys.argv) > 1:
            user_program_module = os.path.splitext(sys.argv[1])[0]
        if tester_module is None:
            # take the program name as the tester module
            tester_module = os.path.splitext(sys.argv[0])[0]
        self.user_program_module = user_program_module
        self.tester_module = tester_module
        self.working_dir = working_dir
        self.tests = {}
        self.test_names = []


    def test(self, test_function):
        " decorator for tests "
        name = test_function.__name__
        self.tests[name] = test_function
        self.test_names.append(name)

        @wraps(test_function)
        def wrapper(module, *args, **kwargs):
            if module.caughtException:
                raise module.caughtException
            result = test_function(module, *args, **kwargs)
            if module.caughtException:
                raise module.caughtException
            return result
        return wrapper


    def runTest(self, test_function_name): 
        """ Runs the test, returning a tuple of (success, results).
            Success is a boolean flag indicating if the test was a success,
            results is a dictionary containing stdout and stderr of run.

            If tester_module is not provided, current program is used. """
        assert test_function_name in self.test_names, "no test named "+test_function_name

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
            user_program_module=self.user_program_module,
            test_function_name=test_function_name,
            tester_module=self.tester_module
        )
        results = runCode(code, self.working_dir)
        results["success"] = bool(1-results["status"])
        return results["success"], results


    def allTestResults(self):
        for test_name in self.test_names:
            yield test_name, self.runTest(test_name)


def testAll(tester):
    for test_name, (success, errors) in tester.allTestResults():
        if success:
            print("Test {test_name} completed successfully!".format(**locals()))
        else:
            print("Test {test_name} failed:\n{errors}".format(**locals()))