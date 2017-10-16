#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd
from Softbei.common.class_switch_method import *
reload(sys)
sys.setdefaultencoding('utf8')

class History:
    def get_num(self, num):
        for case in switch(num):
            if case('一'):
                num='1'
                break
            if case('两'):
                num='2'
                break
            if case('三'):
                num='3'
                break
            if case('四'):
                num='4'
                break
            if case():
                # print 'h'
                num='1'
        return num

    def get_value(self, types):
        lists=[]
        # df = pd.read_csv('../../csv/eshow.csv')C:\untitled2\Softbei\removal_csv\csv\eshow.csv
        csv_name = r'C:/untitled2/Softbei/removal_csv/csv/%s.csv' % (types)
        df = pd.read_csv(csv_name)
        hold_num = list(df['届数'])
        hold_cycle = list(df['举办周期'])
        tag = df['标记']
        # print hold_num
        # print hold_cycle

        # index为下标，j为标记数
        for index, j in enumerate(tag):
            if (j == 1):
                continue
            else:
                hold_num_nonrep = hold_num[index]
                # print hold_num_non_repeat , index
                if (hold_num_nonrep != 'null'):
                    # 变量Z
                    hold_nums = hold_num_nonrep.replace('届', '')
                else:
                    hold_nums = '1'
                lists.append(hold_nums)

                hold_cycle_nonrep = hold_cycle[index]
                hold_cycles = hold_cycle_nonrep.decode('utf8')
                x=hold_cycle_nonrep.split('年')[0]

                if(hold_cycles!='null'):
                    # 变量X
                    total_times=self.get_num(x)
                    # print total_times
                else:
                    total_times='1'
                lists.append(total_times)


                hold_cycles = hold_cycle_nonrep.decode('utf8')
                print hold_cycle_nonrep
                y = x.split('届')[0]
                # print '-------yyyy----------'
                # print y

                if (hold_cycles != 'null'):
                    # 变量Y
                    appear_times = self.get_num(y)
                    print appear_times
                else:
                    appear_times = '1'
                lists.append(appear_times)
        #返回要计算的值['11', '1', '1']
        print lists
        return lists


    def judge(self, result):
        if (result<= 5):
            history_level=1
        elif (5<result<10):
            history_level=2
        elif (result>= 10):
            history_level=3
        # print history_level
        return history_level
        # print show_level


    def get_history(self, types):
        history=[]
        # def history():
        #返回要计算的值,例一年一届，11届,它是一个list[11,1,1]
        history_list=self.get_value(types)
        print list
        # list_level = []
        num=len(history_list)  #30
        s = int(num / 3) #10
        i = 0
        while(True):  #i  0-9
            if(i < num):
                # print i
                result = int(history_list[i]) * int(history_list[i + 1]) / int(history_list[i + 2])
                # result=int(list[i])*int(list[i+s])/int(list[i+s+s])  #0   10   20    11   1   2
                print '举办的年数'
                print result
                #判断等级
                level=self.judge(result)
                print '历史悠久程度的等级'
                print level
                print '---------------------------'
                history.append(level)
                i = i + 3
            else:
                break
        #返回list
        return history



    def to_csv(self, types):
        history=self.get_history(types)
        if (len(history) == 0):
            return 'null'

        dict = {

            u'事件历史悠久程度': history

            }
        return dict

    def main_history(self, types):
        # file_name='common/csv/eshow/show_history.csv'
        file_name='C:/untitled2/Softbei/analyse_data/common/csv/eshow/show_history.csv'
        print file_name
        dict = self.to_csv(types)
        print dict
        if(dict=='null'):
            print '没有可生成的数据'
        else:
            pd.DataFrame(dict).to_csv(file_name, encoding='utf8', index=None)
        print '-------------------------------*********************-------------------------------------'

if __name__ == '__main__':
    # value=History().get_history()
    # print value
    # History().get_value()
    History().main_history(types='eshow')



