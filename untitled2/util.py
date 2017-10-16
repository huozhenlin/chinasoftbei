#coding:utf8
import time,datetime
from time import strftime,gmtime

class Util:
    def __init__(self):
        self.ctime=time.strftime("%Y-%m-%d", time.localtime())
        t = time.strptime(self.ctime, "%Y-%m-%d")
        y, m, d = t[0:3]
        self.curtime = datetime.date(y, m, d)

    def get_curtime(self):
        return strftime("%Y-%m-%d %H:%M:%S", time.localtime())
