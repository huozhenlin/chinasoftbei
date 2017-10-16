#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

from Softbei.common.class_database import *


class MergeCsv:

    def merge_ehsow_csv(self):
        c = DB()

        try:
            df1=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/eshow/eshow_age.csv')
            df2=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/eshow/eshow_hot.csv')
            df3=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/eshow/show_history.csv')
            df4=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/eshow/eshow_other.csv')
            df5=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/eshow/show_year_times.csv')
            df6=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/eshow/show_zhuban.csv')

            result = pd.concat([df1, df2,df3,df4,df5,df6], axis=1)
            pd.DataFrame(result).to_csv('C:/untitled2/Softbei/analyse_data/common/merge_eshow_csv.csv',
                                        encoding='utf8', index=None ,mode='a', header=None)

            #添加标记位
            c.update_tag(table='eshow')

        except Exception as e:
            print e.message
            print '文件不存在'

    def merge_news_csv(self):
        c = DB()

        try:
            df1=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/news/news_age.csv')
            df2 = pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/news/news_hot.csv')
            df3=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/news/news_other.csv')

            result = pd.concat([df1, df2, df3], axis=1)
            # result = pd.concat([df3], axis=1)
            pd.DataFrame(result).to_csv('C:/untitled2/Softbei/analyse_data/common/merge_news_csv.csv', encoding='utf8', index=None ,mode='a', header=None)
            # 添加标记位
            c.update_tag(table='news')

        except Exception as e:
            print e.message
            print '文件不存在'

    def merge_sing_csv(self):
        c = DB()

        try:
            df1 = pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/sing/sing_age.csv')
            df2 = pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/sing/sing_hot.csv')
            df3 = pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/sing/sing_other.csv')
            df4 = pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/sing/sing_place.csv')

            result = pd.concat([df1, df2, df3, df4],axis=1)
            pd.DataFrame(result).to_csv('C:/untitled2/Softbei/analyse_data/common/merge_sing_csv.csv', encoding='utf8', index=None,mode='a', header=None)

            # 添加标记位
            c.update_tag(table='sing')

        except Exception as e:
            print e.message
            print '文件不存在'

    def merge_sport_csv(self):
        c = DB()

        try:
            df1=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/sport/sport_age.csv')
            df2=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/sport/sport_hot.csv')
            df3=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/sport/sport_other.csv')
            df4 = pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/sport/sport_place.csv')

            result = pd.concat([df1, df2 ,df3 ,df4], axis=1)
            pd.DataFrame(result).to_csv('C:/untitled2/Softbei/analyse_data/common/merge_sport_csv.csv', encoding='utf8', index=None,mode='a', header=None)

            c.update_tag(table='sport')

        except Exception as e:
            print e.message
            print '文件不存在'


    def merge_weather_csv(self):
        c = DB()

        try:
            df1=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/weather/weather_other.csv')
            df2=pd.read_csv(r'C:/untitled2/Softbei/analyse_data/common/csv/weather/weather_warining_level.csv')

            result = pd.concat([df1, df2], axis=1)
            pd.DataFrame(result).to_csv('C:/untitled2/Softbei/analyse_data/common/merge_weather_csv.csv', encoding='utf8', index=None ,mode='a', header=None)

            # 添加标记位
            c.update_tag(table='weather')

        except Exception as e:
            print e.message
            print '文件不存在'

    def main_merge_csv(self, types):
        # list = ['eshow','news', 'sing', 'sport', 'weather']
        # list = ['news']
        # for s in list:
        if types == 'eshow':
            self.merge_ehsow_csv()
        elif types == 'news':
            self.merge_news_csv()
        elif types == 'sing':
            self.merge_sing_csv()
        elif types == 'sport':
            self.merge_sport_csv()
        elif types == 'weather':
            self.merge_weather_csv()

if __name__ =='__main__':
    MergeCsv().main_merge_csv(types='sing')
