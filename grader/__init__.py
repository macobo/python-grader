## TODO: How to we validate that our vital components arent 
## overwritten by user code?

import sys
import os
from textwrap import dedent

from .code_runner import runCode
from .feedback_utils import *

CURRENT_FOLDER = os.path.dirname(__file__)

class Tester:
    def __init__(self, user_program_path=None, tester_module=None, working_dir=None):
        if user_program_path is None and len(sys.argv) > 1:
            user_program_path = sys.argv[1][:-3]
        if tester_module is None:
            # take the program name as the tester module
            tester_module = sys.argv[0][:-3]
        self.user_program_path = user_program_path
        self.tester_module = tester_module
        self.working_dir = working_dir
        self.tests = {}
        self.test_names = []


    def test(self, test_function):
        " decorator for tests "
        name = test_function.__name__
        self.tests[name] = test_function
        self.test_names.append(name)
        return test_function


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

        m = Module("{user_program_path}")
        {test_function_name}(m)

        sys.__stdout__.write("Test {test_function_name} completed successfully.\\n")
        """)
        code = code.format(
            user_program_path=self.user_program_path,
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