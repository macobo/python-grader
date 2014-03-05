import os
import inspect
from functools import wraps
from collections import OrderedDict
#from .code_runner import runTester
from .utils import beautifyDescription, dump_json

CURRENT_FOLDER = os.path.dirname(__file__)
DEFAULT_TESTCASE_RUNNER = os.path.join(
                                os.path.dirname(CURRENT_FOLDER), 
                                "sandbox", 
                                "run_test_no_sandbox")

testcases = OrderedDict()

DEFAULT_SETTINGS = {
    # hooks that run before tests
    "before-hooks": (),
    # hooks that run after tests
    "after-hooks": (),
    # timeout for function run
    "timeout": 1.0
}

def reset():
    " resets settings and loaded tests "
    global testcases
    testcases = OrderedDict()

def test(test_function):
    """ Decorator for a test. The function should take a single argument which
        is the object containing stdin, stdout and module (the globals of users program).

        The function name is used as the test name, which is a description for the test 
        that is shown to the user. If the function has a docstring, that is used instead.

        Raising an exception causes the test to fail, the resulting stack trace is
        passed to the user. """
    assert hasattr(test_function, '__call__'), \
        "test_function should be a function, got "+repr(test_function)

    @wraps(test_function)
    def wrapper(module, *args, **kwargs):
        if module.caughtException:
            raise module.caughtException
        
        result = test_function(module, *args, **kwargs)
        if module.caughtException:
            raise module.caughtException
        return result

    name = get_test_name(test_function)
    testcases[name] = wrapper
    return wrapper


def get_test_name(function):
    """ Returns the test name as it is used by the grader. """
    name = function.__name__
    if inspect.getdoc(function):
        name = beautifyDescription(inspect.getdoc(function))
    return name

def get_setting(test_function, setting_name):
    if isinstance(test_function, str):
        test_function = testcases[test_function]
    if not hasattr(test_function, "_grader_settings_"):
        # copy default settings
        test_function._grader_settings_ = DEFAULT_SETTINGS.copy()
    return test_function._grader_settings_[setting_name]

def set_setting(test_function, setting_name, value):
    if isinstance(test_function, str):
        test_function = testcases[test_function]
    # populate settings if needed
    get_setting(test_function, setting_name)
    test_function._grader_settings_[setting_name] = value

### Hooks 

def before_test(action):
    """ Decorator for a hook on a tested function. Makes the tester execute
        the function `action` before running the decorated test. """
    def _inner_decorator(test_function):
        hooks = get_setting(test_function, "before-hooks") + (action,)
        set_setting(test_function, "before-hooks", hooks)
        return test_function
    return _inner_decorator

def after_test(action):
    """ Decorator for a hook on a tested function. Makes the tester execute
        the function `action` after running the decorated test. """
    def _inner_decorator(test_function):
        hooks = get_setting(test_function, "after-hooks") + (action,)
        set_setting(test_function, "after-hooks", hooks)
        return test_function
    return _inner_decorator

def timeout(seconds):
    """ Decorator for a test. Indicates how long the test can run. """
    def _inner(test_function):
        set_setting(test_function, "timeout", seconds)
        return test_function
    return _inner

### Exposed methods to test files/code

def test_module(tester_module, user_module, **options):
    """ Runs all tests for user_module. Should be only run with 
        appropriate rights/user.

        Note that this assumes that user_module and tester_module
        are all in path and grader doesn't have extra tests loaded. 

        Returns/prints the dictionary from call_function.
    """
    from .execution_base import do_testcase_run
    from .utils import import_module
    # populate tests
    reset()
    import_module(tester_module)
    assert len(testcases) > 0
    test_results = [do_testcase_run(test_name, tester_module, user_module) 
                                    for test_name in testcases.keys()]

    results = { "results": test_results }
    if options.get('print_result'):
        print(dump_json(results))
    return results


def test_solution(tester_code, user_code, **options):
    from .utils import AssetFolder
    assets = AssetFolder(tester_code, user_code, is_code=True)
    try:
        return test_module(assets.tester_path, assets.solution_path, **options)
    finally:
        assets.remove()