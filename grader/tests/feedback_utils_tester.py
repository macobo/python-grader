import unittest
import textwrap
from grader.feedback_utils import *

def dedent(str):
    return textwrap.dedent(str).strip()

class Tests(unittest.TestCase):
    def test_require_contains_happy_str(self):
        require_contains("123456", "345")

    def test_require_contains_fail_str(self):
        with self.assertRaises(AssertionError) as err:
            require_contains("123456", "335")
        self.assertEquals(str(err.exception), dedent("""
            Expected 335 to be in input.
            input was:
              123456
        """))