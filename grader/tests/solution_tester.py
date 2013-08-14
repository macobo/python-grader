import unittest
import os
from os.path import join
import importlib
from grader import *

CURRENT_FOLDER = os.path.dirname(__file__)

# list of existing solution-tester pairs
# (tester_module, solution_path)
existing_tests = [
    ("intress_tester",   "intress_solution.py"),
    ("kypsisetort_test", "kypsisetort.py")
]

def strip_extension(path):
    if path[:-3] == ".py":
        return path[:-3]
    return path

class Tests(unittest.TestCase):
    def run_tester(self, tester_module, solution_path, working_dir=CURRENT_FOLDER):
        tester = importlib.import_module("grader.tests."+tester_module).t

        tester.user_program_path = solution_path
        tester.tester_module = tester_module
        tester.working_dir = working_dir

        tester.testedProgramPath = strip_extension(solution_path)
        for test_name, (success, results) in tester.allTestResults():
            assert success, (test_name, results)


def runner(tester, test_path):  
    return lambda self: self.run_tester(tester, test_path)

for tester_path, solution_path in existing_tests:
    setattr(Tests, "test_"+solution_path, 
            runner(tester_path, solution_path))