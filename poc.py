from threading import Thread, Condition
from queue import Queue
from time import sleep

class SyncCondition(Condition):
    def __init__(self):
        self.release_count = 0
        Condition.__init__(self)

    def notify_release(self):
        self.notify()
        self.release()
        self.release_count += 1

    def wait_next_release(self,a):
        target_release_count = self.release_count
        print("waiting... by", a, )
        while self.release_count <= target_release_count:
            sleep(0.00001)



class Stdin:
    def __init__(self, condition):
        self.count = 0
        self.out = Queue()
        self.condition = condition

    def put(self, line):
        # cond should be acquired by tester
        self.out.put(line)
        print("put", line, self.out)
        self.condition.notify_release()
        # users program does their thing
        print("released by put, waiting until next release")
        self.condition.wait_next_release("put")
        # let me do my thing now!
        self.condition.acquire()
        print("acquired by put")

    def read(self):
        self.condition.notify_release()

        print("released by read, waiting until next release")
        self.condition.wait_next_release("read")
        # tester does its thing
        self.condition.acquire()
        print("acquired by put")
        return self.out.get(timeout=1)

class UserProgram(Thread):
    def __init__(self):
        Thread.__init__(self)

        print("released by read, waiting until next release")
        self.condition = SyncCondition()
        self.stdin = Stdin(self.condition)
        self.setDaemon(True)
        self.a = 0

    def start(self, *args, **kwargs):
        Thread.start(self, *args, **kwargs)

    def output(self, value):
        print("UserProgram {}: {}\n".format(self.a, value))
        self.a += 1

    def run(self):
        self.condition.acquire()
        self.output("started!")
        for i in "abcd":
            self.output("reading...")
            a = self.stdin.read()
            self.output(i + a)

        self.output("Ending users program")
        # end of program
        self.condition.notify_release()

UP = UserProgram()
UP.start()

condition = UP.condition
condition.acquire()
print("HAI")

UP.stdin.put("first")
UP.stdin.put("second")
UP.stdin.put("third")
#UP.stdin.put("fourth")

print("put done!")