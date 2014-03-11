"""
Executed when using `python -m grader <tester_path> <solution_path> [<other_files>...]`.

Tests the module and prints the results (json) to console.
"""
import os
import argparse

from . import *
from .asset_management import AssetFolder


def is_valid_path(path, raiseError=True):
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        if raiseError:
            raise argparse.ArgumentTypeError("{0} does not exist".format(abs_path))
        return None
    return abs_path


def valid_runner(runner):
    path = is_valid_path(runner, False)
    if path:
        return path
    if runner in TESTCASE_RUNNERS:
        return TESTCASE_RUNNERS[runner]
    raise argparse.ArgumentTypeError("Test runner {0} does not exist".format(runner))

parser = argparse.ArgumentParser(description='Test a program.')
parser.add_argument('tester_path', type=is_valid_path)
parser.add_argument('solution_path', type=is_valid_path)
parser.add_argument('assets', type=is_valid_path, nargs="*")
parser.add_argument('-c', '--test-runner',
                    dest="runner_cmd",
                    default=DEFAULT_TESTCASE_RUNNER,
                    type=valid_runner,
                    help="Command to run to run a test within a sandbox")

args = parser.parse_args()

assets = AssetFolder(args.tester_path, args.solution_path, args.assets)

try:
    test_module(
        assets.tester_path,
        assets.solution_path,
        print_result=True,
        runner_cmd=args.runner_cmd)
finally:
    pass
    #assets.remove()
