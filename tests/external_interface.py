import unittest
import grader
from textwrap import dedent

def command_exists(cmd):
    import subprocess
    status, _ = subprocess.getstatusoutput(cmd)
    return status == 0


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

    @unittest.skipIf(not command_exists('docker'), 'requires docker')
    def test_docker_sandbox(self):
        results = grader.test_code(dedent("""\
        from grader import *
        @test
        def empty(m): pass
        """), "", sandbox_cmd="docker")
        assert results["success"], results

    def tests_assets_are_importable_at_test_registration(self):
        # TODO: check sys.path size
        asset_code = {
            "filename": "asset_file.py",
            "contents": "exists = True"
        }

        results = grader.test_code(dedent("""\
        from grader import *
        import asset_file
        @test
        def empty(m):
            assert asset_file.exists
        """), "", [asset_code])

        assert results["success"], results
        assert results["results"][0]["success"], results

    def test_assets_available_while_running(self):
        # TODO: check sys.path size
        asset_code = {
            "filename": "file.txt",
            "contents": "secret"
        }

        results = grader.test_code(dedent("""\
        from grader import *
        @test
        def empty(m):
            assert m.stdout.read().strip() == 'secret'
        """), "print(open('file.txt').read())", [asset_code])

        assert results["success"], results
        assert results["results"][0]["success"], results["results"][0]
