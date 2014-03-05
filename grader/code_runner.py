import os
import subprocess
from .utils import load_json

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
