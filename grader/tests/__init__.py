import unittest
#import macropy.activate

def test_suite(suites=[], cases=[]):
    new_suites = [x.Tests for x in suites]
    new_cases = [unittest.makeSuite(x.Tests) for x in cases]
    return unittest.TestSuite(new_cases + new_suites)

from . import datastructures_tester
from . import core_tester
from . import assertions_tester
from . import timing_tester
from . import timeout_tester
from . import renaming_tester
from . import utils_tester
from . import stdio_tester


cases = [
  utils_tester,
  datastructures_tester,
  core_tester,
  assertions_tester,
  timing_tester,
  timeout_tester,
  renaming_tester,
  stdio_tester
]

import os
CURRENT_FOLDER = os.path.dirname(__file__)
SOLUTION_FOLDER = os.path.join(os.path.dirname(os.path.dirname(CURRENT_FOLDER)), "tasks")
if os.path.exists(os.path.join(SOLUTION_FOLDER, "tasks.json")):
    from . import solution_tester
    #cases.insert(1, solution_tester)
else:
    print("Failed to open tasks/tasks.json. Did you do git submodule update?")
    
Tests = test_suite(cases=cases)
