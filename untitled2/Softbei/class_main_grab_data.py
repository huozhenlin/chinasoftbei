# coding:utf8
import time

from selenium import webdriver

from Softbei.grab_data.news.class_xinhua_news import XiHuaNews
from Softbei.grab_data.news.class_xinlang_news import XiLangNews
from Softbei.grab_data.show.class_eshow_show import Eshow
from Softbei.grab_data.sing.class_idaocao_sing import IdaocaoSing
from Softbei.grab_data.sport.class_damai_sport import DamaiSport
from Softbei.grab_data.sport.class_yongle_sport import YongleSport
from Softbei.grab_data.void.class_yanchanhui import GetData
from Softbei.grab_data.weather.class_tufa_weather import Weather
from Softbei.to_csv.class_handle_time import HandleTime

'''
高度整合了爬取数据的所有功能
插入数据库之前会对数据进行查询，如果数据库已经存在了该条数据，将不会被插入到数据库中
'''


class GrabData:
    def main_grab_data(self):
        # list = ['eshow', 'news', 'sing', 'sport', 'weather']
        list = ['sport']
        for s in list:
            if s == 'eshow':
                # 展会类
                print '开始爬取e展网-------------------------------------'
                # e展网
                a = Eshow('http://www.eshow365.com/')
                print '--------------------------------------------------********************************------------------------------------------------'
                continue
            elif s =='news':
                #新闻类
                #新华网
                print '开始爬新华网数据-------------------------------------'
                a = XiHuaNews('http://www.news.cn/politics/')
                #新浪网
                print '开始爬新浪网数据'
                a = XiLangNews('http://news.sina.com.cn/china/')
            elif s == 'sing':
                # 大麦网演唱会数据获取，多线程请运行class_damai_sing.py文件
                print '开始爬大麦网演唱会数据-------------------------------------'
                from Softbei.grab_data.sing.class_damai_sing import DamaiSing
                DamaiSing(threadID=1, name=None, q=None, exitFlag=1).start_thread()
                # DamaiSing(threadID=1,name=None, q=None, exitFlag=0)
                # a = GetData('https://www.damai.cn/projectlist.do?mcid=1')  # 实例化对象，去捉取大麦网的数据
                # pages = a.get_pages()
                # print pages
                # for i in range(1, int(pages) + 1):
                #     url = 'https://www.damai.cn/projectlist.do?mcid=1&pageindex=%d' % (i)
                #     # get_content(url)
                #     DamaiSing().get_content(url)
                # 获取爱稻草的数据
                print '开始爬取爱稻草网数据-------------------------------------'
                # get_idaocao()
                IdaocaoSing().get_idaocao()  # 实例化对象，去捉取爱稻草网的数据
                print '--------------------------------------------------********************************------------------------------------------------'
                continue
            elif s == 'sport':
                # 体育类
                # 大麦网
                print '开始爬取大麦网体育类数据-------------------------------------'
                a = DamaiSport('https://s.damai.cn/ticket/sports.html', driver=webdriver.Chrome())
                # 228网
                time.sleep(5)
                print '开始爬永乐票务的体育类数据-------------------------------------'
                # a = YongleSport('http://www.228.com.cn/category/tiyusaishi/')
                print '--------------------------------------------------********************************------------------------------------------------'
                continue
            elif s == 'weather':
                # 天气类
                # 中国天气网
                print '开始爬天气网的数据-------------------------------------'
                a = Weather('http://www.weather.com.cn/alarm/#')
                print '--------------------------------------------------********************************------------------------------------------------'
                continue


if __name__ == '__main__':
    # while (True):
        num = input("请输入要数据爬取的频率，以“天”为单位，如：1天输入1\n", )
        if (num < 0.5):
            print "你输入的频率太快了，系统很吃力的，你可以输入1哦"
        else:
            GrabData().main_grab_data()
            # 插入完数据库后对数据库时间格式化
            # list = ['sing', 'weather', 'sport']
            # for s in list:
            #     HandleTime().main_void(s)
            # print '进入休眠---------------'
            # time.sleep(num * 86400)
