import unittest
import sys
#import macropy.activate

def test_suite(suites=[], cases=[]):
    new_suites = [x.Tests for x in suites]
    new_cases = [unittest.makeSuite(x.Tests) for x in cases]
    return unittest.TestSuite(new_cases + new_suites)

if __name__ == "__main__":
    cases = [
        __import__("utils_tester"),
        __import__("datastructures_tester"),
        __import__("core_tester"),
        __import__("assertions_tester"),
        __import__("timing_tester"),
        __import__("timeout_tester"),
        __import__("renaming_tester"),
        __import__("stdio_tester"),
        __import__("exception_tester"),
        __import__("extensions_ast"),
        __import__("external_interface"),
        __import__("wrappers_tester")
    ]
    # import os
    # CURRENT_FOLDER = os.path.dirname(__file__)
    # SOLUTION_FOLDER = os.path.join(os.path.dirname(os.path.dirname(CURRENT_FOLDER)), "tasks")
    # if os.path.exists(os.path.join(SOLUTION_FOLDER, "tasks.json")):
    #     from . import solution_tester
    #     #cases.insert(1, solution_tester)
    # else:
    #     print("Failed to open tasks/tasks.json. Did you do git submodule update?")

    Tests = test_suite(cases=cases)
    results = unittest.TextTestRunner().run(Tests)
    if results.errors or results.failures:
        sys.exit(1)
