# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:47:20 2013

@author: macobo
"""

# TODO: restrict filesystem access? urllib?
import sys
import queue
from time import sleep
from threading import Thread, Lock

d = []
class Stdin:
    def __init__(self, lock):
        self.queue = queue.Queue()
        self.lock = lock
        self.lock.acquire()
    def write(self, line):
        self.queue.put(line)
    def readline(self):
        if self.lock.locked():
            self.lock.release()
            d.append("released")
        result = self.queue.get(timeout = 3)
        self.lock.acquire()
        d.append("aquired")
        return result

class Stdout:
    def __init__(self):
        self.output = []
    def flush(self): 
        pass
    def write(self, msg):
        self.output.append(msg)
    def read(self):
        return self.output
        
class Module(Thread):
    def __init__(self, filename):
        Thread.__init__(self)
        self.filename = filename
        self.lock = Lock()
        # this thread doesn't block exiting
        self.setDaemon(True)
        self.start()
        sleep(0.05) # to assure the thread has started
    
    def run(self):
        self.stdin = sys.stdin = Stdin(self.lock)
        self.stdout = sys.stdout = Stdout()
        self.module = __import__(self.filename)
        
def get_module(filename):
    m = Module(filename)
    return m.module, m.stdin, m.stdout
            
def reset_io():
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__