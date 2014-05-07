from grader import *

__all__ = ["check_function"]
MISSING_VALUE = object()


def get_description_string(fn_name, arguments, expected_result, prefix):
    desc_template = "{fn_name}({args}) == {expected_result}"
    if prefix is None:
        description = desc_template
    else:
        description = prefix + " - " + desc_template
    args = ", ".join(map(repr, arguments))
    return description.format(
        fn_name=fn_name,
        args=args,
        expected_result=repr(expected_result)
    )


def get_error_description(result, expected, call):
    if call == 1:
        error = "Function should return {expected} but returned {result}."
    else:
        error = "Function returned {result} instead of {expected} on call {n}."
        error += "\nCheck if your solution relies on global variables"

    error = error.format(
        result=repr(result),
        expected=repr(expected),
        n=call
    )
    return error


def globals_error_msg(differences):
    error = ["\nFunction returned the correct value, but changed the following global variables:"]
    order = sorted(differences.keys())
    for var_name in order:
        old, new = differences[var_name]

        if old is MISSING_VALUE:
            a = "    created global variable {var} = {new}"
        elif new is MISSING_VALUE:
            a = "    deleted global variable {var} which was {old}"
        else:
            a = "    changed global variable {var} which was {old} and now is {new}"

        error.append(a.format(var=var_name,
                              old=repr(old),
                              new=repr(new)))
    return "\n".join(error)


def _copy(value):
    import copy
    copied = copy.deepcopy(value)
    if copied != value:
        #assert False, (copied, value)
        return value
    return copied


def variables_snapshot(module):
    "Returns a snapshot of variables in module, ignoring builtins"
    ignored = set(['__builtins__', '__name__', '__doc__'])

    values = {k: _copy(v) for k, v in module.__dict__.items() if k not in ignored}
    return values


def dict_diff(A, B):
    """ Returns a dictionary containing the differences between
        two dictionaries.

        dict_diff({1: 1, 2:2, 3:3}, {1:1, 3:2, 4:5}) returns
            {2: (2, None), 3: (2, 3), 4: (None, 5)} """
    keys = frozenset(A.keys()) | frozenset(B.keys())
    result = {}
    for key in keys:
        a = A.get(key, MISSING_VALUE)
        b = B.get(key, MISSING_VALUE)
        if a != b:
            result[key] = (a, b)
    return result


def check_function(
        sample_function, arguments,
        expected_result=None,
        description=None,
        # check if the function printed result instead
        # of returning it
        check_print=True,
        # number of times to call the function
        n_calls=3,
        # check if globals change after calling the function.
        check_globals=True):

    # get expected result from function, function name and
    # test description
    fn_name = sample_function.__name__
    if expected_result is None:
        expected_result = sample_function(*arguments)

    description = get_description_string(fn_name,
                                         arguments,
                                         expected_result,
                                         prefix=description)

    # Internally create a function and register as a test
    # All the checking logic goes in there.
    @test
    @set_description(description)
    def _inner_test(m):
        assert m.finished, "Program has to have finished execution"
        assert hasattr(m.module, fn_name), (
            "Function named {} was not defined.".format(repr(fn_name))
        )
        fn = getattr(m.module, fn_name)

        for i in range(1, n_calls + 1):
            start_vars = variables_snapshot(m.module)
            result = fn(*arguments)

            output = m.stdout.read()
            if check_print and result is None and \
                    str(expected_result) in output:

                raise AssertionError(
                    "Function printed out the correct result "
                    "instead of returning it.\n"
                    "Hint: replace print with return."
                )

            # if answer isn't what was expected, raise error
            assert result == expected_result, \
                get_error_description(result, expected_result, i)

            # check if any globals changed
            if check_globals:
                # get changed variables as a dictionary
                end_vars = variables_snapshot(m.module)
                diff = dict_diff(start_vars, end_vars)
                # if any variables changed, raise error accordingly
                assert not diff, globals_error_msg(diff)
