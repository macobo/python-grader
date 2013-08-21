import macropy.activate

from .core import *
from .test_wrappers import *

def testAll():
    for test_name, (success, errors) in allTestResults():
        if success:
            print("Test {test_name} completed successfully!".format(**locals()))
        else:
            print("Test {test_name} failed:\n{errors}".format(**locals()))

