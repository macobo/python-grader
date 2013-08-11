from grader import Tester, testAll

m = Tester()

@m.test
def simple(m):
    m.stdin.write(3)
    m.stdin.write(3)
    m.stdin.write(3)
    # 3x3x3 cake
    m.stdin.write(1)
    assert "27" in m.stdout.read()

@m.test
def extraPack(m):
    m.stdin.write(3)
    m.stdin.write(7)
    m.stdin.write(5)
    # 3*7*5 = 105 cookies needed
    m.stdin.write(4) # packages per pack
    assert "27" in m.stdout.read()

testAll(m)