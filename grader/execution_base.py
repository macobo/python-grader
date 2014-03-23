"""
This module handles the execution of the users module. It should ideally
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
from time import sleep, time
from threading import Thread, Lock
from .utils import get_traceback, import_module
from .program_container import ProgramContainer
import grader


def call_all(function_list, *args, **kwargs):
    for fun in function_list:
        fun(*args)


def call_test_function(test_name, tester_module, user_module):
    """ Called in another process. Finds the test `test_name`,  calls the
        pre-test hooks and tries to execute it.

        If an exception was raised by call, prints it to stdout """

    pre_hook_info = {
        "test_name": test_name,
        "tester_module": tester_module,
        "user_module": user_module,
        "extra_args": [],
        "extra_kwargs": {}
    }

    import_module(tester_module)
    test_function = grader.testcases[test_name]

    # pre-test hooks
    call_all(grader.get_setting(test_name, "before-hooks"), pre_hook_info)

    # start users program
    module = ProgramContainer(user_module)
    module.condition.acquire()
    try:
        test_function(
            module,
            *pre_hook_info["extra_args"],
            **pre_hook_info["extra_kwargs"]
        )
    except Exception as e:
        module.restore_io()
        error_message = ""
        if module.caughtException:
            error_message += "Exception in program:\n\n"
            error_message += get_traceback(module.caughtException)
            error_message += "\n\nException in tester:\n\n"
        error_message += get_traceback(e)
        #print(repr(ModuleContainer.stdout.read())+">>>>>"+error_message)
        print(error_message)


def do_testcase_run(test_name, tester_module, user_module, options):
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
    options["timeout"] = grader.get_setting(test_name, "timeout")

    start = time()
    traceback = call_test(test_name, tester_module, user_module, options)
    end = time()
    if (end - start) > options["timeout"]:
        traceback = "Timeout"

    result = {
        "success": traceback == "",
        "traceback": traceback,
        "description": test_name,
        "time": "%.3f" % (end - start),
    }
    # after test hooks - cleanup
    call_all(grader.get_setting(test_name, "after-hooks"))
    return result
