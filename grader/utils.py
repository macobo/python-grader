import os
import json
import contextlib

from tempfile import NamedTemporaryFile

@contextlib.contextmanager
def tempModule(code, working_dir=None, encoding="utf8"):
    if working_dir is None: 
        working_dir = os.getcwd()
    file = NamedTemporaryFile(
        dir = working_dir,
        mode = "wb",
        suffix = ".py",
        delete = False
    )
    file.write(code.encode(encoding))
    file.close()
    try:
        module_name = os.path.splitext(os.path.basename(file.name))[0]
        yield module_name
    finally:
        os.remove(file.name)


## Function descriptions
def beautifyDescription(description):
    lines = (line.strip() for line in description.split('\n'))
    return " ".join(filter(lambda x:x, lines))

def setDescription(function, description):
    function.__doc__ = beautifyDescription(description)


## Json managing
def load_json(json_string):
    " Loads json_string into an dict "
    return json.loads(json_string)

def dump_json(ordered_dict):
    " Dumps the dict to a string, indented "
    return json.dumps(ordered_dict, indent=4)#, ensure_ascii=False)


## File creation, deletion for hooks
def create_file(filename, contents = ""):
    " Hook for creating files "
    import collections
    if isinstance(contents, collections.Iterable) and not isinstance(contents, str):
        contents = "\n".join(map(str, contents))
    def _inner():
        with open(filename, "w") as f:
            f.write(contents)
    return _inner

def delete_file(filename):
    " Hook for deleting files "
    def _inner():
        os.remove(filename)
    return _inner