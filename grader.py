## TODO: How to we validate that our vital components arent 
## overwritten by user code?

import os
import json
import inspect
import subprocess
import itertools
from textwrap import dedent
from pprint import pprint


CURRENT_FOLDER = os.path.dirname(__file__)


def runCode(code, globals=None):
    if globals is None: globals = dict()
    #stdin = bytes(json.dumps([code, globals]), "ascii")
    #print(stdin)
    subproc = subprocess.Popen(
        ["python3", "-c", code], cwd=os.getcwd(), stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = subproc.communicate()
    return {
        "stdout": stdout,
        "stderr": stderr,
        "status": subproc.returncode
    }


def dropDecorators(sourceCode):
    lines = sourceCode.split("\n")
    predicate = lambda line: line.rstrip()[0] == "@"
    return "\n".join(itertools.dropwhile(predicate, lines))


class Tester:
    def __init__(self, testedProgramPath):
        self.testedProgramPath = testedProgramPath
        self.tests = {}

    def test(self, test_function):
        name = test_function.__name__
        self.tests[name] = test_function

    def _runTest(self, test_function_code, test_function_name): 
        code = open(os.path.join(CURRENT_FOLDER, "execution_base.py")).read()
        code += dedent("""
        m = Module("{user_program_path}")

        {test_function_code}

        {test_function_name}(m)

        sys.__stdout__.write("Test {test_function_name} completed successfully.\\n")
        """)
        code = code.format(
            user_program_path=self.testedProgramPath,
            test_function_name=test_function_name,
            test_function_code=test_function_code
        )
        results = runCode(code)
        pprint(results)
        return bool(1-results["status"]), results["stderr"]


    def testAll(self):
        for key, test_function in self.tests.items():
            test_function_code = dropDecorators(inspect.getsource(test_function))
            test_name = test_function.__name__
            success, errors = self._runTest(test_function_code, test_name)
            if success:
                print("Test {test_name} completed successfully!".format(**locals()))
            else:
                print("Test {test_name} failed:\n{errors}".format(**locals()))
