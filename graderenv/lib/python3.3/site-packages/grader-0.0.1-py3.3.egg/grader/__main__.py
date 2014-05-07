""" 
Executed when using `python -m grader <tester_module> <solution_module>`.

Tests the module and prints the results (json) to console.
"""
import sys
import os

from . import *

tester_module, solution_module = sys.argv[1:3]
#tester_module   = os.path.splitext(sys.argv[1])[0]
#solution_module = os.path.splitext(sys.argv[2])[0]

test_module(tester_module, solution_module, print_result=True)