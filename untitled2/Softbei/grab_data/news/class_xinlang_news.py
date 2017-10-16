#coding:utf8
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

import time
import sys

from Softbei.common.class_database import DB

reload(sys)
sys.setdefaultencoding('utf-8')


class XiLangNews():

    weather_urls=[]
    def __init__(self,url):
        self.url=url
        self.get_news()


    def get_news(self):
        # driver=webdriver.Chrome()
        i = 0
        driver=webdriver.Chrome()
        driver.get(self.url)
        while i < 300:
            ActionChains(driver).key_down(Keys.DOWN).perform()
            i += 1
        time.sleep(2)
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        div = bs.find('div', id='subShowContent1_news4').find_all('div', class_='news-item')
        # print div
        self.getcontent(div)
        time.sleep(2)
        #循环实现翻页的次数 10次  lmin
        for i in range(10):
            print '****************************************************************************************'
            print i
            driver.find_element_by_link_text('下一页').click()
            while i < 300:
                ActionChains(driver).key_down(Keys.DOWN).perform()
                i += 1
            time.sleep(2)
            bs1 = BeautifulSoup(driver.page_source, 'html.parser')
            div1 = bs1.find('div', id='subShowContent1_news4').find_all('div', class_='news-item')
            self.getcontent(div1)
        driver.close()
            # if ((href[0:4] == "http")):
            #     getcontent(href,title)

    def getcontent(self, div):
        c = DB()
        for i in div:
            try:
                title = i.find('a').string
                href = i.find('a')['href']
                timesource = i.find('div', class_='time').contents[0].strip()
                print timesource
                times = datetime.strptime(timesource, '%m月%d日 %H:%M')
                t = times.strftime('%m/%d')

                print title
                print href
                print t
            except Exception as e:
                print 'not found'
                title = 'null'
                href = 'null'
            if len(c.select_new(table='news', title=title)) == 1: #匹配到会议才插入数据库
                if len(c.select(table='news', title=title)) == 0: #从数据库找不到，才插入，避免重复
                    c.insert_news(table='news', start_time=t, endtime=t, title=title, url=href)
                print '---------------------------------'
            else:
                print '不是会议'


if __name__ == '__main__':
    a=XiLangNews('http://news.sina.com.cn/china/')