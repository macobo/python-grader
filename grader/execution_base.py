import sys
import queue
import importlib
import traceback
import multiprocessing
from codecs import open
from time import sleep, time
from threading import Thread, Lock
from grader.utils import dump_json
#from macropy.tracing import macros, trace

import grader

class SpoofedStdin:
    def __init__(self, lock):
        self.queue = queue.Queue()
        self.waiting = False
        self.lock = lock
        self.lock.acquire()

    def write(self, line):
        self.queue.put(str(line))
        # TODO: timing problems
        sleep(0.0001)

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


class ModuleContainer(Thread):
    """ A thread that runs the users program.
        It has hooks for a spoofed stdin and stdout, and also a reference to 
        the users module (available after the import is finished) """
    def __init__(self, module_name):
        Thread.__init__(self)
        self.module_name = module_name
        self.lock = Lock()
        self.caughtException = None
        # this thread doesn't block exiting
        self.setDaemon(True)
        self.start()
        # TODO: give a chance for the thread to run
        sleep(0.005)

    
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
        mod.__file__ = module_name + ".py"
        with open(module_name + ".py", "r", "utf-8") as f:
            source = f.read()
        code = compile(source, module_name, "exec", dont_inherit=True)
        exec(code, mod.__dict__)
        mod.__meh__ = str(dir(mod))
        return mod


    def is_waiting_input(self):
        return self.stdin.waiting


    @classmethod
    def restore_io(cls):
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__


def call_all(function_list):
    for fun in function_list: 
        fun()

def call_test_function(q, test_name, tester_module, user_module):
    """ Calls the function with args, checking if it doesn't raise an Exception.
        Returns a dictionary in the following form:
        {
            "success": boolean,
            "traceback": string ("" if None)
            "time": string (execution time, rounded to 3 decimal digits)
            "description": string (test name/its description)
        }
    """
    q.put(time())
    # populate tests
    importlib.import_module(tester_module)
    test_function = grader.testcases[test_name]
    # # pre-test hooks
    call_all(grader.get_before_hooks(test_function))

    module = ModuleContainer(user_module)
    test_function(module)

    # after test hooks - cleanup
    #call_all(grader.get_after_hooks(test_function))

def get_traceback(exception):
    type_, value, tb = type(exception), exception, exception.__traceback__
    return "".join(traceback.format_exception(type_, value, tb))

def resolve_testcase_run(q, async, test_name, timeout):
    test_function = grader.testcases[test_name]

    # TODO: if start_time doesn't resolve?
    start_time = q.get(timeout=timeout)
    time_left = start_time + timeout - time()
    success, traceback_ = True, ""
    return_result = None
    try:
        return_result = async.get(time_left)
    except Exception as e:
        success = False
        type_, value, tb = type(e), e, e.__traceback__
        traceback_ = "".join(traceback.format_exception(type_, value, tb))
    exec_time = time() - start_time
    ModuleContainer.restore_io()
    result = {
        "success": success,
        "traceback": traceback_,
        "description": grader.get_test_name(test_function),
        "time": "%.3f" % exec_time,
    }
    call_all(grader.get_after_hooks(test_function))
    return result


def test_module(tester_module, user_module, print_result = False):
    """ Runs all tests for user_module. Should be only run with 
        appropriate rights/user.

        Note that this assumes that user_module and tester_module
        are all in path and grader doesn't have extra tests loaded. 

        Returns/prints the dictionary from call_function.
    """
    from multiprocessing.pool import Pool
    # populate tests
    importlib.import_module(tester_module)

    pool = Pool(1)
    manager = multiprocessing.Manager()
    test_results = []
    for test_name in grader.testcases:
        q = manager.Queue()
        args = (q, test_name, tester_module, user_module)
        async = pool.apply_async(call_test_function, args)
        test_results.append(
            resolve_testcase_run(q, async, test_name, 1)
        )


    # test_results = [
    #     call_test_function(test_function, user_module)
    #         for test_name, test_function in grader.testcases.items()
    # ]

    results = {
        "results": test_results
    }

    if print_result:
        print(dump_json(results))
    return results


if __name__ == "__main__":
    tester_module, user_module = sys.argv[1:3]
    test_module(tester_module, user_module, True)