""" 
Executed when using `python -m grader <tester_path> <solution_path> [<other_files>...]`.

Tests the module and prints the results (json) to console.
"""
import os
import argparse

def is_valid_path(path):
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        raise argparse.ArgumentTypeError("{0} does not exist".format(abs_path))
    return abs_path

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('tester_path', type=is_valid_path)
parser.add_argument('solution_path', type=is_valid_path)
parser.add_argument('assets', type=is_valid_path, nargs="*")

parser.add_argument('-c', '--test-runner', 
    default=DEFAULT_TESTCASE_RUNNER,
    help="Command to run to run a test within a sandbox")

args = parser.parse_args()

from . import *
from .utils import AssetFolder

assets = AssetFolder(args.tester_path, args.solution_path, args.assets)

try:
    test_module(assets.tester_path, assets.solution_path, print_result=True)
finally:
    assets.remove()