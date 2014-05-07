Extensions API
=========================

This page contains API reference for various extensions of the grader module.

grader.extensions.adv_functions module
--------------------------------------

.. automodule:: grader.extensions.adv_functions
    :members:
    :undoc-members:
    :show-inheritance:

grader.extensions.ast module
----------------------------

Module for testing fill-in-the-blanks task type.

Tester for the example task. ::

    from grader import *
    from grader.extensions import ast

    template = """
    number = int(input("Input a number: "))
    if number > _____: # fill in the blank here...
        print("Non-negative!")
    else:
        ... # and here! Can be several lines
    """

    ast.template_test(template)

Note that additional tests are also needed to verify the behaviour of the program.

.. automodule:: grader.extensions.ast
    :members:
    :undoc-members:
    :show-inheritance:
