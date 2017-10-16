#!/usr/bin/env python
# -*- coding: utf-8 -*-
from simhash import Simhash
import sys
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf-8')



class Removal:
    '''
    去重算法思路：
    第一步：使用drop_duplicates()方法去掉dataframe中完全相同的标题
    第二步：使用递归算法，层层循环遍历样本
    第二步：使用simhash的distance()方法获取两个样本之间的海明距离，根据经验，海明距离在0-3之间的
            算重复事件
    '''

    # 封装去重算法，方法传入一个csv文件名，列名(单个),生成后的文件名
    def drop_repet(self, csv_name, colunm, update_name):
        b = 0  # 起点

        # drop_duplicates()方法可用于快速去除相同的重复数据，python自带
        df = pd.read_csv(csv_name).drop_duplicates([colunm])

        # 将需要去重的列提取出来转换成list

        title = list(df[colunm])
        hash_title = []
        for ii in title:
            hash_title.append(Simhash(ii))

        # 两个list转成dict
        d = {}
        xx = []
        for i in range(len(title)):
            d[title[i]] = hash_title[i]

        # 递归算法,i为字典键
        for i in d:
            b = int(b) + 1
            for k in title[b:]:
                # 判断海明距离
                ss = d[i].distance(d[k])

                if 0 < ss <= 3:
                    xx.append(k)

                    print '找到重复事件:' + k

        title = []
        for x in set(xx):
            d.pop(x)
        for a in d:
            title.append(a)
        # 判断是否存在
        df = df[df[colunm].isin(title)]
        return df

    def main_void(self, value):
        # before_csv_name = '../before_csv/before_%s.csv' % (value)
        # csv_name = '../csv/%s.csv' % (value)
        before_csv_name = 'C:/untitled2/Softbei/to_csv/before_csv/before_%s.csv' % (value)
        csv_name = 'C:/untitled2/Softbei/removal_csv/csv/%s.csv' % (value)
        dict = self.drop_repet(before_csv_name, '标题', csv_name)
        pd.DataFrame(dict).to_csv(csv_name, encoding='utf8', index=None)
        print 'csv保存成功，路径：%s' % (csv_name)
        print '-------------**************----------------'

    #将去重后的数据保存到指定文件中
    # pd.DataFrame(df).to_csv(update_name,encoding='utf8',index=None)
    def main_removal(self, types):
        self.main_void(types)
        # list = ['eshow', 'sing', 'news','sport', 'weather']
        # list = ['news']
        # for s in list:
            # self.main_void(s)


# 函数调用
if __name__ == '__main__':
    Removal().main_removal(types='sing')

