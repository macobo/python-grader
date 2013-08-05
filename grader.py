import inspect
import os
import subprocess
import json
from pprint import pprint

class Tester:
    def __init__(self, programName):
        self.programName = programName
        self.tests = {}

    def test(self, test_function):
        name = test_function.__name__
        self.tests[name] = test_function

    def _runTest(self, test_function):
        function_code = inspect.getsource(test_function)
        function_name = test_function.__name__
        code = ""
        #code = "{}\n{}(__import__({}))".format(function_code, 
        #                                        function_name, 
        #                                        self.programName)
        results = runCode(code)
        pprint(results)
        print(results["stderr"])

    def testAll(self):
        for key, test_function in self.tests.items():
            self._runTest(test_function)

def runCode(code, globals=None):
    if globals is None: globals = dict()
    stdin = bytes(json.dumps([code, globals]), "ascii")
    print(stdin)
    subproc = subprocess.Popen(
        ["python3","test.py"], cwd=os.getcwd(), stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = subproc.communicate(stdin)
    return {
        "stdout": stdout,
        "stderr": stderr,
        "status": subproc.returncode
    }


a = Tester("b")


@a.test
def f(module):
    module.a == 3
    import sys
    sys.stderr.write("blah")

a.testAll()
