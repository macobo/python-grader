import os
import subprocess
import json
from .utils import tempModule


def runTester(tester_module, user_module, working_dir=None):
    if working_dir is None: 
        working_dir = os.getcwd()
    subproc = subprocess.Popen(
        ['python3', '-c', 'import macropy.activate; import '], 
        cwd=working_dir, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = subproc.communicate()
    return json.dumps(stdout.decode("utf-8"))