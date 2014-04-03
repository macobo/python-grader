import unittest
import os
from os.path import join
from grader.asset_management import tempModule, AssetFolder
from grader.utils import (
    import_module,
    beautifyDescription,
    get_traceback
)

CURRENT_FOLDER = os.path.dirname(__file__)

def readFile(path):
    with open(path) as file:
        return file.read()

class Tests(unittest.TestCase):
    def tempModuleCheck(self, contents, folder):
        with tempModule(contents, folder) as module_path:
            self.assertTrue(os.path.exists(module_path))

            self.assertEqual(readFile(module_path), contents)
        self.assertFalse(os.path.exists(module_path))

    def test_tempModule(self):
        self.tempModuleCheck("HelloWorld\nHello", CURRENT_FOLDER)

    def test_tempModule2(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory(dir=CURRENT_FOLDER) as folder:
            self.tempModuleCheck("Somethingsomething\nSomethingÄÄÄõõõ", folder)

    def test_assets(self):
        with AssetFolder('a', 'b', is_code=True) as assets:
            assert os.path.exists(assets.path)
        assert not os.path.exists(assets.path)

    def test_assets_other_files_code(self):
        with AssetFolder('a', 'b', [{'filename': 'something', 'contents': 'other'}], is_code=True) as assets:
            self.assertEqual(len(assets.other_files), 1)
            f = assets.other_files[0]
            self.assertEqual(os.path.dirname(f), assets.path)
            self.assertEqual(os.path.basename(f), 'something')
            self.assertEqual(readFile(f), 'other')

    def import_check(self, name=None):
        code = (
            'a = 6\n'
            'if __name__ == "__main__":\n'
            '    other = 7'
        )
        with tempModule(code, CURRENT_FOLDER) as module_path:
            if name is not None:
                module = import_module(module_path, name)
            else:
                module = import_module(module_path)
            self.assertEqual(module.a, 6)
            self.assertEqual(hasattr(module, "other"), name == "__main__", module)

    def test_import_module_without_name(self):
        self.import_check()

    def test_import_module_with_explicit_name(self):
        self.import_check("__main__")



    def test_beautifyDescription(self):
        text = "\n".join(["Hello   ", "World ", "", " without excess", "whitespace "])
        self.assertEqual(beautifyDescription(text), 
            "Hello World without excess whitespace")

    def test_beautifyDescription2(self):
        def fun():
            """ This is a multiline docstring.  
                It does wonders to humankind, etcetc. 

                Example: 3 """
            pass

        expected = "This is a multiline docstring. It does wonders to humankind, etcetc. Example: 3"
        self.assertEqual(beautifyDescription(fun.__doc__), expected)

    def test_get_traceback(self):
        try:
            raise ValueError("ErrorMessage")
        except Exception as e:
            traceback = get_traceback(e)
        self.assertIn("Traceback (most recent call last):\n", traceback)
        self.assertIn('File "'+__file__+'", line 86, in test_get_traceback\n', traceback)
        self.assertIn('raise ValueError("ErrorMessage")\n', traceback)
        self.assertIn('ValueError: ErrorMessage\n', traceback)