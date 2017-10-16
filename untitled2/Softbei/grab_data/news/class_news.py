#coding:utf8
import re
import math
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import sys
from newspaper import Article
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from Softbei.common.class_database import DB
reload(sys)
sys.setdefaultencoding('utf8')


url='http://news.baidu.com/ns?word=峰会+召开&tn=news&from=news&cl=2&rn=20&ct=1'
url_baidu = 'http://www.baidu.com'
c=DB()

list_url = []

class New:
    # def __init__(self):
    #     self.get_news()

    def analyse(self, x):
        for i in x:
            title = i.find('h3').find('a').text  #链接标题
            if len(c.select_news(url_title=title)) == 0:
                # c.insert_filter_news(title=title)  # 在filter_news表中未找到标题存进数据库
                # hot_num = float(self.get_hot(title=title)) #获取热度值
                # if hot_num < 7.6:
                #     print hot_num
                href = i.find('h3').find('a')['href']
                try:
                    times = i.find('div', class_='c-summary').find('p').string
                    t = times.split()[1]
                    t = datetime.strptime(t, '%Y年%m月%d日')
                    # print t  #2017-08-23 00:00:00print title
                    ctime = datetime.strftime(t, '%Y/%m/%d')

                except Exception as e:
                    now = datetime.now()
                    t = datetime.strftime(now, '%Y/%m/%d')
                    ctime = t
                print href
                print ctime

                c.insert_news(start_time=ctime, url_title=title, url=href)
            else:  # 已存在
                print '存在'


    def get_news(self):
        i = 0
        driver = webdriver.Chrome()
        driver.get(url)
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        x = bs.find('div' , id='content_left').find_all('div',class_="result")
        self.analyse(x)
        for x in range(0):
            print '下一页'
            time.sleep(2)
            driver.find_element_by_link_text("下一页>").click()
            time.sleep(2)
            bs1 = BeautifulSoup(driver.page_source, 'html.parser')
            x1 = bs1.find('div', id='content_left').find_all('div', class_="result")
            self.analyse(x1)
        driver.close()
        time.sleep(2)
        #爬取完毕后，更新正文
        c.get_news_content()  # 更新正文


    # def get_hot(self, title):
    #     hot_words = []
    #     self.driver.get(url_baidu)
    #     self.driver.find_element_by_id('kw').send_keys(str(title).decode('utf8'))
    #     self.driver.find_element_by_id('su').click()
    #     time.sleep(2)
    #     try:
    #         bsobj = BeautifulSoup(self.driver.page_source, 'html.parser')
    #         div = bsobj.find('div', class_='nums').get_text().encode("utf-8")
    #         num = re.findall(r'约(.*)个$', div)[0]
    #         num = num.replace(',', '')
    #
    #         hot_num = math.log(100000000 / int(num))
    #     except:
    #         hot_num = 11# 加载不到的异常和搜索不到的,出现num为0，除数不为0的异常   1000条
    #     # 返回热度
    #     return hot_num


if __name__ == '__main__':
    New().get_news()
    # ToCsv().main_to_csv(types='news')
    # Removal().main_removal(types='news')






