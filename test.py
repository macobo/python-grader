import sys
import json


class DevNull(object):
    def write(self, *args, **kwargs):
        pass

    def flush(*args, **kwargs):
        pass

sys.stdout = DevNull()

stdin = sys.stdin.readline()
code, globals_dict = json.loads(stdin)
sys.stderr.write(str(stdin))

exec(code, globals_dict)

ok_types = (
    type(None), int, float, str, list, tuple, dict
)
bad_keys = ("__builtins__",)


def jsonable(v):
    if not isinstance(v, ok_types):
        return False
    try:
        json.dumps(v)
    except Exception:
        return False
    return True
globals_dict = {
    k: v
    for k, v in globals_dict.items()
    if jsonable(v) and k not in bad_keys
}

json.dump(globals_dict, sys.__stdout__)
