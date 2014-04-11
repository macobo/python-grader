from grader import *
import ast

@test_cases(
    [1, 2, 3],
    description="Single arg test_cases {}"
)
def t(m, arg):
    assert arg in [1,2,3]

@test_cases(
    [[1,4], [2,5], [3,6]],
    description="Double arg test_cases {} {}"
)
def y(m, a1, a2):
    assert a1 in [1,2,3]
    assert a2 - a1 == 3

@expose_ast
@test_cases(
    [1, 2, 3],
    description="Ast arg test_cases {}"
)
def a(m, arg, AST):
    assert arg in [1,2,3]
    assert isinstance(AST, ast.AST)