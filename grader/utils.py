""" An utility module containing utility functions used by the grader module 
    and some useful pre-test hooks.
"""
import os
import json
import traceback
import tokenize

def import_module(path, name=None):
    if name is None:
        name = path
    import importlib.machinery
    loader = importlib.machinery.SourceFileLoader(name, path)
    module = loader.load_module(name)
    return module

# def import_module(path, name=None):
#     """ Imports a module. If the module is previously loaded, it is nevertheless
#         imported again """
#     if name is None:
#         name = path
#     from types import ModuleType
#     mod = ModuleType("solution_program")
#     with tokenize.open(path) as f:
#         source = f.read()
#     code = compile(source, name, "exec", dont_inherit=True)
#     exec(code, mod.__dict__)
#     return mod

## Function descriptions
def beautifyDescription(description):
    """ Converts docstring of a function to a test description
        by removing excess whitespace and joining the answer on one
        line """
    lines = (line.strip() for line in description.split('\n'))
    return " ".join(filter(lambda x:x, lines))

def setDescription(function, description):
    import grader
    old_description = grader.get_test_name(function)
    if old_description in grader.testcases:
        grader.testcases.remove(old_description)
    description = beautifyDescription(description)
    function.__doc__ = description
    grader.testcases.add(description, function)

## Json managing
def load_json(json_string):
    " Loads json_string into an dict "
    return json.loads(json_string)

def dump_json(ordered_dict):
    " Dumps the dict to a string, indented "
    return json.dumps(ordered_dict, indent=4)#, ensure_ascii=False)

def get_traceback(exception):
    type_, value, tb = type(exception), exception, exception.__traceback__
    return "".join(traceback.format_exception(type_, value, tb))