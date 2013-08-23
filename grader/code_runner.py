import os
import subprocess
import contextlib

from tempfile import NamedTemporaryFile

@contextlib.contextmanager
def tempCodeModule(code_bytes, working_dir):
    file = NamedTemporaryFile(
        dir = working_dir,
        mode = "wb",
        suffix = ".py",
        delete = False
    )
    file.write(code_bytes)
    file.close()
    try:
        module_name = os.path.splitext(os.path.basename(file.name))[0]
        yield module_name
    finally:
        os.remove(file.name)


def runCode(code, working_dir=None):
    if working_dir is None: 
        working_dir = os.getcwd()

    code = code.encode("utf-8")
    with tempCodeModule(code, working_dir) as module_name:
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