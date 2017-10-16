#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from Softbei.common.class_switch_method import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class YearTimes:
    def get_num(self, num):
        for case in switch(num):
            if case('一'):
                num=1
                break
            if case('两'):
                num=2
                break
            if case('三'):
                num=3
                break
            if case('四'):
                num=4
                break
            if case():
                num=1
        return num


    def year_frequency(self, result):
        i=result.decode('utf8')
        print i
        if(i!='null'):
            try:
                total_times=self.get_num(i[0])
                appear_times=self.get_num(i[2])
                #计算一年内的事件频率
                result = int(appear_times) / int(total_times)
                print result
            except Exception as e:
                result = 1

        else:
            result = 1
            print result
        print '-----------------------------'
        return result


    def get_year_times(self, types):
        # df=pd.read_csv('../../csv/eshow.csv')
        csv_name='C:/untitled2/Softbei/removal_csv/csv/%s.csv'%(types)
        df=pd.read_csv(csv_name)
        hold_cycle=list(df['举办周期'])
        tag=df['标记']
        year_times=[]
        #index为下标，j为标记数
        for index,j in enumerate(tag):
            if(j == 1):
                continue
            else:
                hold_cycle_nonrep=hold_cycle[index]
                # print hold_cycle_nonrep,index
                result = self.year_frequency(hold_cycle_nonrep)
                # 事件一年内频率
                year_times.append(result)
        return year_times



    def to_csv(self, types):
        year_times=self.get_year_times(types)
        # year_times=
        if(len(year_times) ==0):
            return 'null'
        dict = {

            u'事件一年内频率':year_times
            # year_times
            }
        return dict


    def main_year_times(self, types):
        file_name='C:/untitled2/Softbei/analyse_data/common/csv/eshow/show_year_times.csv'
        # file_name='common/csv/eshow/show_year_times.csv'
        print file_name
        dict = self.to_csv(types)
        print dict
        if(dict == 'null'):
            print '没有可生成的数据'
        else:
            pd.DataFrame(dict).to_csv(file_name, encoding='utf8', index=None )
        print '-------------------------------*********************-------------------------------------'

if __name__ == '__main__':
    YearTimes().main_year_times(types='eshow')

