#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf8')
str = '国内'
str1 = '国内行业协会'
str2 = '国内民间协会'
str3 = '国际行业协会-------------------------------------------------------------------------------------------------------'
str4 = '国际民间协会-------------------------------------------------------------------------------------------------------'

# 国际，国内
list1 = ['中国', '中华', '省', '市', '北京', '上海', '广州', '深圳']

list_xiehui=['行业','公司','学会','商会','促进会','组委会']

list_goven=['政府','省','市']

class ZhuBan:
    def search(self, x, i):
        value=i.find(list1[x]) != -1
        # print value
        return value

    def search_xiehui(self, y, i):
        value=i.find(list_xiehui[y]) != -1
        return value

    #区分国内某某协会
    def judge_xiehui(self, i):
        num=len(list_xiehui)
        for x in range(num):#0-5
            if (self.search_xiehui(x,i)):
                judge_value = str1
                break
            else:
                judge_value = str2
        return judge_value


    #区分国际某某协会
    def judge_guoji_xiehui(self, i):
        num = len(list_xiehui)
        for x in range(num):#0-5
            if(self.search_xiehui(x,i)):
                judge_value=str3
                break
            else:
                judge_value=str4
        return judge_value


    #主办方级别
    def goven_level(self, z, i):
        value = i.find(list_goven[z]) != -1
        # print value
        return value



    def to_csv(self, csv_name):

        #主办方类型
        zhuban_level_International=[]
        zhuban_level_Country=[]
        zhuban_level_Province=[]
        zhuban_level_City=[]

        #主办方级别
        guonei_nogoven=[]
        guonei_hangye=[]
        guoji_nogoven=[]
        guoji_hangye=[]

        titles=[]
        data = ['0', '1']
        df = pd.read_csv(csv_name)
        # 取出主办方
        zhuban = list(df['主办方'])
        tag = df['标记']

        # index为下标，j为标记数
        for index,j in enumerate(tag):
            # print i
            if(j == 1):
                continue
            else:
                i = zhuban[index]
            # 主办方单位
            print i
            num = len(list1)
            if (i != 'null' and i.find('政府') < 0):  # 如果不为空且找不到了政府
                for x in range(num):
                    # print x,
                    if (self.search(x, i)):  # 判断是国内的
                        result = self.judge_xiehui(i)
                        print result
                        if (result == str1):
                            guonei_hangye.append(data[1])
                            guonei_nogoven.append(data[0])
                            guoji_hangye.append(data[0])
                            guoji_nogoven.append(data[0])
                        else:
                            guonei_nogoven.append(data[1])
                            guonei_hangye.append(data[0])
                            guoji_hangye.append(data[0])
                            guoji_nogoven.append(data[0])

                            # 出现True停止寻找
                    if (self.search(x, i) == True):
                        break

                if (self.search(x, i) == False):
                    result = self.judge_guoji_xiehui(i)
                    print result
                    if (result == str3):
                        guonei_hangye.append(data[0])
                        guonei_nogoven.append(data[0])
                        guoji_hangye.append(data[1])
                        guoji_nogoven.append(data[0])

                    else:
                        guonei_nogoven.append(data[1])
                        guonei_hangye.append(data[0])
                        guoji_hangye.append(data[0])
                        guoji_nogoven.append(data[1])
                        # break  #跳出整个大的循环
            else:
                print 'null or  goven'
                guonei_hangye.append(data[0])
                guonei_nogoven.append(data[0])
                guoji_hangye.append(data[0])
                guoji_nogoven.append(data[0])

            print '------------------------------------------'

            # 若出现政府
            if (self.goven_level(0, i)):
                # judge_goven_level(i)
                if (self.goven_level(0, i) and self.goven_level(2, i)):
                    # print '市政府'
                    zhuban_level_City.append(data[1])
                    zhuban_level_Province.append(data[0])
                    zhuban_level_Country.append(data[0])
                    zhuban_level_International.append(data[0])

                    # 包含省，政府，不包含市
                elif (self.goven_level(0, i) and self.goven_level(1, i)):
                    # print '省政府'
                    zhuban_level_City.append(data[0])
                    zhuban_level_Province.append(data[1])
                    zhuban_level_Country.append(data[0])
                    zhuban_level_International.append(data[0])

                else:
                    # print '国家政府'
                    zhuban_level_City.append(data[0])
                    zhuban_level_Province.append(data[0])
                    zhuban_level_Country.append(data[1])
                    zhuban_level_International.append(data[0])

            else:
                zhuban_level_City.append(data[0])
                zhuban_level_Province.append(data[0])
                zhuban_level_Country.append(data[0])
                zhuban_level_International.append(data[0])

        if (len(zhuban_level_International) == 0):
            return 'null'

        dict = {
            # u'标题':titles,
            u'是否是国际性组织': zhuban_level_International, u'是否是国家政府': zhuban_level_Country,
            u'是否是省政府': zhuban_level_Province, u'是否是地方级政府': zhuban_level_City,
            u'是否是国内民间协会': guonei_nogoven, u'是否是国际民间协会': guoji_nogoven, u'是否是国内行业协会': guonei_hangye,
            u'是否是国际行业协会': guoji_hangye
        }

        return dict

    # dict=to_csv("D:\PycharmProjects\untitled2\getData\softbei\csv\sing.csv")

    def main_zhuban(self, types):
        # file_name='common/csv/eshow/show_zhuban.csv'
        file_name='C:/untitled2/Softbei/analyse_data/common/csv/eshow/show_zhuban.csv'
        print file_name
        # dict=to_csv('../../csv/eshow.csv')
        csv_name = 'C:/untitled2/Softbei/removal_csv/csv/%s.csv' % (types)
        dict=self.to_csv(csv_name)
        print dict
        if(dict == 'null'):
            print '没有可生成的数据'
        else:
            # pd.DataFrame(dict).to_csv(file_name ,encoding='utf8',index=None , mode='a' ,header=None)
            pd.DataFrame(dict).to_csv(file_name, encoding='utf8', index=None)
        print '-------------------------------*********************-------------------------------------'

if __name__ == '__main__':
    ZhuBan().main_zhuban(types='eshow')