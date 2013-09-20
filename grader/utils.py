import os
import json
import contextlib
import traceback
from threading import Thread

from tempfile import NamedTemporaryFile

@contextlib.contextmanager
def tempModule(code, working_dir=None, encoding="utf8"):
    if working_dir is None: 
        working_dir = os.getcwd()
    file = NamedTemporaryFile(
        dir = working_dir,
        mode = "wb",
        suffix = ".py",
        delete = False
    )
    file.write(code.encode(encoding))
    file.close()
    try:
        module_name = os.path.splitext(os.path.basename(file.name))[0]
        yield module_name
    finally:
        os.remove(file.name)


## Process killer
class ProcessKillerThread(Thread):
    " A thread to kill a process after a given time limit. "
    def __init__(self, subproc, limit):
        super(ProcessKillerThread, self).__init__()
        self.subproc = subproc
        self.limit = limit
        self.killedProcess = False

    def run(self):
        start = time.time()
        while (time.time() - start) < self.limit:
            time.sleep(.25)
            if self.subproc.poll() is not None:
                # Process ended, no need for us any more.
                return

        if self.subproc.poll() is None:
            # Can't use subproc.kill because we launched the subproc with sudo.
            pgid = os.getpgid(self.subproc.pid)
            subprocess.call(["sudo", "pkill", "-9", "-g", str(pgid)])
            self.killedProcess = True

## Function descriptions
def beautifyDescription(description):
    lines = (line.strip() for line in description.split('\n'))
    return " ".join(filter(lambda x:x, lines))

def setDescription(function, description):
    function.__doc__ = beautifyDescription(description)


## Json managing
def load_json(json_string):
    " Loads json_string into an dict "
    return json.loads(json_string)

def dump_json(ordered_dict):
    " Dumps the dict to a string, indented "
    return json.dumps(ordered_dict, indent=4)#, ensure_ascii=False)


## 
def get_traceback(exception):
    type_, value, tb = type(exception), exception, exception.__traceback__
    return "".join(traceback.format_exception(type_, value, tb))



## File creation, deletion for hooks
def create_file(filename, contents = ""):
    " Hook for creating files "
    import collections
    if isinstance(contents, collections.Iterable) and not isinstance(contents, str):
        contents = "\n".join(map(str, contents))
    def _inner():
        with open(filename, "w") as f:
            f.write(contents)
    return _inner

def delete_file(filename):
    " Hook for deleting files "
    def _inner():
        os.remove(filename)
    return _inner

def create_temporary_file(filename, contents = ""):
    from grader.core import before_test, after_test
    """ Decorator for constructing a file which is available
        during a single test and is deleted afterwards. """
    def _inner(test_function):
        before_test(create_file(filename, contents))(test_function)
        after_test(delete_file(filename))(test_function)
        return test_function
    return _inner