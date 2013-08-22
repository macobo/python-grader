import os
import subprocess

from tempfile import NamedTemporaryFile

def tempCodeFile(working_dir):
    return NamedTemporaryFile(
        dir = working_dir,
        mode = "wb",
        suffix = ".py",
        delete = False
    )

def runCode(code, working_dir=None):
    if working_dir is None: 
        working_dir = os.getcwd()

    with tempCodeFile(working_dir) as f:
        module_name = os.path.basename(f.name).split('.')[0]
        f.write(code.encode("utf-8"))

    subproc = subprocess.Popen(
        ['python3', '-c', 'import macropy.activate; import '+module_name], 
        cwd=working_dir, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = subproc.communicate()
    os.remove(f.name)
    #print(subproc.returncode, stdout)
    #print(stderr.decode("utf-8"))

    return {
        "stdout": stdout.decode("utf-8"),
        "stderr": stderr.decode("utf-8"),
        "status": subproc.returncode
    }