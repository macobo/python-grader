import unittest
import grader
import ast
from grader.extensions import ast as ast_ext
from textwrap import dedent

parse = lambda code: ast.parse(dedent(code))
compare = ast_ext.compare_trees


def simplify(node):
    if isinstance(node, ast.AST):
        res = vars(node).copy()
        for k in 'lineno', 'col_offset', 'ctx':
            res.pop(k, None)
        for k, v in res.items():
            res[k] = simplify(v)
        res['__type__'] = type(node).__name__
        return res
    elif isinstance(node, list):
        return map(simplify, node)
    else:
        return node


class Tests(unittest.TestCase):
    def test_identical_code(self):
        code = parse("""\
            def function(something): return something
            l = lambda x: 1+2+3

            x() + y()
            """)

        self.assertEqual(compare(code, code), [])

    def test_identical_ast(self):
        tree_1 = parse("""\
        def function(something): return something
        l = lambda x: 1+2+3

        x() + y()
        """)

        tree_2 = parse("""\
        def function(something):
            return something
        l=lambda x: (1 + 2 + 3)

        x()+y()
        """)
        self.assertEqual(compare(tree_1, tree_2), [])

    def test_not_matching(self):
        tree_1 = parse("""\
        def function(something): return something
        l = lambda x: 1+2+3

        x() + y()
        """)

        tree_2 = parse("""\
        def function(something): return something_else
        l = lambda x: 1+(2+3)

        x() + y()
        """)

        result = compare(tree_1, tree_2)
        self.assertEqual(len(result), 3, ast_ext.dump(result))

        self.assertIsInstance(result[0][0], ast.Name)
        self.assertEqual(result[0][1].id, "something_else")

        self.assertEqual(simplify(result[1][0]),
                         simplify(ast.BinOp(left=ast.Num(n=1), right=ast.Num(n=2), op=ast.Add())))

        self.assertEqual(simplify(result[1][1]),
                         simplify(ast.Num(n=1)))

    def test_underscore_single(self):
        template = parse("a = ____")
        tree = parse("a=5")
        self.assertEqual(compare(template, tree), [])

    def test_underscore_several(self):
        template = parse("a = ____ * ____ + 3")
        tree = parse("a=5*(8+2)+3")
        self.assertEqual(compare(template, tree), [])

        tree2 = parse("a= 5 * (4 + 3)")
        result = compare(template, tree2)
        self.assertGreater(len(result), 0, result)

    def test_wildcard_matches(self):
        template = parse("a = 5; ...; b = 6")
        self.assertEqual(compare(template, parse("a = 5; b = 6")), [])
        self.assertEqual(compare(template, parse("a = 5; something+other; b = 6")), [])
        tree3 = parse("""\
        a = 5

        line1
        line2 * statement
        blah

        b = 6
        """)

        self.assertEqual(compare(template, tree3), [])

        tree4 = parse("""\
        a = 5

        if something:
            b = 6
        """)

        self.assertNotEqual(compare(template, tree4), [])

    def test_multiple_wildcards(self):
        template = parse("""\
        a = b
        ...
        c = d
        e = g
        ...
        d = f
        """)

        tree1 = parse("a=b;c=d;e=g;d=f")
        self.assertEqual(compare(template, tree1), [])

        tree2 = parse("""\
        a = b
        if something:
            do_something()
        c = d
        e = g
        statement1
        statement2
        d = f
        """)
        self.assertEqual(compare(template, tree2), [])

        tree3 = parse("something; a=b;c=d;e=g;d=f")
        self.assertNotEqual(compare(template, tree3), [])

        tree4 = parse("a=b;c=d;e=g;d=f;something")
        self.assertNotEqual(compare(template, tree4), [])

    def test_grader_valid(self):
        tester = dedent("""\
        from grader import *
        from grader.extensions import ast

        template = '''
        b = 0
        if not ____:
            i = 5
        ...
        j = 6
        assert j * i * b == 30
        ...

        '''

        ast.template_test(template_code=template)
        """)

        solution_valid = dedent("""\
        b = 0
        if not False:
            i = 5
        b = 1
        j = 6
        assert j * i * b == 30
        """)

        results = grader.test_code(tester, solution_valid)["results"][0]
        assert results["success"], results

    def test_grader_invalid(self):
        tester = dedent("""\
        from grader import *
        from grader.extensions import ast

        template = '''
        b = 0
        if not ____:
            i = 5
        ...
        j = 6
        assert j * i * b == 30
        ...

        '''

        ast.template_test(template_code=template)
        """)

        solution_invalid = dedent("""\
        b = 0
        if not False:
            b = 1
            i = 5
        j = 6
        assert j * i * b == 30
        """)

        results = grader.test_code(tester, solution_invalid)["results"][0]
        assert not results["success"], results
        self.assertIn("Program code does not match template.", results["error_message"])
