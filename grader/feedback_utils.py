def indent(text, spaces):
    lines = str(text).split("\n")
    return "\n".join(" " * spaces + line for line in lines).rstrip()

def require_contains(input, what, message=None, **extraparams):
    if what in input: return
    if message is None:
        message = "Expected [{what}] to be in input.\ninput was:\n  [{input}]"
    message = message.format(
        what=what,
        input=input,
        **extraparams
    )
    raise AssertionError(message)

def require_each_contains(input_list, expected_list, message=None, **extraparams):
    if message is None:
        message = "Difference at index {index}\nGot: {got}\nExpected: {expected}"
    for index, (expected, got) in enumerate(zip(expected_list, input_list)):
        require_contains(got, expected, **locals())
