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

