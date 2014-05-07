from grader import *

@test
def empty(m):
    from asset_file import variable
    assert variable == 6
# from grader.extensions import ast

# template = '''
# b = 0
# if not ____:
#     i = 5
# ...
# j = 6
# assert j * i * b == 30
# ...

# '''

# ast.template_test(template_code=template)
