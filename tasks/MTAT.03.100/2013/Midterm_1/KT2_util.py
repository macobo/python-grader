from grader import *


def assertEquals(a, b, template = "Expected {a} but got {b}", **kw):
    if a != b:
        message = template.format(a=a, b=b, **kw)
        raise AssertionError(message)

def assertNContains(input, collection, N, template=None):
    if template is None:
        template = "Expected input to contain {N} of {collection}.\nInput was:{input}"
    count = sum(A in input for A in collection)
    if count != N:
        raise AssertionError(template.format(N=N, count=count, collection=collection, input=repr(input)))

def assertOneContains(input, collection, template=None):
    if template is None:
        template = "Sisend peaks sisaldama maksimaalselt ühte järgnevatest({count}): {collection}.\nSisend oli: {input}"
    assertNContains(input, collection, 1, template)

def function_test(function_name, args, expected, description=None, before_test_call=None):
    args_str = ", ".join(map(repr, args))
    if description is None:
        description = "Test - {function}({args}) == {expected}"
    description = description.format(
        function=function_name, 
        args=args_str, 
        expected=repr(expected))

    @test
    def test_function(m):
        if before_test_call is not None:
            before_test_call(m)
        assert hasattr(m, 'module'), "Programmi täitmine ei lõppenud. Failis ei tohiks olla üleliigseid input() käski"
        assert hasattr(m.module, function_name), "Peab leiduma funktsioon nimega {name}!".format(name=function_name, dict=m.module.__dict__)
        user_function = getattr(m.module, function_name)
        result = user_function(*args)
        assertEquals(result, expected,
            "{function_name}({args_str}) peaks tagastama {expected} aga tagastas {result}",
            expected=expected,
            result=result,
            function_name=function_name,
            args_str=args_str)

    setDescription(test_function, description)
    return test_function

def make_checker(tester, function_name=None):
    if function_name is None:
        function_name = tester.__name__
    return lambda *args, **kw: function_test(function_name, args, tester(*args), **kw)


class do:
    def __init__(self, function):
        if isinstance(function, do): function = function.function
        self.function = function

    def after(self, _test, ignore_test_errors=False):
        if isinstance(_test, do): _test = _test.function
        # TODO: inherit docstring, name
        def new_test(m):
            if ignore_test_errors:
                try: result = _test(m)
                except: pass
            else:
                result = _test(m)
            self.function(m)

        return do(new_test)

    def then(self, _test):
        if isinstance(_test, do): _test = _test.function
        def new_test(m):
            self.function(m)
            _test(m)
        return do(new_test)

    def as_test(self, description):
        f = test(self.function)
        setDescription(f, description)
        return do(f)

    def add_decorator(self, decorator):
        return do(decorator(self.function))