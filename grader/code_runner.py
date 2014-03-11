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
    try:
        stdout = subprocess.check_output(cmd, cwd=working_dir)
    except subprocess.CalledProcessError as e:
        stdout = e.output
    stdout = stdout.decode('utf-8')
    return stdout
