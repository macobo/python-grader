from test_base import GraderTestBase

class Tests(GraderTestBase):
    @classmethod
    def setUpClass(cls):
        tester = 'helpers/empty_tester.py'
        cls.solution_syntaxerror = cls.run_test(tester, '_helper_invalid_syntax.py')
        cls.solution_runerror = cls.run_test(tester, '_helper_runtime_exception.py')

    def test_syntax(self):
        result = self.find_result("empty", self.solution_syntaxerror)
        assert not result["success"], result
        assert "SyntaxError" in result["traceback"], result

    def test_runtime(self):
        result = self.find_result("empty", self.solution_runerror)
        assert not result["success"], result
        assert "NameError" in result["traceback"], result
