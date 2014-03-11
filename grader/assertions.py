def indent(text, spaces):
    lines = str(text).split("\n")
    return "\n".join(" " * spaces + line for line in lines).rstrip()


def require_contains(input, what, message=None, **extraparams):
    if what in input:
        return
    if message is None:
        message = "Expected [{what}] to be in input.\ninput was:\n  [{input}]"
    message = message.format(
        what=repr(what),
        input=repr(input),
        **extraparams
    )
    raise AssertionError(message)


def require_each_contains(input_list, expected_list, message=None, **extraparams):
    if message is None:
        message = "Difference at index {index}\nGot: {got}\nExpected: {expected}"
    for index, (expected, got) in enumerate(zip(expected_list, input_list)):
        require_contains(got, expected, **locals())


def assertEquals(got, expected, template="Expected {expected} but got {got}", **kw):
    if got != expected:
        message = template.format(got=got, expected=expected, **kw)
        raise AssertionError(message)


def assertNContains(input, collection, N, template=None):
    if template is None:
        template = "Expected input to contain {N} of {collection}.\nInput was:{input}"
    count = sum(A in input for A in collection)
    if count != N:
        raise AssertionError(template.format(N=N, count=count, collection=collection, input=repr(input)))


def assertOneContains(input, collection, template=None):
    if template is None:
        template = "Input should contain exactly one of the following: {collection}.\nInput was: {input}"
    assertNContains(input, collection, 1, template)
