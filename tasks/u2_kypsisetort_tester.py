from grader import *

@test
def simple_test(m):
    " 3*3*3 tort, 1 pakis => 27 pakki "
    m.stdin.write(3)
    m.stdin.write(3)
    m.stdin.write(3)
    # 3x3x3 cake
    m.stdin.write(1)
    assert "27" in m.stdout.read()

@test
def extraPack(m):
    " 3*7*5 tort, 4 pakis => 27 pakki "
    m.stdin.write(3)
    m.stdin.write(7)
    m.stdin.write(5)
    # 3*7*5 = 105 cookies needed
    m.stdout.reset()
    m.stdin.write(4) # packages per pack
    assert "27" in m.stdout.new()