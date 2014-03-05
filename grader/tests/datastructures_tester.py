import unittest
from ..datastructures import OrderedTestcases

class Tests(unittest.TestCase):
    def setUp(self):
        self.cases = OrderedTestcases()

    def test_simple(self):
        assert len(self.cases) == 0
        self.cases.add('key', 'value')
        self.cases.add('another', 2)
        self.cases.add('value', 3)
        assert len(self.cases) == 3
        assert list(self.cases.values()) == [
            ('key', 'value'),
            ('another', 2),
            ('value', 3)
        ], list(self.cases.values())

    def test_rename(self):
        self.cases.add('key', 'value')
        self.cases.add('another', 2)
        self.cases.add('value', 3)

        self.cases.rename('another', 'new')

        assert list(self.cases.values()) == [
            ('key', 'value'),
            ('new', 2),
            ('value', 3)
        ], list(self.cases)

    