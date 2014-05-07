import sys

from time import sleep
from threading import Thread
from .utils import read_code
from .stdio import SyncCondition, SpoofedStdin, SpoofedStdout


class ProgramContainer(Thread):
    """ The thread in which the users program runs """

    def __init__(self, module_path, results):
        Thread.__init__(self)

        self.module_path = module_path
        self._results = results
        self.condition = SyncCondition()

        self.caughtException = None
        self.__startProgram()

    def __startProgram(self):
        self.setDaemon(True)
        self.start()
        self._started = False
        #while not self._started:
        #    sleep(0.001)

    def run(self):
        self.stdin = sys.stdin = SpoofedStdin(self.condition)
        self.stdout = sys.stdout = SpoofedStdout()

        self.condition.acquire()
        self._started = True
        self.finished = False

        try:
            self._exec_code()
        except Exception as error:
            self.caughtException = error
        # notify tester of the end of program
        self.condition.notify_release()
        self.condition.finish()
        self.finished = True

    def _exec_code(self):
        from types import ModuleType
        mod = ModuleType("__main__")
        self.module = mod

        source = read_code(self.module_path)
        code = compile(source, "<tested-program>", "exec", dont_inherit=True)
        exec(code, mod.__dict__)
        return mod

    def log(self, what):
        self._results["log"].append(what)

    @classmethod
    def restore_io(cls):
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__