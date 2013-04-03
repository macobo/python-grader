# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:47:20 2013

@author: macobo
"""

import sys
import queue
from time import sleep
from threading import Thread

class Stdin:
    def __init__(self):
        self.queue = queue.Queue()
    def write(self, line):
        self.queue.put(line)
    def readline(self):
        return self.queue.get(timeout = 3)

class Stdout:
    def __init__(self):
        self.output = []
    def flush(self): 
        pass
    def write(self, msg):
        self.output.append(msg)
        
class Module(Thread):
    def __init__(self, filename):
        Thread.__init__(self)
        self.filename = filename
        # this thread doesn't block exiting
        self.setDaemon(True)
        self.start()
    
    def run(self):
        self.stdin = sys.stdin = Stdin()
        self.stdout = sys.stdout = Stdout()
        self.module = __import__(self.filename)
        
def get_module(filename):
    m = Module(filename)
    sleep(0.05) # to assure the thread has started
    return m.module, m.stdin, m.stdout
            
def reset_io():
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
    
