#coding:utf8
from Softbei.analyse_data.city import GetCitys
from Softbei.common.class_database import DB
from Softbei.grab_data.news.class_ltplearning import NewsItplearning
from Softbei.to_csv.class_handle_time import HandleTime
from untitled2 import Task,tell
import sys
from untitled2 import db
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
option = webdriver.ChromeOptions()
option.add_argument(
        r'--user-data-dir=C:\Users\hzl\AppData\Local\Google\Chrome\User Data\Default\Default')  # 设置成用户自己的数据目录

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
c = DB()
def taks(id):
    # 获取爬虫配置信息
    args = id
    result = Task.query.filter_by(id=args).first()
    print '----------------线程爬虫已经启动-------------------'
    if result:
        type = ["演唱会类", "展会类", "时政类", "体育赛事类", "异常天气类"]
        # 0, 1, 2, 3, 4
        type_l = ['sing', 'eshow', 'news', 'sport', 'weather']
        types = list(result.types.split(","))
        for x in types:
            value = type[int(x)]
            if value == "演唱会类":
                analyse_data_sing_or_sport(type_l[0])
            elif value == "展会类":
                analyse_data_eshow(type_l[1])
            elif value == "时政类":
                analyse_data_news(type_l[2])
            elif value == "体育赛事类":
                analyse_data_sing_or_sport(type_l[3])
            elif value == "异常天气类":
                analyse_data_weather(type_l[4])
        c.updata_db()  # 更新数据库
        # GetCitys().to_place()  # 统一城市名

        result.status = 1
        db.session.commit()
    else:
        tell(1)


def analyse_data_eshow(t):
    ToCsv().main_to_csv(types=t)  # 数据库数据转换为csv
    Removal().main_removal(types=t)  # 去重
    Age(driver=webdriver.Chrome(chrome_options=option)).main_age(types=t)  # 年龄
    Hot(driver=webdriver.Chrome()).main_hot(types=t)  # 热度
    History().main_history(types='eshow')  # 历史悠久程度
    YearTimes().main_year_times(types='eshow')  # 事件一年内的频率
    ZhuBan().main_zhuban(types='eshow')  # 主办方
    OtherCsv().main_handle_other(types=t)
    MergeCsv().main_merge_csv(types=t)  # 合并,文件存放在analyse_data/common/csv
    c.to_db(types=t)  # 将分析好的数据存入数据库


def analyse_data_sing_or_sport(t):
    HandleTime().main_void(types=t)#时间格式转换
    ToCsv().main_to_csv(types=t)  # 数据库数据转换为csv
    Removal().main_removal(types=t)  # 去重
    Age(driver=webdriver.Chrome(chrome_options=option)).main_age(types=t)  # 年龄
    Hot(driver=webdriver.Chrome()).main_hot(types=t)  # 热度
    GetCity().main_place(types=t)  # 地点
    OtherCsv().main_handle_other(types=t)
    MergeCsv().main_merge_csv(types=t)  # 合并,文件存放在analyse_data/common/csv
    c.to_db(types=t)  # 将分析好的数据存入数据库


def analyse_data_weather(t):
    HandleTime().main_void(types=t) #时间格式转换
    ToCsv().main_to_csv(types=t)  # 数据库数据转换为csv
    Removal().main_removal(types=t)  # 去重
    WeatherWarning().main_weather_warning(types=t)  # 天气预警
    OtherCsv().main_handle_other(types=t)
    MergeCsv().main_merge_csv(types=t)  # 合并,文件存放在analyse_data/common/csv
    c.to_db(types=t)  # 将分析好的数据存入数据库



def analyse_data_news(t):
    # ToCsv().main_to_csv(types=t)  # 数据库数据转换为csv
    # Removal().main_removal(types=t)  # 去重
    # Age(driver=webdriver.Chrome()).main_age(types=t)  # 年龄
    # Hot(driver=webdriver.Chrome()).main_hot(types=t)  # 热度
    # OtherCsv().main_handle_other(types=t)
    # MergeCsv().main_merge_csv(types=t)  # 合并,文件存放在analyse_data/common/csv
    NewsItplearning().main()  # 语义分析
    c.delete_title(table=t)
    c.select_news_time()
    ToCsv().main_to_csv(types=t)
    Removal().main_removal(types=t)
    Age(driver=webdriver.Chrome(chrome_options=option)).main_age(types=t)  # 年龄
    Hot(driver=webdriver.Chrome()).main_hot(types=t)  # 热度
    OtherCsv().main_handle_other(types=t)
    MergeCsv().main_merge_csv(types=t)  # 加热度，可选择
    c.to_db(types=t)  # 将分析好的数据存入数据库

