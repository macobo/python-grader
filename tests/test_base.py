import unittest
import os
import grader

CURRENT_FOLDER = os.path.dirname(__file__)
HELPERS_FOLDER = os.path.join(CURRENT_FOLDER, "helpers")


class GraderTestBase(unittest.TestCase):
    @staticmethod
    def run_test(tester_path, solution_path):
        solution = os.path.join(HELPERS_FOLDER, solution_path)
        tester = os.path.join(CURRENT_FOLDER, tester_path)
        return grader.test_module(
            tester_path = tester,
            solution_path = solution
        )["results"]

    @staticmethod
    def run_code(tester_code, solution_code):
        return grader.test_code(tester_code, solution_code)["results"]

    def find_result(self, name, results):
        result = next(filter(lambda x: x["description"] == name, results))
        return result
