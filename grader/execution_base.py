import sys
import queue
from time import sleep
from threading import Thread, Lock

# d = []
class Stdin:
    def __init__(self, lock):
        self.queue = queue.Queue()
        self.lock = lock
        self.lock.acquire()

    def write(self, line):
        self.queue.put(str(line))
        sleep(0.01)

    def readline(self):
        if self.lock.locked():
            self.lock.release()
            # d.append("released")
        result = self.queue.get(timeout = 3)
        self.lock.acquire()
        # d.append("aquired")
        return result

class Stdout:
    def __init__(self):
        self.reset()

    def flush(self): pass

    def write(self, msg):
        self.output.append(msg)

    def reset(self):
        self.output = []
        self.lastread = 0

    def read(self):
        self.lastread = len(self.output)
        return "".join(self.output)

    def new(self):
        " returns the new elements in stdout since the last read "
        result = "".join(self.output[self.lastread:])
        self.lastread = len(self.output)
        return result
        
class Module(Thread):
    def __init__(self, filename):
        Thread.__init__(self)
        self.filename = filename
        self.lock = Lock()
        # this thread doesn't block exiting
        self.setDaemon(True)
        self.start()
        sleep(0.05)
    
    def run(self):
        self.stdin = sys.stdin = Stdin(self.lock)
        self.stdout = sys.stdout = Stdout()
        self.module = __import__(self.filename)