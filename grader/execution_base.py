import sys
import queue
import importlib
from time import sleep, time
from threading import Thread, Lock
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
            # this has to be last since it blocks if there's io
            self.module = self.import_duplicate(self.module_name)
        except Exception as e:
            # Threads don't propagate their errors to main thread
            # so this is neccessary for detecting errors with importing
            self.caughtException = e
            raise e from e


    def import_duplicate(module_name):
        """ Imports a module. If the module is previously loaded, it is nevertheless
            imported again """
        if module_name in sys.modules:
            del sys.modules[module_name]
        return importlib.import_module(module_name)


    def is_waiting_input(self):
        return self.stdin.waiting


def call_function(fun, args):
    """ Calls the function with args, checking if it doesn't raise an Exception.
        Returns a dictionary in the following form:
        {
            "success": boolean,
            "traceback": string ("" if None)
            "time": string (execution time, rounded to 2 decimal digits)
        }
    """
    success, traceback = True, ""
    start_time = time()
    try:
        fun(*args)
    except Exception as e:
        success = False
        traceback = str(e.__traceback__)
    end_time = time()
    return {
        "success": success,
        "traceback": traceback,
        "time": "%.2f" % (start_time - end_time)
    }


# TODO: an extra arg for the rest? or __name__ == main
tester_module, user_module = sys.argv[1:3]

# populate tests
import grader
importlib.import_module(tester_module)

results = {
    test_name: call_function(test_function, Module(user_module))
        for test_name, test_function in grader.testcases.items()
}

import json
sys.__stdout__.write(json.dumps(results, indent=4))