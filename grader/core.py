import inspect
from functools import wraps
from .code_runner import call_sandbox, DOCKER_SANDBOX
from .asset_management import AssetFolder
from .datastructures import OrderedTestcases
from .utils import beautifyDescription, load_json
from .decorators import test_decorator

testcases = OrderedTestcases()

DEFAULT_TEST_SETTINGS = {
    # hooks that run before tests
    "pre-hooks": (),
    # hooks that run after tests
    "post-hooks": (),
    # timeout for function run
    "timeout": 1.0
}

SANDBOXES = {
    'docker': DOCKER_SANDBOX
}


def reset():
    " Removes all loaded tests from test case table. "
    testcases.clear()


def test(test_function):
    """ Decorator for a test. The function should take a single argument which
        is the object containing stdin, stdout and module (the globals of users program).

        The function name is used as the test name, which is a description for the test
        that is shown to the user. If the function has a docstring, that is used instead.

        Raising an exception causes the test to fail, the resulting stack trace is
        passed to the user. """
    assert hasattr(test_function, '__call__'), \
        "test_function should be a function, got " + repr(test_function)

    @wraps(test_function)
    def wrapper(module, *args, **kwargs):
        if module.caughtException:
            raise module.caughtException
        result = test_function(module, *args, **kwargs)
        if module.caughtException:
            raise module.caughtException
        return result

    name = get_test_name(test_function)
    testcases.add(name, wrapper)
    return wrapper


def get_test_name(function):
    """ Returns the test name as it is used by the grader. Used internally. """
    name = function.__name__
    if inspect.getdoc(function):
        name = beautifyDescription(inspect.getdoc(function))
    return name


def get_setting(test_function, setting_name):
    """ Returns a test setting. Used internally. """
    if isinstance(test_function, str):
        test_function = testcases[test_function]
    if not hasattr(test_function, "_grader_settings_"):
        # copy default settings
        test_function._grader_settings_ = DEFAULT_TEST_SETTINGS.copy()
    return test_function._grader_settings_[setting_name]


def set_setting(test_function, setting_name, value):
    """ Sets a test setting. Used internally. """
    if isinstance(test_function, str):
        test_function = testcases[test_function]
    # populate settings if needed
    get_setting(test_function, setting_name)
    test_function._grader_settings_[setting_name] = value

### Hooks
def before_test(action):
    """ Decorator for a pre-hook on a tested function. Makes the tester execute
        the function `action` before running the decorated test. """
    @test_decorator
    def _inner_decorator(test_function):
        hooks = get_setting(test_function, "pre-hooks") + (action,)
        set_setting(test_function, "pre-hooks", hooks)
        return test_function
    return _inner_decorator


def after_test(action):
    """ Decorator for a post-hook on a tested function. Makes the tester execute
        the function `action` after running the decorated test. """
    @test_decorator
    def _inner_decorator(test_function):
        hooks = get_setting(test_function, "post-hooks") + (action,)
        set_setting(test_function, "post-hooks", hooks)
        return test_function
    return _inner_decorator


### Exposed methods to test files/code
def test_module(tester_path, solution_path, other_files=[], sandbox_cmd=None):
    """ Runs all tests for the solution given as argument.

        :param str tester_path: Path to the tester used.
        :param str solution_path: Path to the solution being tested.
        :param list other_files: Paths to other files to put into same directory while testing.
        :param sandbox_cmd: Sandbox to use. Set this to 'docker' to use the built-in docker sandbox.

        :return: Dictionary of test results.

        Return value format::

            {
                "results": [
                    {
                        "description": str, # test description
                        "success": bool, # indicates whether the test case was successful
                        "time": "0.101", # float indicating how long test took
                        "error_message": str, # error message if test was not successful
                        "traceback": str, # full error traceback if test was not successful
                    },
                    ...
                ],
                "success": bool, # indicates whether tests were run or not
                "reason": str, # short string describing why tester failed to run
                "extra_info": dict, # extra information about why tester failed to run
            }
    """

    from .execution_base import do_testcase_run

    # copy files for during the tests to /tmp
    with AssetFolder(tester_path, solution_path, other_files) as assets:
        if sandbox_cmd is not None:
            return _collect_results_from_sandbox(assets, sandbox_cmd)

        # populate tests. TODO: add error handling
        try:
            testcases.load_from(assets.tester_path)
        except Exception as e:
            return _test_load_failure(e)

        if len(testcases) == 0:
            return _fail_result("No tests found in tester")

        test_results = []
        for test_name in testcases:
            result = do_testcase_run(test_name, assets.tester_path, assets.solution_path, {})
            test_results.append(result)

    results = {"results": test_results, "success": True}
    return results


def test_code(tester_code, user_code, other_files=[], *args, **kwargs):
    """ Tests code. See :func:`test_module` for argument and return value description. """
    with AssetFolder(tester_code, user_code, other_files, is_code=True) as assets:
        return test_module(
            assets.tester_path,
            assets.solution_path,
            assets.other_files,
            *args,
            **kwargs
        )


## Helpers

def _fail_result(reason, **extra_info):
    result = {
        "success": False,
        "reason": reason,
        "extra_info": extra_info
    }
    return result


def _collect_results_from_sandbox(assets, sandbox_cmd):
    from . import utils
    sandbox_cmd = SANDBOXES.get(sandbox_cmd, sandbox_cmd)
    if isinstance(sandbox_cmd, str):
        sandbox_cmd = [sandbox_cmd]
    try:
        status, stdout, stderr = call_sandbox(
            sandbox_cmd, assets.tester_path, assets.solution_path)
        if status == 0:
            result = load_json(stdout)
        else:
            result = _fail_result("Sandbox failure", stdout=stdout, stderr=stderr)
    except FileNotFoundError as e:
        result = _fail_result(
            "Invalid command: {}".format(" ".join(sandbox_cmd)),
            error_message=utils.get_error_message(e),
            traceback=utils.get_traceback(e))
    return result


def _test_load_failure(exception):
    from . import utils
    return _fail_result(
        "Load tests failure",
        error_message=utils.get_error_message(exception),
        traceback=utils.get_traceback(exception))
