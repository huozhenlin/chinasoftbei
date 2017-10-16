# -*- coding: utf-8 -*-
# !/usr/bin/env python
import math
import re
import time
from pyltp import Segmentor
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from Softbei.common.class_database import DB

stopwords = {}.fromkeys([line.rstrip() for line in open(r'C:\untitled2\softbei\data\tingyongci')])  # 去掉停用词
segmentor = Segmentor()
segmentor.load(r'C:\BaiduNetdiskDownload\ltp_data\cws.model')  # 分句模型

'''
这是第二种获取关键字的方法
原理:捉取百度搜索引擎返回来的结果数，通过 math.log(100000000/int(num) 这数学公式获取热度
因为分词后词词出现的次数越大，结果越小，那么这个就是关键字
'''


class TfIdf(DB):

    def __init__(self, driver):
        DB.__init__(self)
        self.driver = driver

    def get_num(self, title):
        global hot_num
        hot_words = []
        url = 'http://www.baidu.com'
        for x in title:
            # print x
            # 去掉停用词
            if x not in stopwords:
                a = TfIdf.selecthotwords(self, x)
                print '*****************************'
                print a
                # 在数据库找不到或者不生效的词，必须从网页上找
                if a == -1:
                    self.driver.get(url)
                    self.driver.find_element_by_id('kw').send_keys(str(x).decode('utf8'))
                    self.driver.find_element_by_id('su').click()
                    time.sleep(3)
                    bsobj = BeautifulSoup(self.driver.page_source, 'html.parser')
                    try:
                        div = bsobj.find('div', class_='nums').get_text().encode("utf-8")
                        num = re.findall(r'约(.*)个$', div)[0]
                        num = num.replace(',', '')
                        hot_num = math.log(100000000 / int(num))
                        # print hot_num
                    except Exception as e:
                        hot_num = 0  # hot_num<1.0,不是热词，如果搜索不到，默认不是热词
                else:
                    # 能从数据库找到
                    hot_num = a

                if hot_num > 1.0:
                    print x, hot_num
                    hot_words.append(x)

                if hot_num < 2.0:
                    # 常用词
                    # 找不到或不生效，才能插入数据库，避免重复插入
                    # print 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
                    # print a
                    # print 6666666666
                    print a
                    if a == -1:
                        TfIdf.inserthotwords(self, x, hot_num)
                    # elif a == -2:
                    #     TfIdf.updatehot_num(self, hot_word=x, hot_num=hot_num)

        # print "这些是热词"
        # print hot_words
        # 返回关键字
        return hot_words

    '''
    这个是对标题进行分词的模块
    方法接收一个参数，为待分词的标题
    采用本地分词，效率高
    顺便加强了分词效果，像一些专用名词，我们不会对其进行拆解
    '''

    def fenci(self, title):
        # 将专用名词提取出来，像被'《》，“”，【】'等符号包括的
        special_word = []
        try:
            kw = re.findall(r'“(.*)”', title)[0]
            special_word.append(kw)
        except Exception as e:
            pass
        try:
            kw = re.findall(r'《(.*)》', title)[0]
            special_word.append(kw)
        except Exception as e:
            pass
        try:
            kw = re.findall(r'【(.*)】', title)[0]
            special_word.append(kw)
        except Exception as e:
            pass
        try:
            kw = re.findall(r'[(.*)]', title)[0]
            special_word.append(kw)
        except Exception as e:
            pass

        words = segmentor.segment(title)  # 分词
        key_word = []
        if len(special_word) != 0:
            key_word.append(special_word[0])

        result = self.get_num(words)
        # print result
        # 把分词后的词语
        for x in result:
            # 将专用名词提取出来
            # print 'special_word'
            # print special_word
            if len(special_word) != 0:
                if x not in special_word[0]:
                    key_word.append(x)
            else:
                key_word.append(x)

        # print '------------------------------------------------'
        # print key_word
        for b in key_word:
            print b

        return key_word

    # fenci("(预告)11月11日任贤齐游鸿明参加江阴农商行之夜演唱会")

    def getlist(self, csv_name):
        s = []
        # str = 'sport'
        # print csv_name
        # 从数据库读出来的csv
        df = pd.read_csv(csv_name)
        title = list(df['标题'])
        tag = df['标记']

        # index为下标，j为标记数
        for index, j in enumerate(tag):
            if (j == 1):
                continue
            else:
                titles = title[index]
                print titles, index
                words = self.fenci(titles)
                print len(words)
                print '--------------------------------------------------------'
                value = words[:2]  # 取两个关键字
                s.append(value)  # 关键字的列表(两个一组)
                print s

        # if str in csv_name:
            # print str
        self.driver.close()
        return s

        # result=Tf_Idf().fenci("薛之谦“我好像在哪见过你”—2017全国巡回演唱会青岛站")
        # print result
        #
        # vaule=result[:2]
        # print vaule
