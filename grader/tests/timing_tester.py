import unittest
import grader
import os

CURRENT_FOLDER = os.path.dirname(__file__)

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
            tester_module = "timing_tester",
            user_module = "_helper_timing_module",
            working_dir = CURRENT_FOLDER
        )["results"]

    def find_result(self, function):
        test_name = grader.get_test_name(function)
        result = next(filter(lambda x: x["description"] == test_name, self.results))
        return result

    def run_test(self, test_function):
        result = self.find_result(test_function)
        assert result["success"], result

    @unittest.skip("tbd (#4)")
    def test_timing_issue(self):
        self.run_test(timing_issue_test)