import unittest

def test_suite(suites=[], cases=[]):
    new_suites = [x.Tests for x in suites]
    new_cases = [unittest.makeSuite(x.Tests) for x in cases]
    return unittest.TestSuite(new_cases + new_suites)

from . import tester
Tests = test_suite(cases=[
   tester
], suites=[
    
])
