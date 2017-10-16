#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pandas as pd
import json
from selenium import webdriver
import time
import re
import sys

from Softbei.common.class_database import DB

reload(sys)
sys.setdefaultencoding('utf8')


class GetCitys(DB):
    def getlal(self, lal):
        try:
            time.sleep(0.02)
            res = requests.get(url=lal)
            #{"status":0,"result":{"location":{"lng":114.0259736573215,"lat":22.546053546205248},"precise":0,"confidence":14,"level":"城市"}}
            json_data=res.text
            value_lal=re.findall(r'\([\s\S]*\)',json_data )[0][1:-1]
            jd = json.loads(value_lal)
            #得到经度
            lat=jd['result']['location']['lat']
            print '经度'
            print lat
            #得到纬度
            lng=jd['result']['location']['lng']
            print '纬度'
            print lng

            time.sleep(0.02)
            # 根据经度和纬度返回json数据(包含城市名)
            str = 'http://api.map.baidu.com/geocoder/v2/?callback=renderReverse' \
                  '&location=%s,%s' \
                  '&output=json&ak=t3vn5Rb35MhGsqv1recs9Qojbwz7Kiqb' % (lat, lng)
            res = requests.get(str)
            json_data = res.text
            #得到城市名
            value_city = re.findall(r'\([\s\S]*\)', json_data)[0][1:-1]
            jd = json.loads(value_city)
            city = jd['result']['addressComponent']['city']

        except Exception as e:
            # print e.message
            return '未知'
        return city


    def to_place(self):
        # 请求经纬度
        sql = "select city from data order by id desc limit 50"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for i in data:
            address = i[0]
            lal = 'http://api.map.baidu.com/geocoder/v2/?' \
              'address=%s&output=json&ak=t3vn5Rb35MhGsqv1recs9Qojbwz7Kiqb&callback=showLocation' % (address)
            # 返回json（包含经纬度）
            city = self.getlal(lal)
            print '城市名：' + city
            sql2 = "update data set city = '%s' WHERE city ='%s'"%(city,i[0])
            print sql2
            #更新数据库
            self.cursor.execute(sql2)
            self.conn.commit()



#函数调用
if __name__ == '__main__':
    GetCitys().to_place()

