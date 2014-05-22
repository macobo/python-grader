import os
import grader
from .utils import read_code, setDescription
from functools import wraps

def test_decorator(decorator):
    """ Decorator for test decorators. 

        This makes the decorator work testcases decorated with 
        :func:`grader.wrappers.test_cases`. """
    @wraps(decorator)
    def _inner(f):
        if isinstance(f, list) or isinstance(f, tuple):
            return tuple(decorator(func) for func in f)
        else:
            return decorator(f)
    return _inner


def timeout(seconds):
    """ Decorator for a test. Indicates how long the test can run. """
    @test_decorator
    def _inner(test_function):
        grader.set_setting(test_function, "timeout", seconds)
        return test_function
    return _inner

### Hooks
def before_test(action):
    """ Decorator for a pre-hook on a tested function. Makes the tester execute
        the function `action` before running the decorated test. """
    @test_decorator
    def _inner_decorator(test_function):
        hooks = grader.get_setting(test_function, "pre-hooks") + (action,)
        grader.set_setting(test_function, "pre-hooks", hooks)
        return test_function
    return _inner_decorator


def after_test(action):
    """ Decorator for a post-hook on a tested function. Makes the tester execute
        the function `action` after running the decorated test. """
    @test_decorator
    def _inner_decorator(test_function):
        hooks = grader.get_setting(test_function, "post-hooks") + (action,)
        grader.set_setting(test_function, "post-hooks", hooks)
        return test_function
    return _inner_decorator

@test_decorator
def set_description(d):
    """ Decorator for setting the description of a test.

        Example usage::

            @grader.test
            @grader.set_description("New description")
            def a_test_case(m):
                ...
    """
    def inner(f):
        setDescription(f, d)
        return f
    return inner


## File creation, deletion hooks
def create_file(filename, contents=""):
    """ Hook for creating files before a test.

        Example usage::

            @grader.test
            @grader.before_test(create_file('hello.txt', 'Hello world!'))
            @grader.after_test(delete_file('hello.txt'))
            def hook_test(m):
                with open('hello.txt') as file:
                    txt = file.read()
                    # ...
    """
    import collections
    if isinstance(contents, collections.Iterable) and not isinstance(contents, str):
        contents = "\n".join(map(str, contents))

    def _inner(info):
        with open(filename, "w") as f:
            f.write(contents)

    return _inner


def delete_file(filename):
    """ Hook for deleting files after a test.

        Example usage::

            @grader.test
            @grader.before_test(create_file('hello.txt', 'Hello world!'))
            @grader.after_test(delete_file('hello.txt'))
            def hook_test(m):
                with open('hello.txt') as file:
                    txt = file.read()
                    # ...
    """

    def _inner(result):
        try:
            os.remove(filename)
        except:
            pass

    return _inner


def create_temporary_file(filename, contents=""):
    """ Decorator for constructing a file which is available
        during a single test and is deleted afterwards.

        Example usage::

            @grader.test
            @create_temporary_file('hello.txt', 'Hello world!')
            def hook_test(m):
                with open('hello.txt') as file:
                    txt = file.read()
        """

    def _inner(test_function):
        before_test(create_file(filename, contents))(test_function)
        after_test(delete_file(filename))(test_function)
        return test_function
    return _inner


def add_value(value_name, value_or_fn):
    """ Post-test hook which as the value or the result of evaluating function on
        result to the test result dict.

        Example usage::

            @test
            @after_test(add_value("grade", 7))
            def graded_testcase(m):
                ...
        """
    def _inner(result):
        value = value_or_fn
        if hasattr(value, '__call__'):
            value = value_or_fn(result)
        result[value_name] = value
    return _inner


@test_decorator
def expose_ast(test_function):
    """ Pre-test hook for exposing the ast of the solution module
        as an argument to the tester. 

        Example usage::

            @grader.test
            @grader.expose_ast
            def ast_test(m, AST):
                ...
    """
    import ast

    def _hook(info):
        code = read_code(info["solution_path"])
        # add the solutions AST as a named argument to the test function
        info["extra_kwargs"]["AST"] = ast.parse(code)
    # add function _hook as a pre-hook to test_function
    return before_test(_hook)(test_function)
