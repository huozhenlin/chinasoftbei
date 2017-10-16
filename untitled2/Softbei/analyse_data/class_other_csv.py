#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 展会
# noinspection PyGlobalUndefined
class OtherCsv:
    def to_eshow_csv(self, csv_name):
        titles = []

        # 时间
        start_times = []
        endtimes = []

        # 地点
        places = []

        show = []
        sing = []
        sport = []
        meeting = []
        weather = []

        # 是否有固定的参与人群
        attend = []

        # 是否影响社会群体
        business_crowd = []  # 是否影响商务人群
        public = []  # 是否影响社会大众

        # 事件历史悠久程度
        history = []

        # 事件一年内频率
        year_times = []

        data = ['0', '1']
        df = pd.read_csv(csv_name)
        title = list(df['标题'])
        place = list(df['地点'])
        start_time = list(df['开始日期'])
        endtime = list(df['结束日期'])
        tag = list(df['标记'])
        # hold_cycle = list(df['举办周期'])
        num = len(title)
        for i in range(num):
            # 标记
            if (tag[i] == 1):
                continue

            # 标题
            titles.append(title[i])
            # 时间
            start_times.append(start_time[i])
            endtimes.append(endtime[i])
            # 地点
            places.append(place[i])

            # 是否有固定的参与人群
            attend.append(data[0])

            # 影响社会群体
            business_crowd.append(data[1])  # 是否影响商务人群
            public.append(data[0])  # 是否影响社会大众

            show.append(data[1])
            sing.append(data[0])
            sport.append(data[0])
            meeting.append(data[0])
            weather.append(data[0])

        if len(titles) == 0:
            return 'null'
        dict = {
            u'标题': titles,
            u'开始日期': start_times, u'结束日期': endtimes,
            u'地点': places,
            u'是否有固定的参与人群': attend,
            u'是否影响商务人群': business_crowd, u'是否影响社会大众': public,
            u'是否展会': show, u'是否演唱会': sing, u'是否体育赛事': sport, u'是否会议': meeting, u'是否天气': weather
        }
        return dict

    # 体育赛事
    def to_sport_csv(self, csv_name):
        titles = []
        start_times = []
        endtimes = []
        # 主办方级别
        zhuban_level_International = []
        zhuban_level_Country = []
        zhuban_level_Province = []
        zhuban_level_City = []

        # 主办方类型
        guonei_nogoven = []
        guoji_nogoven = []
        guonei_hangye = []
        guoji_hangye = []

        # 主要影响的年龄阶段
        children = []
        youth = []
        adult = []
        older = []

        show = []
        sing = []
        sport = []
        meeting = []
        weather = []

        # 是否有固定的参与人群
        attend = []

        # 是否影响社会群体
        business_crowd = []  # 是否影响商务人群
        public = []  # 是否影响社会大众

        # 事件历史悠久程度
        history = []

        # 事件一年内频率
        year_times = []

        data = ['0', '1']
        df = pd.read_csv(csv_name)
        title = list(df['标题'])
        start_time = list(df['开始日期'])
        endtime = list(df['结束日期'])
        tag = list(df['标记'])
        num = len(title)

        for i in range(num):
            # 标记
            if (tag[i] == 1):
                continue

            titles.append(title[i])
            start_times.append(start_time[i])
            endtimes.append(endtime[i])

            zhuban_level_City.append(data[0])
            zhuban_level_Province.append(data[0])
            zhuban_level_Country.append(data[0])
            zhuban_level_International.append(data[0])

            guonei_nogoven.append(data[0])
            guoji_nogoven.append(data[0])
            guonei_hangye.append(data[0])
            guoji_hangye.append(data[0])

            # 主要影响的年龄阶段
            # children.append(data[0])
            # youth.append(data[0])
            # adult.append(data[0])
            # older.append(data[1])

            # 是否有固定的参与人群
            attend.append(data[0])

            # 影响社会群体
            business_crowd.append(data[0])  # 是否影响商务人群
            public.append(data[1])  # 是否影响社会大众

            show.append(data[0])
            sing.append(data[0])
            sport.append(data[1])
            meeting.append(data[0])
            weather.append(data[0])

            history.append(data[1])
            year_times.append(data[1])

        if (len(titles) == 0):
            return 'null'
        dict = {
            u'标题': titles,
            u'开始日期': start_times, u'结束日期': endtimes,
            u'是否是国际性组织': zhuban_level_International, u'是否是国家政府': zhuban_level_Country,
            u'是否是省政府': zhuban_level_Province, u'是否是地方级政府': zhuban_level_City,
            u'是否是否是国内民间协会': guonei_nogoven, u'是否是国际民间协会': guoji_nogoven, u'是否是国内行业协会': guonei_hangye,
            u'是否是国际行业协会': guoji_hangye,
            # u'主要影响年龄层为儿童': children, u'主要影响年龄层为青年': youth, u'主要影响年龄层为成年': adult, u'主要影响年龄层为老年': older,
            u'是否有固定的参与人群': attend,
            u'是否影响商务人群': business_crowd, u'是否影响社会大众': public,
            u'是否展会': show, u'是否演唱会': sing, u'是否体育赛事': sport, u'是否会议': meeting, u'是否天气': weather,
            u'事件历史悠久程度': history,
            u'事件一年内频率': year_times

        }
        return dict

    def to_weather_csv(self, csv_name):
        titles = []
        start_times = []
        endtimes = []
        # 主办方级别
        zhuban_level_International = []
        zhuban_level_Country = []
        zhuban_level_Province = []
        zhuban_level_City = []

        # 主办方类型
        domestic_nogoven = []
        international_nogoven = []
        domestic_hangye = []
        international_hangye = []

        # 主要影响的年龄阶段
        children = []
        youth = []
        adult = []
        older = []

        # 是否有固定的参与人群
        attend = []

        # 是否影响社会群体
        business_crowd = []  # 是否影响商务人群
        public = []  # 是否影响社会大众

        # max_Global=[]
        # max_Intercontinental=[]
        # max_Country=[]
        # max_Province=[]
        # max_City=[]

        show = []
        sing = []
        sport = []
        meeting = []
        weather = []

        # 事件历史悠久程度
        history = []

        # 事件一年内频率
        year_times = []

        # 事件热度
        heat = []

        data = ['0', '1']

        df = pd.read_csv(csv_name)
        title = list(df['标题'])
        start_time = list(df['开始日期'])
        endtime = list(df['结束日期'])
        tag = list(df['标记'])
        num = len(title)
        # print type(csv_name)
        for i in range(num):
            # 标记
            if (tag[i] == 1):
                continue

            titles.append(title[i])
            start_times.append(start_time[i])
            endtimes.append(endtime[i])

            # 主办方级别
            # 默认是0，即主办方级别各项都为0
            zhuban_level_International.append(data[0])
            zhuban_level_Country.append(data[0])
            zhuban_level_Province.append(data[0])
            zhuban_level_City.append(data[0])

            # 主办方类型
            domestic_nogoven.append(data[0])
            international_nogoven.append(data[0])
            domestic_hangye.append(data[0])
            international_hangye.append(data[0])

            # 主要影响的年龄阶段
            children.append(data[1])
            youth.append(data[1])
            adult.append(data[1])
            older.append(data[1])

            # 是否有固定的参与人群
            attend.append(data[0])

            # 影响社会群体
            business_crowd.append(data[1])  # 是否影响商务人群
            public.append(data[1])  # 是否影响社会大众

            # 默认最大影响全市是，该项填1
            # max_Global.append(data[0])
            # max_Intercontinental.append(data[0])
            # max_Country .append(data[0])
            # max_Province.append(data[0])
            # max_City.append(data[1])


            show.append(data[0])
            sing.append(data[0])
            sport.append(data[0])
            meeting.append(data[0])
            weather.append(data[1])

            history.append(data[0])
            year_times.append(data[0])
            heat.append(data[1])

        if (len(titles) == 0):
            return 'null'

        dict = {
            u'标题': titles,
            u'开始日期': start_times, u'结束日期': endtimes,
            u'是否是国际性组织': zhuban_level_International, u'是否是国家政府': zhuban_level_Country, u'是否是省政府': zhuban_level_Province,
            u'是否是地方级政府': zhuban_level_City,
            u'是否是否是国内民间协会': domestic_nogoven, u'是否是国际民间协会': international_nogoven, u'是否是国内行业协会': domestic_hangye,
            u'是否是国际行业协会': international_hangye,
            u'主要影响年龄层为儿童': children, u'主要影响年龄层为青年': youth, u'主要影响年龄层为成年': adult, u'主要影响年龄层为老年': older,
            u'是否有固定的参与人群': attend,
            u'是否影响商务人群': business_crowd, u'是否影响社会大众': public,
            # u'最大影响全球':max_Global, u'最大影响洲际':max_Intercontinental, u'最大影响全国':max_Country, u'最大影响全省':max_Province, u'最大影响全市':max_City,
            u'是否展会': show, u'是否演唱会': sing, u'是否体育赛事': sport, u'是否会议': meeting, u'是否天气': weather,
            u'事件历史悠久程度': history,
            u'事件一年内频率': year_times,
            u'事件热度': heat

        }
        return dict

    def to_sing_csv(self, csv_name):
        titles = []
        start_times = []
        endtimes = []
        # 主办方级别
        zhuban_level_International = []
        zhuban_level_Country = []
        zhuban_level_Province = []
        zhuban_level_City = []

        # 主办方类型
        domestic_nogoven = []
        international_nogoven = []
        domestic_hangye = []
        international_hangye = []

        # 是否有固定的参与人群
        attend = []

        # 是否影响社会群体
        business_crowd = []  # 是否影响商务人群
        public = []  # 是否影响社会大众

        max_Global = []
        max_Intercontinental = []
        max_Country = []
        max_Province = []
        max_City = []

        show = []
        sing = []
        sport = []
        meeting = []
        weather = []

        # 事件历史悠久程度
        history = []

        # 事件一年内频率
        year_times = []

        data = ['0', '1']
        # str = csv_name  # 通过文件名来判断事件类型
        # s = str.split('\\')[-1].split('.')[0]
        # print s

        df = pd.read_csv(csv_name)
        title = list(df['标题'])
        start_time = list(df['开始日期'])
        endtime = list(df['结束日期'])
        tag = list(df['标记'])
        num = len(title)
        # print type(csv_name)
        for i in range(num):
            # 标记
            if (tag[i] == 1):
                continue

            titles.append(title[i])
            start_times.append(start_time[i])
            endtimes.append(endtime[i])
            # 主办方级别
            # 默认是0，即主办方级别各项都为0
            zhuban_level_International.append(data[0])
            zhuban_level_Country.append(data[0])
            zhuban_level_Province.append(data[0])
            zhuban_level_City.append(data[0])

            # 主办方类型
            domestic_nogoven.append(data[0])
            international_nogoven.append(data[0])
            domestic_hangye.append(data[0])
            international_hangye.append(data[0])

            # 是否有固定的参与人群
            attend.append(data[0])

            # 影响社会群体
            business_crowd.append(data[0])  # 是否影响商务人群
            public.append(data[1])  # 是否影响社会大众

            # 默认最大影响全市是，该项填1
            max_Global.append(data[0])
            max_Intercontinental.append(data[0])
            max_Country.append(data[0])
            max_Province.append(data[0])
            max_City.append(data[1])

            show.append(data[0])
            sing.append(data[1])
            sport.append(data[0])
            meeting.append(data[0])
            weather.append(data[0])

            history.append(data[1])
            year_times.append(data[1])

        if (len(titles) == 0):
            return 'null'

        dict = {
            u'标题': titles,
            u'开始日期': start_times, u'结束日期': endtimes,
            u'是否是国际性组织': zhuban_level_International, u'是否是国家政府': zhuban_level_Country,
            u'是否是省政府': zhuban_level_Province, u'是否是地方级政府': zhuban_level_City,
            u'是否是否是国内民间协会': domestic_nogoven, u'是否是国际民间协会': international_nogoven, u'是否是国内行业协会': domestic_hangye,
            u'是否是国际行业协会': international_hangye,
            u'是否有固定的参与人群': attend,
            u'是否影响商务人群': business_crowd, u'是否影响社会大众': public,
            # u'最大影响全球': max_Global, u'最大影响洲际': max_Intercontinental, u'最大影响全国': max_Country, u'最大影响全省': max_Province,
            # u'最大影响全市': max_City,
            u'是否展会': show, u'是否演唱会': sing, u'是否体育赛事': sport, u'是否会议': meeting, u'是否天气': weather,
            u'事件历史悠久程度': history,
            u'事件一年内频率': year_times
        }
        return dict

    def to_news_csv(self, csv_name):
        print csv_name
        titles = []

        # 时间
        start_times = []
        endtimes = []

        # 地点
        places = []

        # 主办方级别
        zhuban_level_International = []
        zhuban_level_Country = []
        zhuban_level_Province = []
        zhuban_level_City = []

        # 主办方类型
        domestic_nogoven = []
        international_nogoven = []
        domestic_hangye = []
        international_hangye = []

        # 是否有固定的参与人群
        attend = []

        # 是否影响社会群体
        business_crowd = []  # 是否影响商务人群
        public = []  # 是否影响社会大众

        max_Global = []
        max_Intercontinental = []
        max_Country = []
        max_Province = []
        max_City = []

        show = []
        sing = []
        sport = []
        meeting = []
        weather = []

        # 事件历史悠久程度
        history = []

        # 事件一年内频率
        year_times = []

        data = ['0', '1']
        # str = csv_name  # 通过文件名来判断事件类型
        # s = str.split('\\')[-1].split('.')[0]
        # print s

        df = pd.read_csv(csv_name)
        title = list(df['标题'])
        # print title
        start_time = list(df['开始日期'])
        endtime = list(df['结束日期'])
        place = list(df['地点'])
        tag = list(df['标记'])
        num = len(title)
        # print type(csv_name)
        for i in range(num):
            # 标记
            if (tag[i] == 1):
                continue

            titles.append(title[i])
            # 时间
            start_times.append(start_time[i])
            endtimes.append(endtime[i])
            # 地点
            places.append(place[i])

            # 主办方级别
            # 默认是0，即主办方级别各项都为0
            zhuban_level_International.append(data[0])
            zhuban_level_Country.append(data[0])
            zhuban_level_Province.append(data[0])
            zhuban_level_City.append(data[0])

            # 主办方类型
            domestic_nogoven.append(data[0])
            international_nogoven.append(data[0])
            domestic_hangye.append(data[0])
            international_hangye.append(data[0])

            # 是否有固定的参与人群
            attend.append(data[0])

            # 影响社会群体
            business_crowd.append(data[0])  # 是否影响商务人群
            public.append(data[1])  # 是否影响社会大众

            # 默认最大影响全市是，该项填1
            max_Global.append(data[0])
            max_Intercontinental.append(data[0])
            max_Country.append(data[0])
            max_Province.append(data[0])
            max_City.append(data[1])

            show.append(data[0])
            sing.append(data[0])
            sport.append(data[0])
            meeting.append(data[1])
            weather.append(data[0])

            history.append(data[1])
            year_times.append(data[1])

        if (len(titles) == 0):
            return 'null'

        dict = {
            u'标题': titles,
            u'开始日期': start_times,
            u'结束日期':endtimes,
            u'地点': places,
            u'是否是国际性组织': zhuban_level_International, u'是否是国家政府': zhuban_level_Country,
            u'是否是省政府': zhuban_level_Province, u'是否是地方级政府': zhuban_level_City,
            u'是否是否是国内民间协会': domestic_nogoven, u'是否是国际民间协会': international_nogoven, u'是否是国内行业协会': domestic_hangye,
            u'是否是国际行业协会': international_hangye,
            u'是否有固定的参与人群': attend,
            u'是否影响商务人群': business_crowd, u'是否影响社会大众': public,
            # u'最大影响全球': max_Global, u'最大影响洲际': max_Intercontinental, u'最大影响全国': max_Country, u'最大影响全省': max_Province,
            # u'最大影响全市': max_City,
            u'是否展会': show, u'是否演唱会': sing, u'是否体育赛事': sport, u'是否会议': meeting, u'是否天气': weather,
            u'事件历史悠久程度': history,
            u'事件一年内频率': year_times

        }
        return dict

    def to_csv(self, dict, value):
        filename = 'C:/untitled2/Softbei/analyse_data/common/csv/%s/%s_other.csv' % (value, value)
        if (dict == 'null'):
            print '没有可生成的数据'
        else:
            print filename
            pd.DataFrame(dict).to_csv(filename, encoding='utf8', index=None)

    # noinspection PyGlobalUndefined
    def main_void(self, value):
        # noinspection PyGlobalUndefined
        global dict
        print value
        if value == "eshow":
            dict = self.to_eshow_csv("C:/untitled2/Softbei/removal_csv/csv/eshow.csv")
        elif value == "news":
            dict = self.to_news_csv("C:/untitled2/Softbei/removal_csv/csv/news.csv")
        elif value == "sing":
            dict = self.to_sing_csv("C:/untitled2/Softbei/removal_csv/csv/sing.csv")
        elif value == "sport":
            dict = self.to_sport_csv("C:/untitled2/Softbei/removal_csv/csv/sport.csv")
        elif value == "weather":
            dict = self.to_weather_csv("C:/untitled2/Softbei/removal_csv/csv/weather.csv")

        self.to_csv(dict, value)
        print '--------------------------********************----------------------------------'

    def main_handle_other(self, types):
        self.main_void(types)
        # list = ['eshow', 'news', 'sing', 'sport', 'weather']  # list表中存放表名，下面选择许序号会从list中取出对应的值
        # # list=['news']
        # for s in list:
        #     self.main_void(s)


if __name__ == '__main__':
    OtherCsv().main_handle_other(types='sing')
