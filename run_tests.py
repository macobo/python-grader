import unittest
import sys

from grader.tests import Tests

results = unittest.TextTestRunner().run(Tests)
if results.errors or results.failures:
    sys.exit(1)