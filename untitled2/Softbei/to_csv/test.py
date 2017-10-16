# coding:utf8
import sys
import time

from datetime import datetime

from Softbei.common.class_database import DB

reload(sys)
sys.setdefaultencoding('utf8')

c = DB()
# u = ['常年']
# print type(u)
#
# print isinstance(u, (unicode, str, int))

# a = []
# print len(a)

# ctime = time.strftime("%Y-%m-%d", time.localtime())
# print ctime # 2017-08-17
# print type(ctime)

# data = str([1.0, 20.0, 30.0, 45.0, 50.0])
# print type(data)

# print len(0)

# s = [1.0, 20.0, 30.0, 45.0, 50.0]
# c.insertkeywords('你好', s)
#
# a=c.selectkeywords('第95')
# print a
# print type(a)
#
# a = a.replace('[', '').replace(']', '')
# a = a.split(',')
# print type(a)
#
# value=int(a[0])
# print type(value)

#22222222222222

# l = [[1.5, 37.5, 81.0, 15.0, 15.0]]
# l = [[u'1', u' 1', u' 2', u' 1', u' 1']]
# x=l[0]
# print len(l)
# print type(x)
# print x[0]
# print type(x[0])
# s = []
# for i in l[0]:
#     s.append(float(i))
#
# print s.index(max(s))
# print x.index(max(x))
# max_index = l.index(max(list[0]))   错误

# a_list = s.replace('[', '').replace(']', '')
# a_list = a_list.split(',')
#
#
# max_index = a_list.index(max(list))
#
# print max_index
# a_List = []
# for i in range(len(a)):
#     a[i] = a[i].replace("'", '')
#     a_List.append(a[i])
# print a_List
# print type(a_List)

# y=ctime.split('-')[0]
# m=ctime.split('-')[1]
# d=ctime.split('-')[2]
# curtime = datetime.date(int(y), int(m), int(d))
# print curtime
# print type(curtime)

# 时间字符串解析为时间元组
# t = time.strptime(ctime, "%Y-%m-%d") #string -- 时间字符串,format -- 格式化字符串。
# print t
# y, m, d = t[0:3]
# curtime = datetime.date(y, m, d)
# print curtime


# x = 0
# def add(a, b):
#     return a+b
#
# for i in range(4):
#     print add(1,2)
#     x = x + 1
# print x
#
# s = []
# x = len(s)
# print x

# timesource='8月19日 07:04'
# times = datetime.strptime(timesource, '%m月%d日 %H:%M')
# print times
# t=times.strftime('%m/%d')
# print type(t)
# print t

# print type(times)
# t=times.replace('-', '/')
# print t
# title='你好'
title='十二届全国人大常委会第29次将在京'
a=c.select_new(table='news', title=title)

print len(a)

# str='\xe4\xbd\xa0\xe5\xa5\xbd'.decode('utf8')
# print str