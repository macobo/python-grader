import os
import contextlib
from shutil import copy, rmtree
from tempfile import NamedTemporaryFile, mkdtemp, gettempdir


@contextlib.contextmanager
def tempModule(code, working_dir=None, encoding="utf8"):
    if working_dir is None:
        working_dir = gettempdir()
    file = NamedTemporaryFile(
        dir=working_dir,
        mode="wb",
        suffix=".py",
        delete=False
    )
    file.write(code.encode(encoding))
    file.close()
    try:
        yield file.name
    finally:
        os.remove(file.name)


class AssetFolder:
    def __init__(self, tester_path, solution_path, other_assets=[], is_code=False):
        self.path = mkdtemp()
        if is_code:
            creator_function = self._write
        else:
            creator_function = self._copy
        if tester_path:
            self.tester_path = creator_function(tester_path)
        if solution_path:
            self.solution_path = creator_function(solution_path)

        self.other_assets = list(map(creator_function, other_assets))

    def _copy(self, file_path):
        if os.path.isdir(file_path):
            files = os.listdir(file_path)
            return [self._copy(os.path.join(file_path, name)) for name in files]
        return copy(file_path, self.path)
  
    def _write(self, code):
        file = NamedTemporaryFile(
            dir=self.path,
            mode="w",
            suffix=".py",
            delete=False
        )
        file.write(code)
        file.close()
        return file.name

    def remove(self):
        if not os.path.exists(self.path):
            raise IOError("{} already doesn't exist".format(self.path))
        rmtree(self.path)

    def __str__(self):
        return "<Assets: %s %s %s>" % (self.tester_path, self.solution_path, self.other_assets)
