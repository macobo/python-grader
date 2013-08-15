import unittest
import os
import importlib
from grader import *

CURRENT_FOLDER = os.path.dirname(__file__)

# list of existing solution-tester pairs
# (tester_module, solution_module)
existing_tests = [
    ("intress_tester",   "intress_solution"),
    ("kypsisetort_test", "kypsisetort"),
    ("intress_tester_other",  "intress_solution")
]

class Tests(unittest.TestCase):
    def run_tester(self, tester_module, solution_module, working_dir=CURRENT_FOLDER):
        tester = importlib.import_module("grader.tests."+tester_module).t

        tester.user_program_module = solution_module
        tester.tester_module = tester_module
        tester.working_dir = working_dir

        for test_name, (success, results) in tester.allTestResults():
            assert success, results["stderr"]


def runner(tester_module, solution_module):  
    return lambda self: self.run_tester(tester_module, solution_module)

for tester_module, solution_module in existing_tests:
    setattr(Tests, "test_"+solution_module+"_with_"+tester_module, 
            runner(tester_module, solution_module))