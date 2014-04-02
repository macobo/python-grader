import os
import subprocess
import datetime
import signal
import time

CURRENT_FOLDER = os.path.abspath(os.path.dirname(__file__))
SANDBOX_DIR = os.path.join(os.path.dirname(CURRENT_FOLDER), "sandbox")

TEST_RUN_CMD = os.path.join(SANDBOX_DIR, "run_test")
DOCKER_SANDBOX = os.path.join(SANDBOX_DIR, 'run_tests_docker_sandbox')


def read_proc_results(proc, decode):
    stdout = proc.stdout.read() 
    stderr = proc.stderr.read()
    if decode:
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
    status = proc.returncode
    return status, stdout, stderr


def call_command(cmd, timeout=float('inf'), cwd=None, decode=True, **subproc_options):
    if cwd is None:
        cwd = os.getcwd()

    start = datetime.datetime.now()

    subproc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **subproc_options
    )

    reached_timeout = False
    while subproc.poll() is None:
        time.sleep(0.02)
        now = datetime.datetime.now()
        if (now - start).microseconds >= timeout * 10**6:
            os.kill(subproc.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            reached_timeout = True

    status, stdout, stderr = read_proc_results(subproc, decode)
    if reached_timeout:
        status = 1
    return status, stdout, stderr


def call_test(test_name, tester_path, solution_path, options):
    # this assumes that tester, solution resides in the same path
    #working_dir = os.getcwd()#os.path.dirname(tester_path)
    cmd = [
        TEST_RUN_CMD,
        tester_path,
        solution_path,
        test_name
    ]
    status, stdout, stderr = call_command(cmd, timeout=options["timeout"])
    return status == 0, stdout, stderr


def call_sandbox(sandbox_cmd, tester_path, solution_path):
    cmd = sandbox_cmd + [tester_path, solution_path]
    return call_command(cmd)
