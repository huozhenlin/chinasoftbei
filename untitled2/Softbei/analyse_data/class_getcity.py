#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pandas as pd
import json
from selenium import webdriver
import time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class GetCity:
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


    def to_place_csv(self, csv_name):

        df=pd.read_csv(csv_name)
        places=[]
        # changuan_key='场馆'.decode('utf8')
        # print changuan_key
        changuan = list(df['场馆'])
        tag = df['标记']
        # index为下标，j为标记数
        for index, j in enumerate(tag):
            if (j == 1):
                continue
            else:
                changuan_non_repeat = changuan[index]
                print changuan_non_repeat, index
                if(changuan_non_repeat == 'null'):
                    city='null'
                    places.append(city)
                else:
                    # 请求经纬度
                    lal = 'http://api.map.baidu.com/geocoder/v2/?' \
                          'address=%s&output=json&ak=t3vn5Rb35MhGsqv1recs9Qojbwz7Kiqb&callback=showLocation' % (changuan_non_repeat)
                    # 返回json（包含经纬度）
                    city = self.getlal(lal)
                    print '城市名：' + city
                    places.append(city)
                    print '------------------------------'

        if (len(places) == 0):
            return 'null'
        dict = {

            u'地点': places
            # places
        }

        return dict


    def main_void(self, value):
        # csv_name='../../csv/%s.csv'%(value)
        csv_name = 'C:/untitled2/Softbei/removal_csv/csv/%s.csv' % (value)
        # print csv_name
        # file_name = '../common/csv/%s/%s_place.csv' % (value,value)
        file_name = 'C:/untitled2/Softbei/analyse_data/common/csv/%s/%s_place.csv' % (value, value)
        print file_name
        dict=self.to_place_csv(csv_name)
        print dict
        if (dict == 'null'):
            print '没有可生成的数据'
        else:
            pd.DataFrame(dict).to_csv(file_name, encoding='utf8', index=None)
        print '--------------------------********************----------------------------------'


    def main_place(self, types):
        self.main_void(types)
        # list=['sing']
        # list = ['sing', 'sport']
        # for s in list:
        #     self.main_void(s)


#函数调用
if __name__ == '__main__':
    GetCity().main_place(types='sing')

