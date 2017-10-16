# coding:utf-8
import json
import re

import MySQLdb
import datetime

import pandas as pd
from newspaper import Article
from selenium import webdriver
from bs4 import BeautifulSoup

import time
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# 获得连接对象
class DB:
    # 构造函数
    def __init__(self):
        self.conn = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="1234",
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.ctime = time.strftime("%Y-%m-%d", time.localtime())
        t = time.strptime(self.ctime, "%Y-%m-%d")
        y, m, d = t[0:3]
        self.curtime = datetime.date(y,m,d)

        # 创建数据库
        # database_sql = "create database if NOT EXISTS Softbei"
        # self.cursor.execute(database_sql)

        # 选择数据库
        self.conn.select_db('Softbei')

        # table_sql = "create table if not EXISTS  news(id  int(255) PRIMARY KEY NOT NULL AUTO_INCREMENT," \
        #             "start_time varchar(255) NULL," \
        #             "title  varchar(100) NULL," \
        #             "url  varchar(100) NULL," \
        #             "place  varchar(100) NULL," \
        #             "contents  text NULL)"
        # self.cursor.execute(table_sql)

    '''
       def __init__(self):
        self.conn = MySQLdb.connect(
            host="localhost",
            user="yzx",
            passwd="123456",
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        # 创建数据库
        database_sql = "create database if NOT EXISTS Softbei"
        self.cursor.execute(database_sql)

        # 选择数据库
        self.conn.select_db('Softbei')
        table_sql = "create table if not EXISTS weather(id INT (255) PRIMARY KEY auto_increment," \
                    "start_time VARCHAR (255) NULL ," \
                    "url VARCHAR (100) NULL," \
                    "title VARCHAR (50))"
        self.cursor.execute(table_sql)

        # table_sql = "create table if not EXISTS  news(id  int(255) PRIMARY KEY NOT NULL AUTO_INCREMENT," \
        #             "start_time varchar(255) NULL," \
        #             "title  varchar(100) NULL," \
        #             "url  varchar(100) NULL," \
        #             "contents  text NULL)"
        table_sql = "create table if not EXISTS  news(id  int(255) PRIMARY KEY NOT NULL AUTO_INCREMENT," \
                     "start_time varchar(255) NULL," \
                     "title  varchar(100) NULL," \
                     "url  varchar(100) NULL," \
		              "place  varchar(100) NULL," \
                     "contents  text NULL)"
        self.cursor.execute(table_sql)


        table_sql = "create table if not EXISTS  eshow(id  int(255) PRIMARY KEY NOT NULL AUTO_INCREMENT," \
                    "start_time varchar(255) NULL," \
                    "endtime  varchar(100) NULL," \
                    "title  varchar(255) NULL," \
                    "url  varchar(100) NULL," \
                    "place varchar(100) NULL, " \
                    "hangye varchar(100) NULL," \
                    "hold_num varchar(100) NULL," \
                    "hold_cycle varchar(100) NULL," \
                    "zhanguan varchar(100) NULL," \
                    "zhuban varchar(255) NULL)"
        self.cursor.execute(table_sql)

        table_sql = "create table if not EXISTS  sport(id  int(255) PRIMARY KEY NOT NULL AUTO_INCREMENT," \
                    "start_time  varchar(100) NULL," \
                    "title  varchar(255) NULL," \
                    "url  varchar(100) NULL," \
                    "changuan varchar(100) NULL)"
        self.cursor.execute(table_sql)
    '''

    # 往新闻表中插入数据
    # def insert_news(self, table, start_time, title, url, contents):
    #     try:
    #         sql = "insert into %s VALUES (NULL ,'%s','%s','%s','%s',NULL)" % (table, start_time, title, url, contents)
    #         print sql
    #         self.cursor.execute(sql)  # 执行语句
    #         self.conn.commit()
    #     except Exception as e:
    #         print '执行错误，数据回滚'
    #         self.conn.rollback()

    #新闻筛选表
    def insert_filter_news(self, title):
        try:
            sql = "insert into filter_news VALUES (NULL, '%s')" % (title)
            # sql = "insert into %s VALUES (NULL ,'%s' ,'%s' ,'%s','%s',NULL, NULL, 0)" % (table, start_time, endtime, title, url)
            print sql
            self.cursor.execute(sql)  # 执行语句
            self.conn.commit()
        except Exception as e:
            print e.message
            print '执行错误，数据回滚'
            self.conn.rollback()

    def select_filter_news(self, title):
        sql = "select title from filter_news where title='%s'" % (title)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data


    def select_fitler_hot_num(self):
        sql = "select id,hot_num from filter_news"
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        # for i in data:
        return data




    def insert_news(self, start_time, url_title, url):
        try:
            sql = "insert into news VALUES (NULL,'%s',NULL,'%s',NULL,'%s',NULL,NULL,0,NULL,NULL )" % (start_time, url_title, url)
            # sql = "insert into %s VALUES (NULL ,'%s' ,'%s' ,'%s','%s',NULL, NULL, 0)" % (table, start_time, endtime, title, url)
            print sql
            self.cursor.execute(sql)  # 执行语句
            self.conn.commit()
        except Exception as e:
            print e.message
            print '执行错误，数据回滚'
            self.conn.rollback()


    def select_news(self, url_title):
        sql = "select url_title from news where url_title='%s'" %(url_title)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def select_news_info(self, value):
        lists = []
        # print value
        sql = "select %s from news where tag != 1"%(value)
        # print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            # print i
            lists.append(i[0])
        return lists


    def select_news_title(self):
        sql = "select url,title,url_title from news where tag != 1"
        # print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            if i[1] is None: #正文为空
                self.update_news_title(url=i[0], title=i[2])


    def update_news_title(self, title, url):
        try:
            sql = "update news set title='%s' WHERE url='%s'" % (title, url)
            print sql
            self.cursor.execute(sql)  # 执行语句
            self.conn.commit()
        except Exception as e:
            print e.message
            print '执行错误，数据回滚'
            self.conn.rollback()


    def select_content(self):
        list_url = []
        sql = "select url,contents from news where tag != 1"
        # print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            if i[1] is None: #正文为空
                # print i[1]
                list_url.append(i[0])
        return list_url


    def delete_content(self, url):
        try:
            sql = "delete from news where url='%s'" % (url)
            print sql
            self.cursor.execute(sql)  # 执行语句
            self.conn.commit()
        except Exception as e:
            print e.message
            print '执行错误，数据回滚'
            self.conn.rollback()


    def delete_title(self, table):
        sql = "select id,title from %s where tag!=1"%(table)
        # print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            print '*************************'
            print i[1]
            if i[1] is None:  # title为空
                try:
                    sql = "delete from %s where id='%s'" % (table, i[0])
                    print sql
                    self.cursor.execute(sql)  # 执行语句
                    self.conn.commit()
                except Exception as e:
                    print e.message
                    print '执行错误，数据回滚'
                    self.conn.rollback()


    def update_news_content(self, content, url):
        try:
            sql = "update news set contents='%s' WHERE url='%s'" % (content, url)
            print sql
            print '更新正文'
            self.cursor.execute(sql)  # 执行语句
            self.conn.commit()
        except Exception as e:
            print e.message
            print '执行错误，数据回滚'
            self.conn.rollback()


    def get_news_content(self):
        urls = self.select_content()
        for i in urls:
            try:
                article = Article(i, language='zh')
                article.download()
                article.parse()
                # content = article.text.replace('\n', '').strip()
                content = article.text.replace('\n', '').strip().split('。')
                #print content   # [u'']
                if (len(content) == 1):
                    self.delete_content(url=i)
                    # content = '找不到'
                else:
                    if len(content) > 5:
                        c = content[0:5]
                        txt = '。'.join(c)
                    else:
                        c = content
                        txt = '。'.join(c)
                        print txt
                    self.update_news_content(content=txt, url=i)
            except Exception as e:
                print e.message



    def update_part_news(self, start_time, title, place, url_title):
        # try:
            sql = "update news set start_time='%s',title='%s',place='%s' WHERE url_title='%s'" % (start_time, title, place, url_title)
            print sql
            self.cursor.execute(sql)  # 执行语句
            self.conn.commit()
        # except Exception as e:
        #     print e.message
        #     print '执行错误，数据回滚'
        #     self.conn.rollback()

    def update_news_notime(self, title, place, url_title):
        # try:
            sql = "update news set title='%s',place='%s' WHERE url_title='%s'" % (title, place, url_title)
            print sql
            self.cursor.execute(sql)  # 执行语句
            self.conn.commit()
        # except Exception as e:
        #     print e.message
        #     print '执行错误，数据回滚'
        #     self.conn.rollback()

            # 查询大麦网体育赛事表

    def select_news_time(self):
        sql = 'select start_time,url,endtime from news WHERE tag!=1'
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for i in data:
            # print i[0]
            if i[2] is None:
                # times = self.get_news_time(times=i[0])
                times = i[0]
                print times
                print type(times)
                start_times = times
                endtimes = times

                # print "开始日期：" + start_times
                # print "结束日期：" + endtimes
                if not times is None:
                    self.update_news_endtime(start_time=start_times, endtime=endtimes, url=i[1])
                print '---------------------------'
                # else:
                #     print "已更新"

        # 获取时间

    def get_news_time(self,times):
        s = '/'
        # print str in urls
        if s in times:
            print '///////////'
            print times
            return times
        else:
            now = datetime.datetime.now()
            # delta = datetime.timedelta(days=1)
            list_time = ['今日', '年', '月', '日']
            if list_time[0] in times:  #今日
                # n_days = now - delta
                print '今日'
                n_days = now
                times = datetime.datetime.strftime(n_days, '%Y/%m/%d')
                print times
                return times
            else:
               pass

    # 更新大麦网体育赛事表(通过链接修改表)
    def update_news_endtime(self,start_time, endtime, url):
        # 更新数据
        try:
            sql = "update news set start_time='%s' , endtime='%s' WHERE url='%s'" % (start_time, endtime, url)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e.message
            print "更新失败"


    # (start_time, title, url, place, contents)
    # def select_part_news(self, table, start_time, titles, place):
    #     sql = 'select start_time, from %s where id=1' % (table)
    #     print sql
    #     self.cursor.execute(sql)
    #     data = self.cursor.fetchall()
    #     for i in data:
    #         print i[0]
    #         if (i[0] == 1):
    #             try:
    #                 sql = "update %s set start_time='%s',title='%s',place='%s' WHERE id=1" % (
    #                 table, start_time, title, place)
    #                 print sql
    #                 self.cursor.execute(sql)  # 执行语句
    #                 self.conn.commit()
    #             except Exception as e:
    #                 print e.message
    #                 print '执行错误，数据回滚'
    #                 self.conn.rollback()

    # 往展会插入数据
    def insert_eshow(self, table, start_time, endtime, title, url, place, hangye, hold_num, hold_cycle, zhanguan,
                     zhuban):
        try:
            sql = "insert into %s VALUES (NULL ,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',0)" % (
                table, start_time, endtime, title, url, place, hangye,
                hold_num, hold_cycle, zhanguan, zhuban)
            print sql
            self.cursor.execute(sql)  # 执行语句
            self.conn.commit()
        except Exception as e:
            print '执行错误，数据回滚'
            self.conn.rollback()

    # 往体育表插入数据
    def insert_sport(self, table, start_time, title, url, changuan):
        try:
            sql = "insert into %s VALUES (NULL ,'%s','%s','%s','%s' , NULL ,0)" % (
                table, start_time, title, url, changuan)
            print sql
            self.cursor.execute(sql)  # 执行语句
            self.conn.commit()
        except Exception as e:
            print '执行错误，数据回滚'
            self.conn.rollback()

    # 往天气表中插入数据的方法
    def insert0(self, table, start_time, url, title):
        try:
            sql = "insert into %s VALUES (NULL ,'%s','%s','%s',NULL,0)" % (table, start_time, url, title)
            print sql
            self.cursor.execute(sql)  # 执行语句
            self.conn.commit()
        except Exception as e:
            print '执行错误，数据回滚'
            self.conn.rollback()

    # 往演唱会表插入数据
    def insert(self, table, title, start_time, changuan, url, page_link):
        try:
            sql = "insert into %s VALUES (NULL ,'%s','%s','%s','%s','%s',NULL,0)" % (
                table, title, start_time, changuan, url, page_link)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print '执行错误，数据回滚'
            self.conn.rollback()

    # 查询新浪新闻表
    # def select_news(self, table):
    #     sql = 'select start_time,url from %s' % (table)
    #     print sql
    #     self.cursor.execute(sql)
    #     data = self.cursor.fetchall()
    #     for i in data:
    #         # print i[0]
    #         if (i[0] == 'null'):
    #             times = self.get_time(i[1])
    #             self.update_time(table='news', time=times, url=i[1])

    # 查询天气表
    def select0(self, table):
        sql = 'select url,content from %s' % (table)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            if (i[1] == 'null'):
                content = self.get_content(i[0])
                self.update(table='weather', content=content, url=i[0])

    # 查询表
    def select(self, table, title):
        sql = "select title from %s where title='%s'" % (table, title)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        # print data
        return data

    def select_new(self, table, title):
        # str="召开"
        sql = "select title from %s where '%s' LIKE '%%召开%%会议%%' or '%s' LIKE '%%会议%%召开%%' or '%s' LIKE '%%举行%%会议%%' or '%s' LIKE '%%会议%%举行%%' or '%s' LIKE '%%峰会%%'"%(table, title, title, title, title, title)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        # print data
        # for i in data:
        #     print i

        return data

    # 修改标记位
    def update_tag(self, table):
        try:
            sql = "select tag,url from %s where tag !=1" % (table)
            print sql
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            for i in data:
                if (i[0] != 1):
                    sql = "update %s set tag=1 WHERE url='%s'" % (table, i[1])
                    print sql
                    self.cursor.execute(sql)
                    self.conn.commit()
        except Exception as e:
            print e.message
            print "更新失败"

    def select_news_url(self, table, url):
        sql = "select url from %s where url='%s'" % (table, url)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    # 查询天气表
    def select2(self, table, url):
        sql = "select url from %s where url='%s'" % (table, url)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    # 获取时间
    def get_time(self, i):
        res = requests.get(i)
        res.encoding = 'utf-8'
        bs = BeautifulSoup(res.text, 'html.parser')
        try:
            timesource = bs.select('.time-source')[0].contents[0].strip()
            times = datetime.strptime(timesource, '%Y年%m月%d日%H:%M')
        except Exception as e:
            print e.message
            times = '未知'
        return times

    # 获取天气正文
    def get_content(self, i):
        driver = webdriver.PhantomJS()
        driver.get(i)
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            content = bs.find('dd', id='alarmcontent').string
        except Exception as e:
            print 'not found'
            content = 'not found'
        return content

    # 更新天气表
    def update(self, table, url, content):
        # 更新数据
        try:
            sql = "update %s set content='%s' WHERE url='%s'" % (table, content, url)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e.message
            print "更新失败"

    # 更新新闻表
    def update_time(self, table, start_time, url):
        # 更新数据
        try:
            sql = "update %s set start_time='%s' WHERE url='%s'" % (table, start_time, url)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e.message
            print "更新失败"

    # 从数据库读内容生成csv
    def to_csv(self, table):
        import pandas as pd
        print '-------------------'
        times = []
        urls = []
        titles = []
        places = []
        sql = 'select title,start_time,place,url from %s ORDER by id desc limit 10' % (table)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            titles.append(i[0])
            times.append(i[1])
            places.append(i[2])
            urls.append(i[3])
        dict = {u'时间': times, u'链接': urls, u'标题': titles, u'地点': places}
        return dict

    # 生成演唱会表的csv
    def to_sing_csv(self, table):
        start_times = []  # 开始时间
        titles = []  # 标题
        urls = []  # 链接
        changuans = []  # 地点评论
        endtimes = []  # 结束时间
        pagelinks = []  # 网页
        tags = []
        sql = 'select start_time,title,url,page_link,changuan,endtime,tag from %s where tag !=1  ORDER by id desc limit 10' % (table)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            start_times.append(i[0])
            titles.append(i[1])
            urls.append(i[2])
            pagelinks.append(i[3])
            changuans.append(i[4])
            endtimes.append(i[5])
            tags.append(i[6])
        dict = {u'开始日期': start_times, u'标题': titles, u'链接': urls, u'网页链接': pagelinks, u'场馆': changuans,
                u'结束日期': endtimes, u'标记': tags}
        return dict

    # 生成新闻表的csv
    def to_news_csv(self, table):
        start_times = []
        endtimes = []
        title = []
        urls = []
        places = []
        contents = []
        tags = []
        # hot_nums = []
        sql = 'select start_time,endtime,title,url,contents,tag,place from %s ORDER by id desc limit 5' % (table)
        # sql = 'select start_time,endtime,title,url,contents,tag,place from %s where sel =5' % (table)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            start_times.append(i[0])
            endtimes.append(i[1])
            title.append(i[2])
            urls.append(i[3])
            contents.append(i[4])
            tags.append(i[5])
            places.append(i[6])
            # hot_nums.append(i[6])
        dict = {u'开始日期': start_times, u'结束日期': endtimes, u'标题': title, u'链接': urls,u'正文':contents, u'标记': tags, u'地点':places}
        return dict

    # 生成展会表的csv
    def to_eshow_csv(self, table):
        start_times = []
        endtimes = []
        titles = []
        urls = []
        places = []
        hold_num = []
        hold_cycle = []
        zhanguans = []
        zhubans = []
        tags = []
        sql = 'select start_time,endtime,title,url,place,hold_num,hold_cycle,zhanguan,zhuban,tag from %s where tag !=1 ORDER by id desc limit 5' % (
        table)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            start_times.append(i[0])
            endtimes.append(i[1])
            titles.append(i[2])
            urls.append(i[3])
            places.append(i[4])
            hold_num.append(i[5])
            hold_cycle.append(i[6])
            zhanguans.append(i[7])
            zhubans.append(i[8])
            tags.append(i[9])
        dict = {u'开始日期': start_times, u'结束日期': endtimes, u'标题': titles, u'链接': urls, u'地点': places, u'届数': hold_num,
                u'举办周期': hold_cycle, u'展馆': zhanguans, u'主办方': zhubans, u'标记': tags}
        return dict

    # 生成天气表的csv
    def to_weather_csv(self, table):
        start_times = []
        titles = []
        endtimes = []
        urls = []
        tags = []
        sql = 'select start_time,title, url,endtime,tag from %s where tag !=1 ORDER by id desc limit 50' % (table)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            sql = ''
            start_times.append(i[0])
            titles.append(i[1])
            urls.append(i[2])
            endtimes.append(i[3])
            tags.append(i[4])
        dict = {u'开始日期': start_times, u'标题': titles, u'链接': urls, u'结束日期': endtimes, u'标记': tags}
        return dict

    # 生成体育表的csv
    def to_sport_csv(self, table):
        start_times = []
        titles = []
        urls = []
        changuans = []
        endtimes = []
        tags = []
        sql = 'select start_time,title, url,changuan,endtime,tag from %s where tag !=1 ORDER by id desc limit 10' % (table)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            start_times.append(i[0])
            titles.append(i[1])
            urls.append(i[2])
            changuans.append(i[3])
            endtimes.append(i[4])
            tags.append(i[5])
        dict = {u'开始日期': start_times, u'标题': titles, u'链接': urls, u'场馆': changuans, u'结束日期': endtimes, u'标记': tags}
        # print dict
        return dict


        # 查询展会表

    def select_eshow(self, table):
        sql = 'select place,url from %s' % (table)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            # print i[0]
            place = self.get_place(i[0])
            self.update_place(table='eshow', place=place, url=i[1])

    # 获取时间
    def get_place(self, i):
        place = i.split('|')[1]
        return place

    # 更新展会表表(通过链接修改表)
    def update_place(self, table, place, url):
        # 更新数据
        try:
            sql = "update %s set place='%s' WHERE url='%s' " % (table, place, url)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e.message
            print "更新失败"

    # 查询大麦网体育赛事表
    def select_sport_or_sing(self, table):
        sql = 'select start_time,url,endtime from %s WHERE tag!=1' % (table)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for i in data:
            # print i[0]
            if i[2] is None:
                times = self.get_sport_or_sing_time(times=i[0], urls=i[1])
                print times
                print type(times)
                num = len(times)
                print num
                if num == 1:
                    start_times = times[0]
                    endtimes = times[0]
                elif num == 2:
                    if isinstance(times, unicode):
                        start_times = times
                        endtimes = times
                    else:
                        start_times = times[0]
                        endtimes = times[1]
                else:
                    start_times = times
                    endtimes = times

                print "开始日期：" + start_times
                print "结束日期：" + endtimes

                self.update_sport_or_sing_time(table=table, start_time=start_times, endtime=endtimes, url=i[1])
                print '---------------------------'
            # else:
            #     print "已更新"

    # 获取时间
    def get_sport_or_sing_time(self, urls, times):
        str = 'damai.cn'
        str1 = "-"
        str2 = "."
        # print str in urls
        if str in urls:
            if str1 in times and str2 in times:
                times = times.replace('.', '/').split('-')
            elif str1 in times:
                times = times.replace('-', '/').split()[0]
            elif str2 in times:
                times = times.replace('.', '/').split()[0]
        else:
            times = times.replace('-', '/').split('~')
        return times

    # 更新大麦网体育赛事表(通过链接修改表)
    def update_sport_or_sing_time(self, table, start_time, endtime, url):
        # 更新数据
        try:
            sql = "update %s set start_time='%s' , endtime='%s' WHERE url='%s'" % (table, start_time, endtime, url)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e.message
            print "更新失败"

    # 查询新闻表
    def select_news_or_weather_time(self, table):
        sql = 'select start_time,url,endtime from %s WHERE tag!=1' % (table)
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for i in data:
            # print i[0]
            if i[2] is None:
                times = self.get_news_or_weather_time(times=i[0])
                print times
                start_times = times
                endtimes = times
                print "开始日期：" + start_times
                print "结束日期：" + endtimes
                print '---------------------------'

                self.update_news_or_weather_time(table=table, start_time=start_times, endtime=endtimes, url=i[1])
            # else:
            #     print "已更新"

    # 获取时间
    def get_news_or_weather_time(self, times):
        # print times
        times = times.replace('-', '/').split()[0]
        return times

    # 更新新闻表时间(通过链接修改表)
    def update_news_or_weather_time(self, table, start_time, endtime, url):
        # 更新数据
        try:
            sql = "update %s set start_time='%s' , endtime='%s' WHERE url='%s'" % (table, start_time, endtime, url)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e.message
            print "更新失败"

    # 在数据库中查询关键字
    def selectkeywords(self, keyword):
        sql = "select * from words  WHERE keyword ='%s'" % keyword
        # print sql
        try:
            self.cursor.execute(sql)

            data = self.cursor.fetchall()
            if (len(data) > 0):
                for i in data:
                    # delta = self.curtime - i[2]
                    # 检查时间间隔
                    # if delta.days > 7:
                    #     return 0 #指数值超过7天不生效
                    # else:
                    print '找到指数',i[3]
                    return i[3]  # 指数
            else:
                print '找不到 %s 的指数' % keyword
                return 0

        #返回0，表明该指数值找不到
        except Exception as e:
            print e.message
            self.conn.rollback()
        self.conn.commit()


    # 将关键字的指数存入到数据库
    def insertkeywords(self, keyword, index):
        try:
            sql = "insert into words VALUES (NULL ,'%s','%s' ,'%s')" % (keyword, self.curtime, index)
            print sql
            self.cursor.execute(sql)
        except Exception as e:
            print e.message
            self.conn.rollback()
        self.conn.commit()

    def updatehotwords(self, hot_word, time):
        try:
            sql = "update hotwords set time='%s' WHERE hot_word ='%s'" % (time, hot_word)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e.message
            self.conn.rollback()


    # 在数据库中查询关键字
    def selecthotwords(self, hot_word):
        sql = "select * from hotwords  WHERE hot_word ='%s'" % hot_word
        # print sql
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            print len(data)
            if (len(data) > 0):
                for i in data:
                    # delta = self.curtime - i[2]
                    # 检查时间间隔
                    # if delta.days > 7:
                    #     return -1  # 指数值超过7天不生效
                    # else:
                    print '找到指数', i[3]
                    return i[3]  # 指数
            else:
                print '找不到 %s 的指数' % hot_word
                return -1
        # 返回0，表明该指数值找不到
        except Exception as e:
            print e.message
            self.conn.rollback()
        self.conn.commit()

    # 返回-2时更新热度
    def updatehot_num(self, hot_word, hot_num):
        try:
            sql = "update hotwords set hot_num='%s' WHERE hot_word='%s'" % (hot_word, hot_num)
            print sql
            self.cursor.execute(sql)
        except Exception as e:
            print e.message
            self.conn.rollback()
        self.conn.commit()

    # 将关键字的指数存入到数据库
    def inserthotwords(self, hot_word, hot_num):
        try:
            sql = "insert into hotwords VALUES (NULL ,'%s','%s' ,'%f')" % (hot_word, self.curtime, hot_num)
            print sql
            self.cursor.execute(sql)
        except Exception as e:
            print e.message
            self.conn.rollback()
        self.conn.commit()

    def to_db(self, types):
        name = ['sing', 'eshow', 'news', 'sport', 'weather']
        x = name.index(types) #获得types的name（list）下标
        # for x in range(len(name)):
        print "开始把" + types + "的数据存入数据库"
        df = pd.read_csv(r"C:\untitled2\softbei\analyse_data\common\merge_" + types + "_csv.csv")
        try:
            city = list(df['地点'])
            end_time = list(df['开始日期'])
            start_time = list(df['开始日期'])
            title = list(df['标题'])
            history = list(df['事件历史悠久程度'])
            rate = list(df['事件一年内频率'])
            hot = list(df['事件热度'])
        except Exception as e:
            print "异常"
            print e.message

        for i in range(len(title)):
            try:
                # 插入之前对数据库进行了查询，确保重复数据不会被再次插入
                sql = "select event from data WHERE event ='%s'" % (title[i])
                self.cursor.execute(sql)
                data = self.cursor.fetchall()
                # print data
                if (len(data) == 0):
                    sql = "insert into data (event,start_time,end_time,bs,city,history,rate,hot)VALUES ('%s','%s','%s',%d,'%s','%s','%s','%d')" % (
                        title[i], start_time[i], end_time[i], x, city[i], history[i], rate[i], hot[i])

                print sql
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print "异常"
                print e.args
                self.conn.rollback()

                    # 更新数据库，插入经纬度

    def updata_db(self):
        sql = "select city from data  WHERE lng is null group by city"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            city = i[0]
            url = "http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=t3vn5Rb35MhGsqv1recs9Qojbwz7Kiqb&callback=showLocation" % city
            # 更新之前先对表检查，确保经纬为为空的行才被更改
            location = self.getlal(url)
            print location
            try:
                sql = "update data set lng='%s',lat='%s' where city='%s'and lng is null" % (
                    location[1], location[0], city)
                print sql
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print e.args
                self.conn.rollback()


    def getlal(self, lal):
        try:
            time.sleep(0.02)
            res = requests.get(url=lal)
            # {"status":0,"result":{"location":{"lng":114.0259736573215,"lat":22.546053546205248},"precise":0,"confidence":14,"level":"城市"}}
            json_data = res.text
            value_lal = re.findall(r'\([\s\S]*\)', json_data)[0][1:-1]
            jd = json.loads(value_lal)
            # 得到纬度
            lat = jd['result']['location']['lat']
            # print lat
            # 得到纬度
            lng = jd['result']['location']['lng']
            # print lng
            return [lat, lng]
        except Exception as e:
            print e.args
            print '网络错误'

# c = DB()
# c.delete_title(table='news')
# c.selecthotwords('2018')
# c.select_news(table='news')
# 更新地点
# c.select_eshow(table='eshow')
# 更新时间(演唱会和运动)
# c.select_damai_sport(table='sing')
# c.select_damai_sport(table='sport')
# 更新新闻网时间
# c.select_news_time(table='weather')
