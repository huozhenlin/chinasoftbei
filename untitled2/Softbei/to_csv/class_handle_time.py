#coding:utf8
from Softbei.common.class_database import *



'''
主函数，用于更新数据库中的时间格式
'''
class HandleTime:
    def main_void(self, types):
        c = DB()
        # 更新时间(演唱会和运动)
        if types == "sing" or types =="sport":
            c.select_sport_or_sing(table=types)
            # 更新新闻网时间
        # elif types =="news":
        #     c.select_news_or_weather_time(types='news')
            #更新天气
        elif types =="weather":
            c.select_news_or_weather_time(table='weather')




if __name__ == '__main__':
    HandleTime().main_void(types="sing")