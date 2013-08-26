import sys
import queue
import importlib
import traceback
from time import sleep, time
from threading import Thread, Lock
from grader.utils import dump_json
#from macropy.tracing import macros, trace

class SpoofedStdin:
    def __init__(self, lock):
        self.queue = queue.Queue()
        self.waiting = False
        self.lock = lock
        self.lock.acquire()

    def write(self, line):
        self.queue.put(str(line))
        sleep(0.01)

    def readline(self):
        if self.lock.locked():
            self.lock.release()
        self.waiting = True
        result = self.queue.get(timeout = 3)
        self.waiting = False
        self.lock.acquire()
        return result


class SpoofedStdout:
    def __init__(self):
        self.reset()

    def flush(self): pass

    def write(self, msg):
        self.output.append(msg)

    def reset(self):
        self.output = []
        self.lastread = 0

    def read(self):
        self.lastread = len(self.output)
        return "".join(self.output)

    def new(self):
        " returns the new elements in stdout since the last read "
        result = "".join(self.output[self.lastread:])
        self.lastread = len(self.output)
        return result


class Module(Thread):
    def __init__(self, module_name):
        Thread.__init__(self)
        self.module_name = module_name
        self.lock = Lock()
        self.caughtException = None
        # this thread doesn't block exiting
        self.setDaemon(True)
        self.start()
        sleep(0.05)

    
    def run(self):
        try:
            self.stdin = sys.stdin = SpoofedStdin(self.lock)
            self.stdout = sys.stdout = SpoofedStdout()
            #self.stderr = sys.stderr = SpoofedStdout()
            # this has to be last since it blocks if there's io
            self.module = self.fake_import(self.module_name)
        except Exception as e:
            # Threads don't propagate their errors to main thread
            # so this is neccessary for detecting errors with importing
            self.caughtException = e
            raise e from e


    def fake_import(self, module_name):
        """ Imports a module. If the module is previously loaded, it is nevertheless
            imported again """
        from types import ModuleType
        mod = ModuleType("solution_program")
        with open(module_name + ".py") as f:
            source = f.read()
        code = compile(source, module_name, "exec", dont_inherit=True)
        exec(code, mod.__dict__)
        return mod


    def is_waiting_input(self):
        return self.stdin.waiting


    @classmethod
    def restore_io(cls):
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__



def call_test_function(fun, module):
    """ Calls the function with args, checking if it doesn't raise an Exception.
        Returns a dictionary in the following form:
        {
            "success": boolean,
            "traceback": string ("" if None)
            "time": string (execution time, rounded to 3 decimal digits)
        }
    """
    success, traceback_ = True, ""
    start_time = time()
    try:
        fun(module)
    except Exception as e:
        success = False
        traceback_ = "\n".join(traceback.format_tb(e.__traceback__))
        traceback_ += "\n" + str(e)
    end_time = time()
    Module.restore_io()
    #sys.__stdout__.write("=====" + "\n"*3)
    #sys.__stdout__.write(module.stderr.read())
    return {
        "success": success,
        "traceback": traceback_,
        "time": "%.3f" % (end_time - start_time),
        "stdout": module.stdout.read()
    }


def test_module(tester_module, user_module, print_result = False):
    """ Runs all tests for user_module. Should be only run with 
        appropriate rights/user.

        Note that this assumes that user_module and tester_module
        are all in path and grader doesn't have extra tests loaded. 

        Returns/prints the dictionary from call_function.
    """
    # populate tests
    import grader
    importlib.import_module(tester_module)

    results = {
        test_name: call_test_function(test_function, Module(user_module))
            for test_name, test_function in grader.testcases.items()
    }
    if print_result:
        print(dump_json(results))
    return results


if __name__ == "__main__":
    tester_module, user_module = sys.argv[1:3]
    test_module(tester_module, user_module, True)