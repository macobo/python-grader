import os
import contextlib

from tempfile import NamedTemporaryFile

@contextlib.contextmanager
def tempModule(code, working_dir, encoding="utf8"):
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