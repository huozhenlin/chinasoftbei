# -*- coding: utf-8 -*-
import sys
from Softbei.common.class_switch_method import switch
reload(sys)
sys.setdefaultencoding('utf8')


class Weather_Wanring_Level:


    def getcolor(self, str):
        i='null'
        result='蓝色'
        color = ['蓝色', '黄色', '橙色', '红色']
        for line, i in enumerate(color):
            # print line + 1
            result = str.find(i) != -1
            if result:
                break
        if not result:
            i = 'null'
        return i

    def weather_warning(self, result):
        i = self.getcolor(result)
        level='IV级预警'
        for case in switch(i):
            if case('蓝色'):
                level='IV级预警'
                print 'IV级预警'
                break
            if case('黄色'):
                level='Ⅲ级预警'
                print 'Ⅲ级预警'
                break
            if case('橙色'):
                level='Ⅱ级预警'
                print 'Ⅱ级预警'
                break
            if case('红色'):
                level='I级预警'
                print 'I级预警'
                break
            if case(): # 默认
                level='IV级预警'
                print "something else!"
        return level


