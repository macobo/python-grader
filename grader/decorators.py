import os

## File creation, deletion hooks
def create_file(filename, contents = ""):
    """ Hook for creating files 
        Example usage:

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
    """ Hook for deleting files 
        Example usage:
        
        @grader.test
        @grader.before_test(create_file('hello.txt', 'Hello world!'))
        @grader.after_test(delete_file('hello.txt'))
        def hook_test(m):
            with open('hello.txt') as file:
                txt = file.read()
                # ...
    """

    def _inner():
        try: os.remove(filename)
        except: pass

    return _inner

def create_temporary_file(filename, contents = ""):
    """ Decorator for constructing a file which is available
        during a single test and is deleted afterwards. 

        Example usage:
        @grader.test
        @create_temporary_file('hello.txt', 'Hello world!')
        def hook_test(m):
            with open('hello.txt') as file:
                txt = file.read()
        """
    from grader.core import before_test, after_test
    def _inner(test_function):
        before_test(create_file(filename, contents))(test_function)
        after_test(delete_file(filename))(test_function)
        return test_function
    return _inner



def get_module_AST(path):
    import tokenize
    import ast
    # encoding-safe open
    with tokenize.open(path) as sourceFile:
        contents = sourceFile.read()
    return ast.parse(contents)

def expose_ast(test_function):
    """ Decorator for exposing the ast of the solution module
        as an argument to the tester. """
    from grader.core import before_test
    def _hook(info):
        module_ast = get_module_AST(info["user_module"])
        info["extra_kwargs"]["AST"] = module_ast

    return before_test(_hook)(test_function)