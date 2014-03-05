import unittest
import os
import grader

CURRENT_FOLDER = os.path.dirname(__file__)
HELPERS_FOLDER = os.path.join(CURRENT_FOLDER, "helpers")

def test_generator(name, fun):
    @grader.test
    def some_test(m):
        assert name != fun()
    grader.setDescription(some_test, name)
    #print(grader.testcases)

test_generator("some-description", lambda: 1)
test_generator("other", lambda: 2)
test_generator("fail", lambda: "fail")

class Tests(unittest.TestCase):
    tester_module = os.path.join(HELPERS_FOLDER, "renaming_tester.py")
    user_module = os.path.join(HELPERS_FOLDER, "_helper_tested_module.py")

    @classmethod
    def setUpClass(cls):
        #grader.reset()
        cls.results = grader.test_module(
            tester_module = cls.tester_module,
            user_module = cls.user_module,
            working_dir = CURRENT_FOLDER
        )["results"]

    def find_result(self, test_name):
        result = next(filter(lambda x: x["description"] == test_name, self.results))
        return result

    def run_test(self, test_function):
        result = self.find_result(test_function)
        assert result["success"], result

    def test_initialization(self):
        names = sorted([x["description"] for x in self.results])
        assert len(names) == 3, names
        assert "other" in names
        assert "fail" in names
        assert "some_test" not in names
        assert not self.find_result("fail")["success"]