import sys
import os
import importlib

from . import *

tester_module   = os.path.splitext(sys.argv[1])[0]
solution_module = os.path.splitext(sys.argv[2])[0]

configure(
    tester_module = tester_module,
    user_program_module = solution_module
)

# load tests from tester_module
importlib.import_module(tester_module)

testAll(print_result = True)