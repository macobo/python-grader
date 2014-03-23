from grader import *

@test
def no_writes(m):
    assert m.module.variable == 5

@test
def two_writes(m):
    m.stdin.put('ONE')
    assert m.module.variable == 'ONE'
    m.stdin.put('END')