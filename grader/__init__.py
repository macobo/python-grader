## TODO: How to we validate that our vital components arent 
## overwritten by user code?

import sys
import os
import subprocess
import itertools
from textwrap import dedent

CURRENT_FOLDER = os.path.dirname(__file__)


def runCode(code, working_dir=None):
    if working_dir is None: 
        working_dir = os.getcwd()
    subproc = subprocess.Popen(
        ["python3", "-c", code], cwd=working_dir, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = subproc.communicate()
    return {
        "stdout": stdout,
        "stderr": stderr,
        "status": subproc.returncode
    }

class Tester:
    def __init__(self, testedProgramPath = None, working_dir = None):
        if testedProgramPath is None and len(sys.argv) > 1:
            testedProgramPath = sys.argv[1][:-3]

        self.testedProgramPath = testedProgramPath
        self.working_dir = working_dir
        self.tests = {}
        self.test_names = []

    def test(self, test_function):
        " decorator for tests "
        name = test_function.__name__
        self.tests[name] = test_function
        self.test_names.append(name)
        return test_function


    def runTest(self, test_function_name, tester_module = None): 
        """ Runs the test, returning a tuple of (success, results).
            Success is a boolean flag indicating if the test was a success,
            results is a dictionary containing stdout and stderr of run.

            If tester_module is not provided, current program is used. """
        assert test_function_name in self.test_names, "no test named "+test_function_name
        if not tester_module:
            tester_module = sys.argv[0][:-3]

        with open(os.path.join(CURRENT_FOLDER, "execution_base.py")) as f:
            code = f.read()

        code += dedent("""
        
        #test_function_code
        try:
            from {tester_module} import {test_function_name}
        except ImportError as e:
            sys.__stderr__.write("Is {test_function_name} global and importable?\\n")
            raise

        m = Module("{user_program_path}")
        {test_function_name}(m)

        #sys.__stdout__.write("Test {test_function_name} completed successfully.\\n")
        """)
        code = code.format(
            user_program_path=self.testedProgramPath,
            test_function_name=test_function_name,
            tester_module=tester_module
        )
        #sprint(code)
        results = runCode(code, self.working_dir)
        results["success"] = bool(1-results["status"])
        return results["success"], results

    def allTestResults(self):
        return [(test_name, self.runTest(test_name)) for test_name in self.test_names]


def testAll(tester):
    for test_name, (success, errors) in tester.allTestResults():
        if success:
            print("Test {test_name} completed successfully!".format(**locals()))
        else:
            print("Test {test_name} failed:\n{errors}".format(**locals()))