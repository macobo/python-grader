"""
Test existing solution/tester pairs, basically regression tests.
"""

import unittest
import os
import sys
import importlib
import grader
import json

CURRENT_FOLDER = os.path.dirname(__file__)
SOLUTION_FOLDER = os.path.join(os.path.dirname(os.path.dirname(CURRENT_FOLDER)), "tasks")

sys.path.append(SOLUTION_FOLDER)

tasks_json = json.loads(open(os.path.join(SOLUTION_FOLDER, "tasks.json")).read())
# list of existing solution-tester pairs
# (tester_module, solution_module)
existing_tests = [
    (task["tester"], task["solution"]) for unit in tasks_json.values() 
                                       for task in unit.values()]

class Tests(unittest.TestCase):
    def run_tester(self, tester_module, solution_module, working_dir=SOLUTION_FOLDER):
        grader.reset()
        # load tests from tester_module
        importlib.import_module(tester_module)

        grader.configure(
            user_program_module = solution_module,
            tester_module = tester_module,
            working_dir = working_dir)

        for test_name, (success, results) in grader.allTestResults():
            assert success, results["stderr"]


def runner(tester_module, solution_module):
    return lambda self: self.run_tester(tester_module, solution_module)

for tester_module, solution_module in existing_tests:
    setattr(Tests, "test_"+solution_module+"_with_"+tester_module, 
            runner(tester_module, solution_module))