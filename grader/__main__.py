import sys
import os

from . import *

tester_module   = os.path.splitext(sys.argv[1])[0]
solution_module = os.path.splitext(sys.argv[2])[0]

test_module(tester_module, solution_module, print_result=True)