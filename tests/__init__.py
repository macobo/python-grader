import unittest
import sys
#import macropy.activate

def test_suite(suites=[], cases=[]):
    new_suites = [x.Tests for x in suites]
    new_cases = [unittest.makeSuite(x.Tests) for x in cases]
    return unittest.TestSuite(new_cases + new_suites)

if __name__ == "__main__":
    import datastructures_tester
    import core_tester
    import assertions_tester
    import timing_tester
    import timeout_tester
    import renaming_tester
    import utils_tester
    import stdio_tester
    import exception_tester
    import extensions_ast
    import external_interface

    cases = [
        utils_tester,
        datastructures_tester,
        core_tester,
        assertions_tester,
        timing_tester,
        timeout_tester,
        renaming_tester,
        stdio_tester,
        exception_tester,
        extensions_ast,
        external_interface
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
