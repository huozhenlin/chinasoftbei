#coding:utf8
from Softbei.common.class_database import *

'''
定义一个异常天气爬取类，继承自DB数据库连接类想，实例化类时需要传入一个参数，为天气的地址
类有get_weather()一个爬取网页并分析数据的方法
'''
class TuFaWeather:

    weather_urls=[]
    def __init__(self,url):
        self.url=url;
        self.url = url;
        self.get_weather()

    #天气爬取的方法，获取标题，时间（时间后期处理，生成开始时间，结束时间），天气的链接
    def get_weather(self):
        c=DB()
        driver=webdriver.Chrome()
        driver.get(self.url)
        import time
        time.sleep(20)
        driver.find_element_by_xpath("//*[@id='future6ForecastNav']/a[2]").click()
        time.sleep(10)
        frame=driver.find_element_by_xpath("//*[@id='tab_con1']/div[2]/iframe");
        driver.switch_to_frame(frame)
        # 获取网页源代码
        content = driver.page_source
        bs=BeautifulSoup(content,'html.parser')
        x=bs.find('div', class_='dDisasterAlarm').find_all('ul')
        print x
        for i in x:
            li=i.find_all('li')
            print li
            for a in li:
                href=a.find_all('a')[1]['href']#天气链接
                print href
                title=a.find_all('a')[1].string#天气标题
                print title
                time=a.find('span',class_='dTime').string#天气发布时间
                print time
                num=c.select2(table='weather', url=href)
                print num
                if len(num) == 0:
                    c.insert0(table='weather', url=href, title=title, start_time=time)
                else:
                    print '存在'

            print '------------'
        driver.close()


if __name__ == '__main__':
    a = TuFaWeather('http://www.weather.com.cn/alarm/#')