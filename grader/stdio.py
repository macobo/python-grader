from threading import Condition
from queue import Queue
from time import sleep


class SyncCondition(Condition):
    def __init__(self):
        self.finished = False
        self.release_count = 0
        Condition.__init__(self)

    def notify_release(self):
        if self.finished: return
        self.release_count += 1
        self.notify()
        self.release()

    def wait_next_release(self):
        if self.finished: return
        target_release_count = self.release_count
        while self.release_count <= target_release_count:
            sleep(0.00001)

    def finish(self):
        # called by program container, to mark that everything is finished
        self.finished = True


class SpoofedStdin:
    def __init__(self, condition):
        self.out = Queue()
        self.condition = condition

    def put(self, line):
        # cond should be acquired by tester
        self.out.put(line)
        #print("put", line, self.out)
        self.condition.notify_release()
        # users program does their thing
        #print("released by put, waiting until next release")
        self.condition.wait_next_release()
        # let me do my thing now!
        self.condition.acquire()
        #print("acquired by put")

    def write(self, line):
        self.put(line)

    def readline(self):
        self.condition.notify_release()

        #print("released by read, waiting until next release")
        self.condition.wait_next_release()
        # tester does its thing
        self.condition.acquire()
        #print("acquired by put")
        return self.out.get(timeout=1)


class SpoofedStdout:
    def __init__(self):
        self.reset()

    def flush(self):
        pass

    def write(self, msg):
        self.output.append(msg)

    def reset(self):
        self.output = []
        self.lastread = 0

    def read(self):
        self.lastread = len(self.output)
        result = "".join(self.output)
        return result

    def new(self):
        " Utility method, returns new things written to stdout since last .new() call. "
        result = "".join(self.output[self.lastread:])
        self.lastread = len(self.output)
        return result
