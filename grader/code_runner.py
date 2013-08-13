import os
import subprocess

def runCode(code, working_dir=None):
    if working_dir is None: 
        working_dir = os.getcwd()
    subproc = subprocess.Popen(
        ["python3", "-c", code], cwd=working_dir, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = subproc.communicate()
    return {
        "stdout": stdout,
        "stderr": stderr,
        "status": subproc.returncode
    }