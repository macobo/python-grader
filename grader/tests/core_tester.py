import unittest
import os
import grader
from grader.utils import create_file, delete_file
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
    #module.stdin.write("Karl")

@dyn_test
def module_availability(module):
    # module.module should be available after no more reads
    module.stdin.write("Karl")
    assert hasattr(module, "module")

@dyn_test
def stdout_read(module):
    module.stdin.write("Karl")
    stdout = module.stdout.read()
    assert stdout == "Hi, Karl 6\n", stdout


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

@dyn_test
def io_within_function(m):
    m.stdin.write("Karl")
    m.stdout.reset()
    m.stdin.write("Hello world")
    m.module.askInput()
    assert "Hello world" in m.stdout.read(), m.stdout.read()

@grader.test
def doc_only_function(m):
    "this function should have the docstring as its name in grader"

@grader.test
def multiline_doc_function(m):
    """This function should have a multiline docstring 
        as its name in grader
    """

@grader.test
@grader.before_test(create_file('hello.txt', 'Hello world!'))
@grader.after_test(delete_file('hello.txt'))
def hook_test(m):
    with open(os.path.join(CURRENT_FOLDER, 'hello.txt')) as file:
        txt = file.read()
        assert txt == 'Hello world!', txt

@grader.test
def exceptions(m):
    m.stdin.write("Karl")
    m.module.raiseException("SomeAwesomeMessage")


class Tests(unittest.TestCase):
    tester_module = "core_tester"
    user_module = "_helper_tested_module"

    @classmethod
    def setUpClass(cls):
        grader.reset()
        cls.results = grader.test_module(
            tester_module = cls.tester_module,
            user_module = cls.user_module,
            working_dir = CURRENT_FOLDER
        )["results"]

    def find_result(self, function):
        test_name = grader.get_test_name(function)
        result = next(filter(lambda x: x["description"] == test_name, self.results))
        return result

    def run_test(self, test_function):
        result = self.find_result(test_function)
        assert result["success"], result

    def tester_initialization(self):
        self.assertTrue(len(grader.testcases) >= len(dynamic_tests) + 3)

    def test_docstring_added_as_test_name(self):
        import inspect
        self.assertIn(inspect.getdoc(doc_only_function), 
                    list(grader.testcases.keys()))

    def test_multiline_docstring(self):
        doc = "This function should have a multiline docstring as its name in grader"
        self.assertIn(doc, list(grader.testcases.keys()))

    def test_hooks(self):
        result = self.find_result(hook_test)
        assert result["success"], result
        assert not os.path.exists(os.path.join(CURRENT_FOLDER, "hello.txt"))

    def test_exceptions_cause_test_failure(self):
        result = self.find_result(exceptions)
        assert not result["success"]
        assert "SomeAwesomeMessage" in result["traceback"], result

    @unittest.skip("tbd")
    def test_trace_contains_file_lines(self):
        result = self.find_result(exceptions)
        assert not result["success"]
        trace = result["traceback"]
        # check if tester module trace is in
        self.assertIn('core_tester.py", line 92', trace)
        # check if user code gets a line
        self.assertIn('line 19 in raiseException', trace)


for test_name, test_function in dynamic_tests:
    setattr(Tests, "test_"+test_name, 
        lambda self, t=test_function: self.run_test(t))