from grader import Tester, testAll

t = Tester()

@t.test
def simple_test(m):
    m.stdin.write(3)
    m.stdin.write(3)
    m.stdin.write(3)
    # 3x3x3 cake
    m.stdin.write(1)
    assert "27" in m.stdout.read()

@t.test
def extraPack(m):
    m.stdin.write(3)
    m.stdin.write(7)
    m.stdin.write(5)
    # 3*7*5 = 105 cookies needed
    m.stdout.reset()
    m.stdin.write(4) # packages per pack
    assert "27" in m.stdout.new()


if __name__ == "__main__":
    testAll(t)