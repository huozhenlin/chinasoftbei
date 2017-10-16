#coding:utf8
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
#获得数据库连接
from Softbei.common.class_database import DB


class XiHuaNews(DB):
    def __init__(self,url):
        self.url=url
        self.get_news()


    def get_news(self):
        driver=webdriver.Chrome()
        driver.get(self.url)
        # content=driver.page_source
        # while True:
        #     time.sleep(3)
        #     driver.find_element_by_id('dataMoreBtn').click()
        # print content
        # bs=BeautifulSoup(driver.page_source,'html.parser')
        # x=bs.find('div',class_='con')#获取到li,直接返回元素
        # li=x.find_all('li',class_='clearfix')    #返回一个list
        # getMore(li,c)
        #循环实现加载的次数
        for i in range(12):
            driver.find_element_by_id('dataMoreBtn').click()
            time.sleep(2)
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        x = bs.find('div', class_='con')  # 获取到li,直接返回元素
        li = x.find_all('li', class_='clearfix')  # 返回一个list
        self.getmore(li)
        driver.close()
        # print '---------'

    def getmore(self, li):
        global times
        c = DB()
        try:
            for x in li:
                title = x.find('a').string
                href = x.find('a')['href']
                # contents = x.find('p', class_='summary').string
                times = x.find('span', class_='time').string
                print times
                if times is None:
                    times = 'null'
                    print times
                else:
                    # print 'hhh'
                    ts = times.replace('-', '/').split()[0]
                    print ts
                print title
                print href
                # print contents
                # print times
                # print len(c.select(table='news', title=title))
                if len(c.select_new(table='news', title=title)) == 1: #匹配到会议才插入数据库
                    if len(c.select(table='news', title=title)) == 0: #从数据库找不到，才插入，避免重复
                        c.insert_news(table='news', start_time=ts, endtime=ts, title=title, url=href)
                else:
                    print '不是会议'
                print '------------------------------------------------'
        except Exception as e:
            print e.message
            # if (len(contents) == 0):
            #     contents = 'null'  # (table,time,title,url,contents)

if __name__ == '__main__':
    a=XiHuaNews('http://www.news.cn/politics/')