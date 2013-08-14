def indent(text, spaces):
    lines = str(text).split("\n")
    return "\n".join(" " * spaces + line for line in lines).rstrip()

def require_contains(input, what):
    if what in input: return
    message = "Expected {what} to be in input.\ninput was:\n{input}"
    message = message.format(
        what=what,
        input=indent(input, 2)
    )
    raise AssertionError(message)

