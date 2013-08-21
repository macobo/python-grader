## TODO: How to we validate that our vital components arent 
## overwritten by user code?
from .feedback_utils import *
from .core import *

def testAll():
    for test_name, (success, errors) in allTestResults():
        if success:
            print("Test {test_name} completed successfully!".format(**locals()))
        else:
            print("Test {test_name} failed:\n{errors}".format(**locals()))


def io_test(name, writes, expected_read):
    def f(module):
        for write in writes:
            module.stdout.reset()
            module.stdin.write(write)
        assert expected_read in module.stdout.new()
    # hack to make it importable
    f.__name__ = name
    return test(f)