""" 
Executed when using `python -m grader <tester_module> <solution_module>`.

Tests the module and prints the results (json) to console.
"""
import sys
import os

from . import *
from .utils import AssetFolder

tester_module, solution_module = sys.argv[1:3]

assets = AssetFolder(tester_module, solution_module)

try:
    #print("TESTING", assets)
    test_module(assets.tester_path, assets.solution_path, print_result=True)
finally:
    #print("Removing temp folder")
    assets.remove()