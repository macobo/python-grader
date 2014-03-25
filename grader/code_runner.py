import os
import subprocess
from .utils import load_json

CURRENT_FOLDER = os.path.abspath(os.path.dirname(__file__))
SANDBOX_DIR = os.path.join(os.path.dirname(CURRENT_FOLDER), "sandbox")

TEST_RUN_CMD = os.path.join(SANDBOX_DIR, "run_test")

def call_test(test_name, tester_path, solution_path, options):
    # this assumes that tester, solution resides in the same path
    working_dir = os.getcwd()#os.path.dirname(tester_path)

    cmd = [
        "timeout",
        str(options["timeout"]),
        TEST_RUN_CMD,
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