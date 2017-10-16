#coding:utf8
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from Softbei.common.class_database import *

reload(sys)
sys.setdefaultencoding('utf-8')

class YongleSport:
    weather_urls=[]
    def __init__(self,url):
        self.url=url
        self.get_news()

    def get_news(self):
        c = DB()
        driver=webdriver.Chrome()
        driver.get(self.url)
        content=driver.page_source
        bs=BeautifulSoup(content,'html.parser')
        x=bs.select('#category-box > div.category-boxb > ul > li.category-boxb-ul-ft > span')
        mod=0
        num=int(x[0].string)#商品的数量21
        if(num%20!=0):
            mod=1
        count=150*(num/20+mod)#下滑的次数
        i = 0
        while i < count:
            ActionChains(driver).key_down(Keys.DOWN).perform()
            # print(i)
            i += 1
        time.sleep(3)
        bs=BeautifulSoup(driver.page_source,'html.parser')
        x=bs.find('div', class_='category-cont-list').find('div').find('div',id='pages')#获取到li,直接返回元素
        dl=x.find_all('dl',class_='category-cont-listdl')
        try:
            # while True:
            #     time.sleep(86400)
                for i in dl:
                    dd=i.find_all('dd',class_='category-cont-listdd clearfloat')
                    for ul in dd:
                        title=ul.find('a').contents[0].string.strip()
                        href = ul.find('a')['href']
                        li=ul.find_all('ul',class_='category-cont-listdd-a')
                        for l in li:
                            span=l.find_all('li')
                            times=span[0].contents[2].string.strip()
                            changuan=span[1].find('a').string

                            if len(c.select(table='sport', title=title)) == 0:
                                c.insert_sport(table='sport', start_time=times, title=title, url=href,
                                               changuan=changuan)
                            else:
                                print '存在'

                driver.close()

        except Exception as e:
            print 'not found'


# a=harsh_sport('http://www.228.com.cn/category/tiyusaishi/')

if __name__ == '__main__':
    a = YongleSport('http://www.228.com.cn/category/tiyusaishi/')
    # a = harsh_news('http://news.sina.com.cn/china/')