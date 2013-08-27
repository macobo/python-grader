import os
import subprocess
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
    try:
        return load_json(stdout.decode('utf-8'))
    except:
        raise Exception(stdout.decode('utf-8') + "\n\n\n\n\n" + stderr.decode('utf-8'))