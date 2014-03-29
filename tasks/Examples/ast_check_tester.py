from grader import *
from grader.extensions import ast

template = """
a = [1,2,3]
b = _______
c = b

b.append(4)

print(c) # should print [1 ,2, 3, 4]
print(b) # should print [1 ,2, 3, 4]
print(a) # should print [1 ,2, 3]
"""

ast.template_test(template_code=template)
io_test("Program should have correct output", [], "[1, 2, 3, 4]\n[1, 2, 3, 4]\n[1, 2, 3]")