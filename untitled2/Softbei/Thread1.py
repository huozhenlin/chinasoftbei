import threading
import time
import inspect
import ctypes
lock = threading.RLock()

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
    print thread

class Thread1(threading.Thread):
    def run(self):
        i = 0
        print "begin"
        while True:
            i += 1
            print i
            time.sleep(1)
            lock.acquire()
            lock.release()
        print "end"

if __name__ == "__main__":
    t = Thread1()
    print t
    t.start()
    time.sleep(2)
    stop_thread(t)
    print t
    print "stoped"