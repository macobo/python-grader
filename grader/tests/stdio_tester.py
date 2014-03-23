import unittest
import os
import grader

CURRENT_FOLDER = os.path.dirname(__file__)
HELPERS_FOLDER = os.path.join(CURRENT_FOLDER, "helpers")

# no i-o
# Too few writes -> timeout, error?
# as many writes -> success
# too many writes -> success

class Tests(unittest.TestCase):
    tester_path = os.path.join(CURRENT_FOLDER, "stdio_tester.py")
    solution_path = os.path.join(HELPERS_FOLDER, "_helper_stdio.py")

    @staticmethod
    def run_test(tester_path, solution_path):
        solution = os.path.join(HELPERS_FOLDER, solution_path)
        tester = os.path.join(HELPERS_FOLDER, tester_path)
        return grader.test_module(
            tester_path = tester,
            solution_path = solution
        )["results"]

    @classmethod
    def setUpClass(cls):
        cls.empty_module_results = cls.run_test('stdio_tester.py', '_helper_empty_module.py')
        cls.two_module_results = cls.run_test('stdio_tester.py', '_helper_two_read_module.py')

    def find_result(self, name, results):
        result = next(filter(lambda x: x["description"] == name, results))
        return result

    def test_no_io(self):
        result = self.find_result('no_writes', self.empty_module_results)
        assert result["success"], result

    @unittest.skip("")
    def test_no_io_extra_write(self):
        result = self.find_result('two_writes', self.empty_module_results)
        assert result["success"], result

    def test_two_io(self):
        result = self.find_result('no_writes', self.two_module_results)
        assert result["success"], result

    def test_two_io_exact_writes(self):
        result = self.find_result('two_writes', self.two_module_results)
        assert result["success"], result
