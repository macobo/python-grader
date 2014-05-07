import os
import sys
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
    def __init__(self, tester_path, solution_path, other_files=[], is_code=False, add_to_path=True):
        self.path = mkdtemp()
        if is_code:
            creator_function = self._write
        else:
            creator_function = self._copy

        self.tester_path = creator_function(tester_path)
        self.solution_path = creator_function(solution_path)
        if is_code:
            self.other_files = list(map(self.write_asset, other_files))
        else:
            self.other_files = list(map(self._copy, other_files))

        self.add_to_path = add_to_path
        if add_to_path:
            sys.path.append(self.path)
            self.original_cwd = os.getcwd()
            os.chdir(self.path)

    def _copy(self, file_path):
        # returns path
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

    def write_asset(self, asset_info):
        path = os.path.join(self.path, os.path.basename(asset_info["filename"]))
        with open(path, "w") as f:
            f.write(asset_info["contents"])
        return path

    def remove(self):
        if self.add_to_path:
            sys.path.remove(self.path)
            os.chdir(self.original_cwd)
        if not os.path.exists(self.path):
            raise IOError("{} already doesn't exist".format(self.path))
        rmtree(self.path)

    def files_in_path(self):
        return os.listdir(self.path)

    def __enter__(self): 
        return self

    def __exit__(self, *args):
        self.remove()

    def __str__(self):
        return "<Assets: %s %s %s>" % (self.tester_path, self.solution_path, self.other_files)
