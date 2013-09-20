import os
import subprocess
from .utils import tempModule, load_json


def runTester(tester_module, user_module, working_dir=None):
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


def _test_subproc(test_index, tester_module, user_module, working_dir=None):
    if working_dir is None: 
        working_dir = os.getcwd()

    code = "import macropy.activate; from grader import execution_base as e; "
    code += "e.call_test_function("+str(test_index)+", '"+tester_module+"', '"+user_module+"')"
    subproc = subprocess.Popen(
        ['python3', '-c', code], 
        cwd=working_dir, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return subproc
