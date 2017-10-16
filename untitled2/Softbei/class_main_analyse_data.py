# coding:utf8
import sys

from selenium import webdriver

from Softbei.analyse_data.class_age import Age
from Softbei.analyse_data.class_getcity import GetCity
from Softbei.analyse_data.class_getzhuban import ZhuBan
from Softbei.analyse_data.class_history import History
from Softbei.analyse_data.class_hot import Hot
from Softbei.analyse_data.class_merge_csv import MergeCsv
from Softbei.analyse_data.class_other_csv import OtherCsv
from Softbei.analyse_data.class_weather_warning import WeatherWarning
from Softbei.analyse_data.class_year_times import YearTimes
from Softbei.removal_csv.class_removal import Removal
from Softbei.to_csv.class_to_csv import ToCsv
from selenium.webdriver import ActionChains

reload(sys)
sys.setdefaultencoding('utf8')

'''
调用分析数据的方法,
分析数据之前请确保你已经爬取了数据或者数库中存在数据

'''

class AnalyseData:
    if __name__ == '__main__':

        ToCsv().main_to_csv(types='sing')  # 数据库数据转换为csv
        Removal().main_removal(types='sing')  # 去重
        Age(driver=webdriver.Chrome()).main_age(types='sing')  # 年龄
        Hot(driver=webdriver.Chrome()).main_hot(types='sing')  # 热度
        History().main_history(types='eshow')  # 历史悠久程度
        YearTimes().main_year_times(types='eshow') # 事件一年内的频率
        ZhuBan().main_zhuban(types='eshow')  # 主办方
        WeatherWarning().main_weather_warning(types='weather')  # 天气预警
        GetCity().main_place(types='sing')  # 地点
        OtherCsv().main_handle_other(types='sing')
        MergeCsv().main_merge_csv(types='sing')  # 合并,文件存放在analyse_data/common/csv
