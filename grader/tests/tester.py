import unittest
import os
import grader
from macropy.tracing import macros, trace

CURRENT_FOLDER = os.path.dirname(__file__)

dynamic_tests = []
def dyn_test(f):
    " Create a dynamic test which is called by Tests class automatically "
    f = grader.test(f)
    dynamic_tests.append((f.__name__, f))
    return f

@dyn_test
def stdin_stdout_available(module):
    assert hasattr(module, "stdin")
    assert hasattr(module, "stdout")

@dyn_test
def module_availability(module):
    # module.module should be available after no more reads
    module.stdin.write("Karl")
    assert hasattr(module, "module")

@dyn_test
def stdout_read(module):
    module.stdin.write("Karl")
    stdout = module.stdout.read()
    assert stdout == "Hi, Karl\n", stdout


@dyn_test
def waiting_input_function(m):
    assert m.is_waiting_input()
    m.stdin.write("foo")
    assert not m.is_waiting_input()

@dyn_test
def function_call(m):
    m.stdin.write("Karl")
    assert m.module.add_one(9) == 10

@dyn_test
def stdout_new(m):
    m.stdin.write("Karl")
    m.stdout.reset() # reset stdout
    m.module.add_one(193)
    assert(m.stdout.new() == "Got 193\n")


@dyn_test
def trace_macro_available(m):
    m.stdin.write("Karl")
    m.stdout.reset() # reset stdout
    trace[1+2+3]
    n = m.stdout.new()
    assert "1+2 -> 3\n" in n, n
    assert "1+2+3 -> 6\n" in n, n

@grader.test
def doc_only_function(m):
    "this function should have the docstring as its name in grader"

@grader.test
def multiline_doc_function(m):
    """This function should have a multiline docstring 
        as its name in grader
    """




class Tests(unittest.TestCase):
    def setUp(self):
        grader.reset()
        grader.configure(
            user_program_module = "tested_module",
            tester_module = "tester",
            working_dir = CURRENT_FOLDER
        )

    def run_test(self, test_function):
        #print(test_function.__name__)
        grader.test(test_function)
        success, errors = grader.runTest(test_function.__name__)
        assert success, errors

    def tester_initialization(self):
        self.assertEqual(len(grader.testcases), len(dynamic_tests) + 2)

    def test_docstring_added_as_test_name(self):
        import inspect
        self.assertIn(inspect.getdoc(doc_only_function), 
                    list(grader.testcases.keys()))

    def test_multiline_docstring(self):
        doc = "This function should have a multiline docstring as its name in grader"
        self.assertIn(doc, list(grader.testcases.keys()))


for test_name, test_function in dynamic_tests:
    setattr(Tests, "test_"+test_name, 
        lambda self, t=test_function: self.run_test(t))