#coding:utf8
import sys
import threading
import time
import inspect
import ctypes
from flask import Flask,request
# from untitled2 import taks
lock = threading.RLock()
app=Flask(__name__)
# res = 1
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    print '-------------res------------', res   #res 值为1
    if res == 0:
        print 'hello'
        raise SystemError("invalid thread id")
    elif res == 1:
        # ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("invalid")
    elif res != 1:
        print "stoped"
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
list_t = []
global ids
class Thread2(threading.Thread):
    global ids
    def run(self):
        taks(id=ids)




@app.route('/start',methods=['GET'])
def start_thread():
    global ids
    args=request.args.get('id')
    ids=args
    if not any(list_t):
        t = Thread2()
        t.start()
        list_t.append(t)
    elif not list_t[0].isAlive():
        print "开启新的线程"
        del list_t[0]
        t = Thread2()
        t.start()
        list_t.append(t)


@app.route('/stop')
def stop_thread():
    print '-------stop---------'
    print list_t
    if list_t:
        t = list_t[0]
        print t
        _async_raise(t.ident, SystemExit)
    else:
        print '线程未开启'
    #下边没有执行到线程就停止




if __name__ == "__main__":
    app.run(debug=True,threaded=True)
