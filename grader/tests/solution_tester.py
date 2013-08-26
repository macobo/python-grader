"""
Test existing solution/tester pairs, basically regression tests.
"""

import unittest
import os
import sys
import grader
from grader.utils import load_json, dump_json

CURRENT_FOLDER = os.path.dirname(__file__)
SOLUTION_FOLDER = os.path.join(os.path.dirname(os.path.dirname(CURRENT_FOLDER)), "tasks")

sys.path.append(SOLUTION_FOLDER)

tasks_json = load_json(open(os.path.join(SOLUTION_FOLDER, "tasks.json")).read())
# list of existing solution-tester pairs
# (tester_module, solution_module)
existing_tests = [
    (task["tester"], task["solution"]) for unit in tasks_json.values() 
                                       for task in unit.values()]

class Tests(unittest.TestCase):
    def run_tester(self, tester_module, solution_module, working_dir=SOLUTION_FOLDER):
        grader.reset()
        results = grader.test_module(tester_module, solution_module, working_dir)

        for result in results["results"]:
            assert result["success"], dump_json(results)


def runner(tester_module, solution_module):
    return lambda self: self.run_tester(tester_module, solution_module)

for tester_module, solution_module in existing_tests:
    setattr(Tests, "test_"+solution_module+"_with_"+tester_module, 
            runner(tester_module, solution_module))