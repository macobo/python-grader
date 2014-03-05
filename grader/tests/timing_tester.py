import unittest
import grader
import os

CURRENT_FOLDER = os.path.dirname(__file__)
HELPERS_FOLDER = os.path.join(CURRENT_FOLDER, "helpers")

@grader.test
def timing_issue_test(m):
    m.stdin.write("hello")
    m.stdin.write("world")
    assert "result" in m.stdout.read()


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        grader.reset()
        cls.results = grader.test_module(
            tester_path = os.path.join(CURRENT_FOLDER, "timing_tester.py"),
            solution_path = os.path.join(HELPERS_FOLDER, "_helper_timing_module.py"),
            runner_cmd = grader.DEFAULT_TESTCASE_RUNNER
        )["results"]

    def find_result(self, function):
        test_name = grader.get_test_name(function)
        result = next(filter(lambda x: x["description"] == test_name, self.results))
        return result

    def run_test(self, test_function):
        result = self.find_result(test_function)
        assert result["success"], result

    def test_timing_issue(self):
        self.run_test(timing_issue_test)