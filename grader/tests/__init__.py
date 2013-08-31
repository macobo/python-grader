import unittest
import macropy.activate

def test_suite(suites=[], cases=[]):
    new_suites = [x.Tests for x in suites]
    new_cases = [unittest.makeSuite(x.Tests) for x in cases]
    return unittest.TestSuite(new_cases + new_suites)

from . import core_tester
from . import solution_tester
from . import feedback_utils_tester
from . import timing_tester
from . import timeout_tester
Tests = test_suite(cases=[
   core_tester,
   solution_tester,
   feedback_utils_tester,
   timing_tester,
   timeout_tester
], suites=[
    
])
