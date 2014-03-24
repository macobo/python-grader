import grader
from test_base import GraderTestBase


class Tests(GraderTestBase):
    @classmethod
    def setUpClass(cls):
        cls.syntaxerror_tests = cls.run_test('helpers/empty_tester.py', '_helper_invalid_syntax.py')

    def test_syntax(self):
        result = self.find_result("empty", self.syntaxerror_tests)
        assert not result["success"], result
        assert "SyntaxError" in result["traceback"], result