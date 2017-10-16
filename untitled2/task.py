#coding:utf8
from selenium import webdriver

from Softbei.grab_data.news.class_news import New
from Softbei.grab_data.news.class_xinhua_news import XiHuaNews
from Softbei.grab_data.news.class_xinlang_news import XiLangNews
from Softbei.grab_data.show.class_eshow_show import Eshow
from Softbei.grab_data.sing.class_damai_sing_onethread import get_content
from Softbei.grab_data.sing.class_idaocao_sing import IdaocaoSing
from Softbei.grab_data.sport.class_damai_sport import DamaiSport
from Softbei.grab_data.sport.class_yongle_sport import YongleSport
from Softbei.grab_data.void.class_yanchanhui import GetData
from Softbei.grab_data.weather.class_tufa_weather import TuFaWeather
from untitled2 import Task, tell
import sys
from untitled2 import db
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def taks(id):
    # 获取爬虫配置信息
    args = id
    result = Task.query.filter_by(id=args).first()
    print '----------------线程爬虫已经启动-------------------'
    if result:
        type = ["演唱会类", "展会类", "时政类", "体育赛事类", "异常天气类"]
        types = list(result.types.split(","))

        for x in types:
            if type[int(x)] == "演唱会类":
                # 大麦网演唱会数据获取，多线程请运行class_damai_sing.py文件
                print '开始爬去大麦网演唱会数据'
                a = GetData('https://www.damai.cn/projectlist.do?mcid=1')  # 实例化对象，去捉取大麦网的数据
                pages = a.get_pages()
                for i in range(1, int(pages) / 20 + 1):
                    url = 'https://www.damai.cn/projectlist.do?mcid=1&pageindex=%d' % (i)
                    get_content(url)
                # 获取爱稻草的数据
                print '开始爬取爱稻草网'
                IdaocaoSing().get_idaocao()
            elif type[int(x)] == "展会类":
                # 展会类
                print '开始爬取e展网'
                # e展网
                a = Eshow('http://www.eshow365.com/')
            elif type[int(x)] == "时政类":
                # 新浪网
                # a = XiLangNews('http://news.sina.com.cn/china/')
                # 新华网
                # a = XiHuaNews('http://www.news.cn/politics/')
                New().get_news()
            elif type[int(x)] == "体育赛事类":
                # 体育类
                # 大麦网
                print '开始爬取大麦网体育类数据'
                a = DamaiSport('https://s.damai.cn/ticket/sports.html', driver=webdriver.Chrome())
                # 228网
                print '开始爬去永乐票务的体育类数据'
                a = YongleSport('http://www.228.com.cn/category/tiyusaishi/')
            elif type[int(x)] == "异常天气类":
                # 天气类
                # 中国天气网
                a = TuFaWeather('http://www.weather.com.cn/alarm/#')
                # 修改爬虫状态
        result.status = 1
        db.session.commit()
    else:
        tell(1)
