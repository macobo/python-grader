import unittest
import grader
import os

CURRENT_FOLDER = os.path.dirname(__file__)

@grader.test
def slow_function_timeout(m):
    # empty test - the test should fail since 
    # m.slow_function() takes too long
    m.module.slow_function()


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        grader.reset()
        cls.results = grader.test_module(
            tester_module = "timeout_tester",
            user_module = "_helper_timeout_module",
            working_dir = CURRENT_FOLDER
        )["results"]

    def find_result(self, function):
        test_name = grader.get_test_name(function)
        result = next(filter(lambda x: x["description"] == test_name, self.results))
        return result

    def run_test(self, test_function):
        result = self.find_result(test_function)
        assert result["success"], result

    def test_function_timeout(self):
        result = self.find_result(slow_function_timeout)
        assert not result["success"], result
        assert "timeout" in result["traceback"].lower(), result