#coding:utf8
import sys
from Softbei.common.class_database import *
# from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf-8')



class DamaiSport:
    weather_urls=[]

    def __init__(self,url,driver):
        self.url=url
        self.driver = driver
        self.get_news()



    def analyse(self , x):
        c = DB()
        try:
            # while True:
            #     time.sleep(86400)
            li = x.find_all('li')
            for i in li:
                div = i.find('div', class_='new-list-info')
                href = 'https:' + div.find('a')['href']
                title = div.find('a').string.strip()
                p = div.find_all('p')
                times = p[1].contents[0].split()[0].split('：')[1]
                changuan = p[1].contents[1].find('a').string
                if len(c.select(table='sport', title=title)) == 0:
                    c.insert_sport(table='sport', start_time=times, title=title, url=href, changuan=changuan)
                else:
                    print '存在'

                    # time.sleep(5)
        except Exception as e:
            print 'not found'


    def getmore(self, href):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        res = requests.get(href, headers=headers)
        res.encoding = 'utf-8'
        bs = BeautifulSoup(res.text, 'html.parser')
        x = bs.find('div', class_='s_item s_perform').find('div', class_='in')
        self.analyse(x)
        pages = bs.find('div', class_='pagination').find('label', id='pager')['data-pagecount']
        print pages
        self.driver.get(href)
        for x in range(int(pages) - 1):
            self.driver.find_element_by_link_text('下一页').click()
            time.sleep(2)
            bs1 = BeautifulSoup(self.driver.page_source, 'html.parser')
            x1 = bs1.find('div', class_='s_item s_perform').find('div', class_='in')
            self.analyse(x1)



    def get_news(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        res = requests.get(self.url, headers=headers)
        res.encoding = 'utf-8'
        bs = BeautifulSoup(res.text, 'html.parser')
        x=bs.find('dl', id='subCategory')#获取到li,直接返回元素
        li=x.find_all('a')
        for i in li[0:3]:
            href = 'https://s.damai.cn'+i['href']
            print href
            self.getmore(href)
        self.driver.close()
            # getmore(href)
            # time.sleep(5)


if __name__ == "__main__":
    from selenium import webdriver
    a = DamaiSport('https://s.damai.cn/ticket/sports.html',driver=webdriver.Chrome())
