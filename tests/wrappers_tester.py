import unittest
import grader
from test_base import GraderTestBase


class Tests(GraderTestBase):
    solution_path = '_helper_empty_module.py'
    tester_path = 'helpers/wrappers_tester.py'

    @classmethod
    def setUpClass(cls):
        cls.results = cls.run_test(cls.tester_path, cls.solution_path)

    def descriptions(self):
        return [r["description"] for r in self.results]

    def desc_contains(self, what):
        return [r for d, r in zip(self.descriptions(), self.results) if what in d]

    def test_test_cases_single(self):
        results = self.desc_contains("Single arg test_cases")
        assert len(results) == 3, results
        assert all([r["success"] for r in results]), results
        for x in [1,2,3]:
            assert any(str(x) in r["description"] for r in results)

    def test_test_cases_multiple(self):
        results = self.desc_contains("Double arg test_cases")
        assert len(results) == 3, results
        assert all([r["success"] for r in results]), results
        for a,b in [[1,4], [2,5], [3,6]]:
            desc = "Double arg test_cases {} {}".format(a, b)
            assert any(r["description"] == desc for r in results)

    def test_test_cases_wrapped(self):
        results = self.desc_contains("Ast arg test_cases")
        assert len(results) == 3, results
        assert all([r["success"] for r in results]), results
        for a in [1,2,3]:
            desc = "Ast arg test_cases {}".format(a)
            assert any(r["description"] == desc for r in results)
