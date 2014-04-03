"""
Executed when using `python -m grader <tester_path> <solution_path> [<other_files>...]`.

Tests the module and prints the results (json) to console.
"""
import os
import argparse

from . import *
from .utils import dump_json


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
    if runner in SANDBOXES:
        return runner
    raise argparse.ArgumentTypeError("Test runner {0} does not exist".format(runner))

parser = argparse.ArgumentParser(description='Test a program.')
parser.add_argument('tester_path', type=is_valid_path)
parser.add_argument('solution_path', type=is_valid_path)
parser.add_argument('assets', type=is_valid_path, nargs="*")
parser.add_argument('-s', '--sandbox',
                    dest="runner_cmd",
                    default=None,
                    type=valid_runner,
                    help="sandbox starting command")


args = parser.parse_args()

result = test_module(
    args.tester_path,
    args.solution_path,
    args.assets,
    sandbox_cmd=args.runner_cmd
)
print(dump_json(result))
