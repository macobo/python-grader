import os
import subprocess
from .utils import tempModule

def runCode(code, working_dir=None):
    if working_dir is None: 
        working_dir = os.getcwd()

    with tempModule(code, working_dir) as module_name:
        subproc = subprocess.Popen(
            ['python3', '-c', 'import macropy.activate; import '+module_name], 
            cwd=working_dir, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = subproc.communicate()
    #print(subproc.returncode, stdout)
    #print(stderr.decode("utf-8"))

    return {
        "stdout": stdout.decode("utf-8"),
        "stderr": stderr.decode("utf-8"),
        "status": subproc.returncode
    }