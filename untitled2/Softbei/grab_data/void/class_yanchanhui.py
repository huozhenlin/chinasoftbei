#coding:utf8
from bs4 import BeautifulSoup
import requests
import Queue
import threading

'''
共有的爬取类，用于返回两个网站演唱会类型数据的页数
'''
class GetData:
    urls=[]
    def __init__(self,url):
        self.url=url

    #获取页数
    def get_pages(self):
        if self.url.startswith('http://www.idaocao.com/'):
            content = requests.get('http://www.idaocao.com/yulenews/yanchu_sort.do?sid=8')
            if content.status_code == 200:
                bsobj = BeautifulSoup(content.content, 'html.parser')
                a = bsobj.find('div', class_='pagelist').find_all('a')[-2].string
                return a
            else:
                print '爱稻草网请求错误'
        elif self.url.startswith('https://www.damai.cn/'):
            response=requests.get(self.url)
            if (response.status_code == 200):
                # 获取共有多少页数据
                bsObj = BeautifulSoup(response.content, 'html.parser')
                pages = bsObj.find('div', class_='pagination').find('span', class_='ml10').text[1:-2]  # 获取页数
                return pages
            else:
                print '大麦网请求错误'



