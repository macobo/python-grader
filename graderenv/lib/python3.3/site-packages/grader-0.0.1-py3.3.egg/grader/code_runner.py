import os
import subprocess
from .utils import tempModule, load_json


def runTester(tester_module, user_module, working_dir=None):
    if working_dir is None: 
        working_dir = os.getcwd()

    #code = "import macropy.activate; from grader import execution_base as e; "
    code = "from grader import execution_base as e; "
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


def call_test(test_name, tester_module, user_module, working_dir=None, timeout=1):
    if working_dir is None: 
        working_dir = os.getcwd()

    #code = "import macropy.activate; from grader import execution_base as e; "
    code = "from grader import execution_base as e; "
    code += "e.call_test_function("+repr(test_name)+", '"+tester_module+"', '"+user_module+"')"
    try:
        stdout = subprocess.check_output(
            ["timeout", str(timeout), "python3", "-c", code], 
            cwd=working_dir)
    except subprocess.CalledProcessError as e:
        stdout = e.output
    return stdout.decode('utf-8')
