## TODO: How to we validate that our vital components arent 
## overwritten by user code?

import os
import json
import inspect
import subprocess
import itertools
from textwrap import dedent
from pprint import pprint


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
        code = dedent("""
        import sys
        def singleton(clazz, *args, **kwargs):
            return clazz(*args, **kwargs)

        @singleton
        class StdoutCapture:
            def __init__(self):
                self.output = []

            def write(self, b):
                self.output.append(b)

            def flush(self): pass
            def close(self): pass

            def get_output(self):
                return "".join(self.output)


        sys.stdout = StdoutCapture

        user_module = __import__("{user_program_path}")

        # write test method here
        # call test method - if it crashes, all's well
        {test_function_code}
        {test_function_name}(user_module)

        sys.__stdout__.write("Test {test_function_name} completed successfully.\\n")

        """)
        code = code.format(
            user_program_path=self.testedProgramPath,
            test_function_name=test_function_name,
            test_function_code=test_function_code
        )
        print(code)
        results = runCode(code)
        pprint(results)
        #print(results["stderr"])

    def testAll(self):
        for key, test_function in self.tests.items():
            test_function_code = dropDecorators(inspect.getsource(test_function))
            self._runTest(test_function_code, test_function.__name__)


a = Tester("b")

@a.test
def f(module):
    assert module.foobar(9) == 11

a.testAll()
