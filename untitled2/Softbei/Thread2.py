#coding:utf8
import sys
import threading
import time
import inspect
import ctypes
from flask import Flask
from Softbei.analyse_data.class_hot import Hot
from selenium import webdriver


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



class Thread2(threading.Thread):
    def run(self):
        # option = webdriver.ChromeOptions()
        # option.add_argument(
        #     r'--user-data-dir=C:\Users\mylay\AppData\Local\Google\Chrome\User Data\Default\Default')  # 设置成用户自己的数据目录
        # # driver = webdriver.Chrome(chrome_options=option)  # 让浏览器记住用户
        # Age(driver=webdriver.Chrome(chrome_options=option)).main_age()
        Hot(driver=webdriver.Chrome()).main_hot()


        # a = DamaiSport('https://s.damai.cn/ticket/sports.html')
        # a = XiLangNews('http://news.sina.com.cn/china/')
        # DamaiSing(threadID=1, name=None, q=None).start_thread()
        # a = DamaiSport(url='https://s.damai.cn/ticket/sports.html')
        # a = XiLangNews('http://news.sina.com.cn/china/')

        # a = Eshow('http://www.eshow365.com/')
        # a = YongleSport('http://www.228.com.cn/category/tiyusaishi/')
        # a = XiLangNews('http://news.sina.com.cn/china/')
        # IdaocaoSing().get_idaocao()
        # DamaiSing(threadID=1, name=None, q=None).start_thread()
        # a = GetData('https://www.damai.cn/projectlist.do?mcid=1')  # 实例化对象，去捉取大麦网的数据
        # pages = a.get_pages()
        # for i in range(1, int(pages) + 1):
        #     url = 'https://www.damai.cn/projectlist.do?mcid=1&pageindex=%d' % (i)
        #     get_content(url)

        # a = DamaiSport('https://s.damai.cn/ticket/sports.html', driver=webdriver.Chrome())
        # a = Weather('http://www.weather.com.cn/alarm/#')
        # a = XiHuaNews('http://www.news.cn/politics/')
        # lock.acquire()
        # lock.release()
        # i=0
        # while True:
        #     i = i+1
        #     time.sleep(1)
        #     print '循环次数', i
        #     lock.acquire()
        #     lock.release()



list_t = []
@app.route('/start')
def start_thread():
    print '-----------------start------------------------------'
    print '-------------------list_o-----------------------'
    print list_t   #第一次开启[<Thread2(Thread-2, initial daemon)>]
    if not any(list_t):
        t = Thread2()
        t.start()
        list_t.append(t)
        print "-----------------获取当前线程名------------------------"
        print t
        print list_t
    elif not list_t[0].isAlive():
        print "开启新的线程"
        # if len(list_t):
        del list_t[0]
        print list_t
        t = Thread2()
        t.start()
        list_t.append(t)
        print list_t



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
    # start_thread()
    # stop_thread()
    app.run(debug=True,threaded=True)
