import os
import subprocess
import json
from .utils import tempModule, load_json


def runTester(tester_module, user_module, working_dir=None):
    # TODO: security
    if working_dir is None: 
        working_dir = os.getcwd()

    code = "import macropy.activate; from grader import execution_base as e; "
    code += "e.test_module('"+tester_module+"', '"+user_module+"', True)"
    subproc = subprocess.Popen(
        ['python3', '-c', code], 
        cwd=working_dir, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = subproc.communicate()
    return load_json(stdout.decode('utf-8'))