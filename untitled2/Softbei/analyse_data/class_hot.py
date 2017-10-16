#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyltp import Segmentor
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import math
import time

'''
这是获取热度的方法
原理:捉取百度搜索引擎返回来的结果数，通过 math.log(100000000/int(num) 这数学公式获取热度
'''



class Hot:

    def __init__(self, driver):
        self.driver = driver

    def get_hot(self, title):
        hot_words = []
        url = 'http://www.baidu.com'
        self.driver.get(url)
        self.driver.find_element_by_id('kw').send_keys(str(title).decode('utf8'))
        self.driver.find_element_by_id('su').click()
        time.sleep(2)
        try:
            bsobj = BeautifulSoup(self.driver.page_source, 'html.parser')
            div = bsobj.find('div', class_='nums').get_text().encode("utf-8")
            num = re.findall(r'约(.*)个$', div)[0]
            num = num.replace(',', '')
            print '搜索的次数'
            print num
            hot_num = math.log(100000000 / int(num))
        except:
            hot_num=10   #加载不到的异常和搜索不到的,出现num为0，除数不为0的异常，hot_num>9,事件的热度的等级为1
        # 返回热度
        return hot_num


    def judge(self, result):
        hot_level = 0
        if (result > 9):
            hot_level = 1
        elif (4 < result <= 9):
            hot_level = 2
        elif (0 <= result <= 4):
            hot_level = 3
            # print history_level
        return hot_level


    def to_hot_csv(self, csv_name):
        df = pd.read_csv(csv_name)
        title = list(df['标题'])
        tag = df['标记']
        hot_level = []

        # index为下标，j为标记数
        for index, j in enumerate(tag):
            if (j == 1):
                continue
            else:
                title_non_repeat = title[index]
                # print title_non_repeat ,index
                print title_non_repeat,index
                # print "事件:" + title_non_repeat
                # 返回热度数值
                result = self.get_hot(title_non_repeat)
                print '热度数值'
                print result
                # 返回事件热度等级（1,2，3）
                level = self.judge(result)
                print '事件热度等级'
                print level
                hot_level.append(level)
                print '----------------------------------'

        if (len(hot_level) == 0):
            return 'null'
        dict = {

            u'事件热度': hot_level
            # hot_level

        }
        return dict

    def main_void(self, value):
        # csv_name = '../../csv/%s.csv' % (value)
        # print csv_name
        # file_name = '../common/csv/%s/%s_hot.csv' % (value,value)
        # print file_name
        print value
        csv_name = 'C:/untitled2/Softbei/removal_csv/csv/%s.csv' % (value)
        file_name = 'C:/untitled2/Softbei/analyse_data/common/csv/%s/%s_hot.csv' % (value, value)
        print file_name
        dict = self.to_hot_csv(csv_name)
        if (dict == 'null'):
            print '没有可生成的数据'
        else:
            pd.DataFrame(dict).to_csv(file_name, encoding='utf8', index=None)
            print 'csv保存成功，路径：%s'%(file_name)
        print '----------------------*************************-------------------------------'


    def main_hot(self, types):
        self.main_void(types)
        self.driver.close()
        # list = ['eshow', 'news', 'sing', 'sport']
        # for s in list:
        #     self.main_void(s)
        # self.driver.close()

# 函数调用
if __name__ == '__main__':
    Hot(driver=webdriver.Chrome()).main_hot(types='sing')
