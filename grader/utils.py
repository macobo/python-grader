import os
import json
import contextlib
from collections import OrderedDict

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

def beautifyDescription(description):
    lines = (line.strip() for line in description.split('\n'))
    return " ".join(filter(lambda x:x, lines))

def setDescription(function, description):
    function.__doc__ = beautifyDescription(description)


def load_json(json_string):
    " Loads json_string into an dict "
    return json.loads(json_string)


def dump_json(ordered_dict):
    " Dumps the dict to a string, indented "
    #print(ordered_dict)
    return json.dumps(ordered_dict, indent=4, ensure_ascii=False)
