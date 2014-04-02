import unittest
import grader
from textwrap import dedent


class Tests(unittest.TestCase):
    def test_tester_invalid_syntax(self):
        results = grader.test_code("some invalid code", "")
        assert not results["success"]
        self.assertEquals(results["reason"], "Load tests failure", results)
        self.assertIn("SyntaxError:", results["extra_info"]["error_message"])

    def test_tester_no_tests(self):
        results = grader.test_code("", "")
        assert not results["success"]
        self.assertEquals(results["reason"], "No tests found in tester", results)

    def test_invalid_sandbox(self):
        results = grader.test_code("", "", sandbox_cmd="invalid_command_123 4 5 6")
        assert not results["success"], results
        self.assertIn("Invalid command: invalid_command_123 4 5 6", results["reason"])

    def test_solution_syntaxerror_does_not_raise(self):
        results = grader.test_code(dedent("""\
        from grader import *
        @test
        def empty(m): pass
        """), "invalid_syntax")
        assert results["success"], results

    def test_docker_sandbox(self):
        results = grader.test_code(dedent("""\
        from grader import *
        @test
        def empty(m): pass
        """), "", sandbox_cmd="docker")
        if results["success"]:
            assert results["success"], results
        else:
            # skip on filesystems without docker
            self.assertIn("Invalid command: docker", results["reason"])
