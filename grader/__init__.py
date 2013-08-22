import macropy.activate

from .core import *
from .test_wrappers import *
from pprint import pprint

def testAll(print_result = False):
    all_results = []
    for test_name, (success, errors) in allTestResults():
        result = {"description": test_name, "success": success}
        if not success:
            result["trace"] = errors["stderr"]
        all_results.append(result)
    if print_result:
        pprint(all_results)
    return all_results

