import unittest
import os
from grader import *

CURRENT_FOLDER = os.path.dirname(__file__)

dynamic_tests = []
def dyn_test(f):
    " Create a dynamic test which is called by Tests class automatically "
    dynamic_tests.append((f.__name__, f))
    return f

@dyn_test
def stdin_stdout_available(module):
    assert hasattr(module, "stdin")
    assert hasattr(module, "stdout")

@dyn_test
def module_availability(module):
    " module.module should be available after no more reads "
    module.stdin.write("Karl")
    assert hasattr(module, "module")

@dyn_test
def stdout_read(module):
    module.stdin.write("Karl")
    stdout = module.stdout.read()
    assert stdout == "Hi, Karl\n", stdout

@dyn_test
def function_call(m):
    m.stdin.write("Karl")
    assert m.module.add_one(9) == 10

@dyn_test
def stdout_new(m):
    m.stdin.write("Karl")
    old = m.stdout.read() # reset stdout
    m.module.add_one(193)
    assert(m.stdout.new() == "Got 193\n")


class Tests(unittest.TestCase):
    def setUp(self):
        self.tester = Tester("tested_module", working_dir=CURRENT_FOLDER)

    def run_test(self, test_function):
        #print(test_function.__name__)
        self.tester.test(test_function)
        success, errors = self.tester.runTest(test_function.__name__, "tester")
        assert success, errors

    def tester_initialization(self):
        self.assertEqual(len(self.tester.tests), 0)

    def tester_test_decorator_adds_to_tests(self):
        @self.tester.test
        def some_test(m): pass

        self.assertEqual(len(self.tester.tests), 1)


for test_name, test_function in dynamic_tests:
    setattr(Tests, "test_"+test_name, 
        lambda self, t=test_function: self.run_test(t))