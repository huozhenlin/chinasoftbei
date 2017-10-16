#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

from Softbei.analyse_data.class_age_tf_idf import TfIdf
from Softbei.common.class_database import DB
from Softbei.common.class_switch_method import *

reload(sys)
sys.setdefaultencoding('utf8')

class Age(DB):
    # global drivers
    def __init__(self, driver):
        DB.__init__(self)
        self.driver = driver
        self.login()

    def login(self):
        # 登录到百度指数
        url = 'http://index.baidu.com/'
        # 到百度指数页面
        self.driver.get(url)
        # 定义到搜索输入框
        inputElement = self.driver.find_element_by_xpath('//*[@id="schword"]')
        # 输入查找内容,搜索词默认为中国
        init_value = '中国'.decode('utf8')
        inputElement.send_keys(init_value)
        time.sleep(1)
        submitElement = self.driver.find_element_by_id('searchWords').click()
        # 你的用户名
        yourusername = '13713648593'
        # 你的密码
        yourPW = '856263as'
        try:
            # 自动输入用户名
            self.driver.find_element_by_xpath('//*[@id="TANGRAM_12__userName"]').send_keys(yourusername)
            print 'user success!'
        except:
            print 'user error!'
        time.sleep(1)
        # sign in the pasword
        try:
            # 自动输入密码
            self.driver.find_element_by_xpath('//*[@id="TANGRAM_12__password"]').send_keys(yourPW)
            print 'pw success!'
        except:
            print 'pw error!'
        time.sleep(1)
        # click to login
        try:
            # 提交
            self.driver.find_element_by_xpath('//*[@id="TANGRAM_12__submit"]').click()
            print 'click success!'
        except:
            print 'click error!'
        time.sleep(2)

    # 反复输入关键词查询人群画像
    def get_age(self, value):
        a = Age.selectkeywords(self, value)
        try:
            list = []
            # print a
            if a == 0:  # 在数据库中找不到或不生效的
                # try:
                # 从网页中找
                search_value = value.decode('utf8')
                self.driver.find_element_by_xpath('//*[@id="schword"]').clear()
                self.driver.find_element_by_xpath('//*[@id="schword"]').send_keys(search_value)
                time.sleep(2)
                self.driver.find_element_by_xpath('//*[@id="schsubmit"]').click()
                time.sleep(2)

                # 获得关键字后，点击人群画像
                self.driver.find_element_by_xpath('//*[@id="subNav"]/tbody/tr/td[4]/a').click()
                # 等待加载
                time.sleep(1)
                # except:
                #     print '点击人群画像'
                # 定位svg元素,获取人群属性svg数据
                svgelem = self.driver.find_element_by_css_selector('#grp_social_l > svg')
                action = ActionChains(self.driver)
                action.click(svgelem).perform()

                # 取到各年龄层的值
                bs = BeautifulSoup(self.driver.page_source, 'html.parser')
                # id为crowdsocial，唯一标识
                x = bs.find('div', id='crowdsocial').find('div', class_='grpArea').find('div', id='grp_social').find(
                    'div', id='grp_social_l')
                y = x.find_all('rect')
                for i in y:
                    height = float(i['height'])
                    list.append(height)

                # 从网页中找
                # 关键字记录在数据库,返回找到结果
                # print "从网页查询下来，插入数据库"
                Age.insertkeywords(self, value, list)
                return list

            else:
                # 找到直接返回
                a_list = a.replace('[', '').replace(']', '')
                a_list = a_list.split(',')
                # print type(a_list)
                return a_list
        except Exception as e:
            print e.message
            # 通过关键字查询没有结果，赋给它一个默认值
            # print '从网上找不到，用默认值'
            list = [1, 1, 2, 1, 1]
            # a=Age.selectkeywords(self, value)
            if a == 0:
                Age.insertkeywords(self, value, list)
                return list
            else:
                a_list = a.replace('[', '').replace(']', '')
                a_list = a_list.split(',')
                # print type(a_list)
                return a_list

    def getmore(self, csv_name):
        # 得到tf_id的list
        children = []
        youth = []
        adult = []
        older = []
        data = ['0', '1']
        try:
            # 从csv读取新数据（这里是标题），关键字保存在一个list内;如果读取标题，标记为1，则不进行分析，反之
            tf_list = TfIdf(driver=webdriver.Chrome()).getlist(csv_name)
            print tf_list
            # print "这是一个关键字集合"
            # print tf_list
            # 算出提出关键字有多少组
            first = len(tf_list)
            print first
            if first == 0:
                return 'null'
        except Exception as e:
            return 'null'

        for i in range(first):
            second = len(tf_list[i])
            merge_list = []
            s = []
            for j in range(second):
                value = tf_list[i][j]  # 关键字
                list = self.get_age(value)  # 返回关键字年龄层的值,例[1.0, 20.0, 30.0, 45.0, 50.0]
                merge_list.append(list)
            print merge_list
            if len(merge_list) > 1:
                calu_list = []
                length = len(merge_list[1])
                for x in range(length):
                    list = (float(merge_list[0][x]) + float(merge_list[1][x])) / 2
                    calu_list.append(list)
                list = calu_list
                max_index = list.index(max(list))
            elif (len(merge_list) == 1):
                list = merge_list
                for l in list[0]:
                    s.append(float(l))
                max_index = s.index(max(s))
                # list = merge_list
                # max_index = list.index(max(list))
            else:
                max_index = 2
            print max_index
            # get_num(max_index)
            for case in switch(max_index):
                if case(0):
                    print '儿童'
                    children.append(data[1])
                    youth.append(data[0])
                    adult.append(data[0])
                    older.append(data[0])
                    break
                if case(1):
                    print '青年'
                    children.append(data[0])
                    youth.append(data[1])
                    adult.append(data[0])
                    older.append(data[0])
                    break
                if case(2 or 3):
                    print '成年'
                    children.append(data[0])
                    youth.append(data[0])
                    adult.append(data[1])
                    older.append(data[0])
                    break
                if case(4):
                    print '老年'
                    children.append(data[0])
                    youth.append(data[0])
                    adult.append(data[0])
                    older.append(data[1])
                    break
            print '--------------------------------------'

        dict = {

            u'主要影响年龄层为儿童': children, u'主要影响年龄层为青年': youth, u'主要影响年龄层为成年': adult, u'主要影响年龄层为老年': older,

        }
        return dict

    def main_void(self, value):
        csv_name = 'C:/untitled2/Softbei/removal_csv/csv/%s.csv' % (value)
        file_name = 'C:/untitled2/Softbei/analyse_data/common/csv/%s/%s_age.csv' % (value, value)
        print csv_name
        dict = self.getmore(csv_name)
        print dict
        if dict == 'null':
            print '没有可生成的数据'
        else:
            pd.DataFrame(dict).to_csv(file_name, encoding='utf8', index=None)
        print '--------------------------********************----------------------------------'

    def main_age(self, types):
        self.main_void(types)
        self.driver.close()
        # list = ['eshow', 'news', 'sing', 'sport']
        # for s in list:
        #     self.main_void(s)
        # self.driver.close()


# 函数调用
if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument(
        r'--user-data-dir=C:\Users\hzl\AppData\Local\Google\Chrome\User Data\Default\Default')  # 设置成用户自己的数据目录
    # driver = webdriver.Chrome(chrome_options=option)  # 让浏览器记住用户
    Age(driver=webdriver.Chrome(chrome_options=option)).main_age(types='sing')
