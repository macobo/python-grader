import unittest
import grader
import os

CURRENT_FOLDER = os.path.dirname(__file__)
HELPERS_FOLDER = os.path.join(CURRENT_FOLDER, "helpers")
TIMEOUT = 0.2

@grader.test
@grader.timeout(TIMEOUT)
def test_that_timeouts(m):
    from time import sleep
    sleep(2)

@grader.test
@grader.timeout(TIMEOUT)
def slow_function_timeout(m):
    # empty test - the test should fail since 
    # m.slow_function() takes too long
    m.module.slow_function()


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        grader.reset()
        cls.results = grader.test_module(
            tester_path = os.path.join(CURRENT_FOLDER, "timeout_tester.py"),
            solution_path = os.path.join(HELPERS_FOLDER, "_helper_timeout_module.py"),
            runner_cmd = grader.DEFAULT_TESTCASE_RUNNER
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

    def test_testing_function_timeout(self):
        result = self.find_result(test_that_timeouts)
        assert not result["success"], result
        assert "timeout" in result["traceback"].lower(), result

    def test_resulting_times_in_sensible_range(self):
        for test_ in [test_that_timeouts, slow_function_timeout]:
            name = grader.get_test_name(test_)
            result = self.find_result(test_)
            took = float(result["time"])
            assert took >= TIMEOUT and took < 2*TIMEOUT, result
