#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pandas as pd
from Softbei.common.class_database import *

class ToCsv(DB):
    #主体方法，使用switch，case函数根据不同表名生成不同的csv
    def main_void(self, table):
        if table =="weather":
            return ToCsv.to_weather_csv(self, table)
        elif table=="sing":
            return ToCsv.to_sing_csv(self, table)
        elif table=="sport":
            return ToCsv.to_sport_csv(self, table)
        elif table== "news":
            return ToCsv.to_news_csv(self, table)
        elif table=="eshow":
            return ToCsv.to_eshow_csv(self, table)


    #从数据中读取数据生成csv
    def to_csv(self, table_name):
        # if table_name == 'news':
        #     dict=self.main_void(table=table_name)
        #     filename = r'C:/untitled2/Softbei/to_csv/before_csv/before_%s.csv'%(table_name)
        #     # filename = '../before_csv/before_%s.csv'%(table_name)
        #     pd.DataFrame(dict).to_csv(filename,encoding='utf8',index=None)
        #     pd.DataFrame(dict).to_csv(r'C:/untitled2/Softbei/removal_csv/csv/%s.csv' % table_name, encoding='utf8', index=None)
        # else:
        dict = self.main_void(table=table_name)
        filename = r'C:/untitled2/Softbei/to_csv/before_csv/before_%s.csv' % (table_name)
        pd.DataFrame(dict).to_csv(filename, encoding='utf8', index=None)
        # filename = '../before_csv/before_%s.csv' % (table_name)

        print '生成csv保存在'+filename
        print 'finish'
        print '-------------**************----------------'


    def main_to_csv(self, types):
        self.to_csv(types)
        # list = ['sing', 'eshow', 'news', 'sport', 'weather']
        # list = ['news']
        # for s in list:
        #     self.to_csv(s)


if __name__ == '__main__':
   # main_to_csv()
    ToCsv().main_to_csv(types='sing')
