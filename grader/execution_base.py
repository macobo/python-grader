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

import grader
from time import time, sleep
from .program_container import ProgramContainer
from .utils import get_traceback, get_error_message, import_module, dump_json, load_json

RESULT_DEFAULTS = {
    "log": [],
    "error_message": "",
    "traceback": ""
}


def call_all(function_list, *args, **kwargs):
    for fun in function_list:
        fun(*args)


def call_test_function(test_index, tester_path, solution_path):
    """ Called in another process. Finds the test `test_name`,  calls the
        pre-test hooks and tries to execute it.

        If an exception was raised by call, prints it to stdout """

    import_module(tester_path)
    test_name = grader.testcases.get_name(test_index)
    test_function = grader.testcases[test_name]

    # pre-test hooks
    pre_hook_info = {
        "test_name": test_name,
        "tester_path": tester_path,
        "solution_path": solution_path,
        "extra_args": [],
        "extra_kwargs": {}
    }
    call_all(grader.get_setting(test_name, "pre-hooks"), pre_hook_info)

    results = RESULT_DEFAULTS.copy()

    # start users program
    try:
        module = ProgramContainer(solution_path, results)
        while not hasattr(module, "module"):
            sleep(0.001)
        module.condition.acquire()
        test_function(
            module,
            *pre_hook_info["extra_args"],
            **pre_hook_info["extra_kwargs"]
        )
    except Exception as e:
        if module.caughtException is not None:
            e = module.caughtException
        results["error_message"] = get_error_message(e)
        results["traceback"] = get_traceback(e)
        raise
    finally:
        module.restore_io()
        print(dump_json(results))


def do_testcase_run(test_name, tester_path, solution_path, options):
    """ Calls the test, checking if it doesn't raise an Exception.
        Returns a dictionary in the following form::

            {
                "success": boolean,
                "traceback": string ("" if None)
                "error_message: string
                "time": string (execution time, rounded to 3 decimal digits)
                "description": string (test name/its description)
            }

        If the test timeouts, traceback is set to "timeout".

        Post-hooks can manipulate with the test results before returning.
    """
    from grader.code_runner import call_test
    options["timeout"] = grader.get_setting(test_name, "timeout")

    test_index = grader.testcases.indexOf(test_name)

    start = time()
    success, stdout, stderr = call_test(test_index, tester_path, solution_path, options)
    end = time()

    result = RESULT_DEFAULTS.copy()
    if (end - start) > options["timeout"]:
        result["error_message"] = "Timeout"
        result["traceback"] = "Timeout"
    else:
        try:
            result = load_json(stdout)
        except Exception as e:
            result["traceback"] = stdout
            result["stderr"] = stderr

    result.update(
        success=success,
        description=test_name,
        time=("%.3f" % (end - start))
    )
    # after test hooks - cleanup
    call_all(grader.get_setting(test_name, "post-hooks"), result)
    return result
