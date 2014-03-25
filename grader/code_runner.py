import os
import subprocess

CURRENT_FOLDER = os.path.abspath(os.path.dirname(__file__))
SANDBOX_DIR = os.path.join(os.path.dirname(CURRENT_FOLDER), "sandbox")

TEST_RUN_CMD = os.path.join(SANDBOX_DIR, "run_test")
DOCKER_SANDBOX = os.path.join(SANDBOX_DIR, 'run_tests_docker_sandbox')

def call_command(cmd, cwd = None, decode=True):
    if cwd is None:
        cwd = os.getcwd()
    subproc = subprocess.Popen(
        cmd, cwd=cwd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = subproc.communicate()
    if decode:
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')

    status = subproc.returncode
    return status, stdout, stderr


def call_test(test_name, tester_path, solution_path, options):
    # this assumes that tester, solution resides in the same path
    #working_dir = os.getcwd()#os.path.dirname(tester_path)
    cmd = [
        "timeout",
        str(options["timeout"]),
        TEST_RUN_CMD,
        tester_path,
        solution_path,
        test_name
    ]
    status, stdout, stderr = call_command(cmd)
    return status == 0, stdout, stderr


def call_sandbox(sandbox_cmd, tester_path, solution_path):
    cmd = sandbox_cmd + [tester_path, solution_path]
    return call_command(cmd)
