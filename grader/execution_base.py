"""
This module handles the execution of the users model. It should ideally
be called in an subprocess (like code_runner does) in a secure enviroment
with all code files prepared.

This overhead is needed to avoid having extra testcases loaded by the grader.

`test_module` loads the tester code loaded in a file. In that For each test, an 
async request is fired (run in another process). It is resolved within the 
`resolve_testcase_run` function. If that call timeouts, it is then terminated.

See `resolve_testcase_run` for output format description.
"""

import sys
import queue
import importlib
from codecs import open
from time import sleep, time
from threading import Thread, Lock
from grader.utils import dump_json, get_traceback, ProcessKillerThread
#from macropy.tracing import macros, trace

import grader

class SpoofedStdin:
    def __init__(self, timing_lock):
        self.queue = queue.Queue()
        self.waiting = False
        self.timing_lock = timing_lock
        self.timing_lock.acquire()
        self.need_locking = True

    def write(self, line):
        self.queue.put(str(line))
        # TODO: timing problems
        sleep(0.0001)

    def readline(self):
        if self.timing_lock.locked() and self.need_locking:
            self.timing_lock.release()
        self.waiting = True
        result = self.queue.get(timeout = 3)
        self.waiting = False
        if self.need_locking:
            self.timing_lock.acquire()
        return result


class SpoofedStdout:
    def __init__(self, timing_lock):
        self.timing_lock = timing_lock
        self.reset()
        self.need_locking = True

    def flush(self): pass

    def write(self, msg):
        self.output.append(msg)

    def reset(self):
        self.output = []
        self.lastread = 0

    def read(self):
        if self.need_locking:
            self.timing_lock.acquire()
        self.lastread = len(self.output)
        result = "".join(self.output)
        if self.need_locking:
            self.timing_lock.release()
            # give other thread a chance to execute
            # so we don't grab the lock back immediately
            sleep(0.00001) 
        return result

    def new(self):
        " returns the new elements in stdout since the last read "
        if self.need_locking:
            self.timing_lock.acquire()
        result = "".join(self.output[self.lastread:])
        self.lastread = len(self.output)
        if self.need_locking:
            self.timing_lock.release()
        return result


class ModuleContainer(Thread):
    """ A thread that runs the users program.
        It has hooks for a spoofed stdin and stdout, and also a reference to 
        the users module (available after the import is finished) """
    def __init__(self, module_name):
        Thread.__init__(self)
        self.module_name = module_name
        # dealing with timing issues, see #5
        self.timing_lock = Lock()
        self.caughtException = None
        # this thread doesn't block exiting
        self.setDaemon(True)
        self.start()
        # TODO: give a chance for the thread to run
        sleep(0.005)

    
    def run(self):
        try:
            self.stdin = sys.stdin = SpoofedStdin(self.timing_lock)
            self.stdout = sys.stdout = SpoofedStdout(self.timing_lock)
            #self.stderr = sys.stderr = SpoofedStdout()
            # this has to be last since it blocks if there's io
            # TODO: get/setattr, nicer message on failed access
            self.module = self.fake_import(self.module_name)
            if self.timing_lock.locked():
                self.timing_lock.release()
            self.stdin.need_locking = False
            self.stdout.need_locking = False
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
        with open(module_name + ".py", "r", "utf-8") as f:
            source = f.read()
        code = compile(source, "<tested-program>", "exec", dont_inherit=True)
        exec(code, mod.__dict__)
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

def call_test_function(test_index, tester_module, user_module):
    """ Called in another process. Finds the test `test_name`,  calls the 
        pre-test hooks and tries to execute it. 

        If an exception was raised by call, prints it to stdout """
    importlib.import_module(tester_module)
    test_name = list(grader.testcases.keys())[test_index]
    test_function = grader.testcases[test_name]

    module = ModuleContainer(user_module)
    try:
        test_function(module)
    except Exception as e:
        ModuleContainer.restore_io()
        print(get_traceback(e))


def do_testcase_run(test_name, tester_module, user_module):
    """ Calls the test, checking if it doesn't raise an Exception.
        Returns a dictionary in the following form:
        {
            "success": boolean,
            "traceback": string ("" if None)
            "time": string (execution time, rounded to 3 decimal digits)
            "description": string (test name/its description)
        }

        If the test timeouts, traceback is "timeout"
    """
    from grader.code_runner import call_test
    test_index = list(grader.testcases.keys()).index(test_name)
    timeout = grader.get_setting(test_name, "timeout")

    # pre-test hooks
    call_all(grader.get_setting(test_name, "before-hooks"))

    start = time()
    stdout = call_test(test_index, tester_module, user_module, timeout = timeout)
    end = time()
    if (end-start) > timeout:
        stdout = "Timeout"

    result = {
        "success": stdout == "",
        "traceback": stdout,
        "description": test_name,
        "time": "%.3f" % (end-start),
    }
    # after test hooks - cleanup
    call_all(grader.get_setting(test_name, "after-hooks"))
    return result


def test_module(tester_module, user_module, print_result = False):
    """ Runs all tests for user_module. Should be only run with 
        appropriate rights/user.

        Note that this assumes that user_module and tester_module
        are all in path and grader doesn't have extra tests loaded. 

        Returns/prints the dictionary from call_function.
    """
    # populate tests
    importlib.import_module(tester_module)
    assert len(grader.testcases) > 0
    test_results = [do_testcase_run(test_name, tester_module, user_module) 
                                    for test_name in grader.testcases.keys()]

    results = { "results": test_results }
    if print_result:
        print(dump_json(results))
    return results


if __name__ == "__main__":
    if len(sys.argv) == 3: # testing module
        tester_module, user_module = sys.argv[1:3]
        test_module(tester_module, user_module, True)
    elif len(sys.argv) == 4: # calling test function
        test_index, tester_module, user_module = sys.argv[1:4]
        call_test_function(int(test_index), tester_module, user_module)