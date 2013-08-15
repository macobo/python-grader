from grader import Tester, testAll, io_test

t = Tester()
conciseOne = io_test(t, "conciseOne", [500, 5], "638")
conciseTwo = io_test(t, "conciseTwo", [0, 10], "0.")

if __name__ == '__main__':
    testAll(t)