# coding:utf8


from Softbei.common.class_database import DB

exitFlag = 0
import requests
from bs4 import BeautifulSoup

'''
单线程爬取大麦网演唱会数据
'''
def get_content(data):
    a = DB()
    response = requests.get(data)
    if (response.status_code == 200):
        obj = BeautifulSoup(response.content, 'html.parser')
        li = obj.find('ul', id="performList").find_all('li')
        for i in li:
            title = i.find('h2').find('a').string  # 获取事件名
            href = 'https:' + i.find('h2').find('a')['href']  # 获取活动链接
            strings = i.find('p', class_='mt5').strings  # 获取标签立马所有文本
            strings = list(strings)  # 转成list集合便于下面操作
            changuan = strings[2]  # 获得地点，城市名
            time = strings[0].strip()[3:]  # 字符串截取

            if len(a.select(table='sing', title=title)) == 0:
                print title
                print href
                print changuan
                print time
                a.insert(table='sing', title=title, start_time=time, changuan=changuan, page_link=data, url=href)
            else:
                print '存在'