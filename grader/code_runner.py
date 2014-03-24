import os
import subprocess
#from .utils import load_json

def call_test(test_name, tester_path, solution_path, options):
    working_dir = os.getcwd()

    cmd = [
        "timeout",
        str(options["timeout"]),
        options["runner_cmd"],
        tester_path,
        solution_path,
        test_name
    ]
    subproc = subprocess.Popen(
        cmd, cwd=working_dir,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = subproc.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    status = subproc.returncode
    return status == 0, stdout, stderr
