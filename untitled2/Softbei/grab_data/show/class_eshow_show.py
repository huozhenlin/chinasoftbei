# -*- coding: utf-8 -*-
from Softbei.common.class_database import *
reload(sys)
sys.setdefaultencoding('utf-8')


class Eshow:
    def __init__(self,url):
        self.url=url
        self.get_news()

    def getshowurl(self, href, title):
        c = DB()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        res = requests.get(url=href, headers=headers)

        res.encoding = 'utf-8'
        response = res.text
        bs = BeautifulSoup(response, 'html.parser')
        x = bs.find('div', class_='zhxxcontent').find_all('p')
        try:
            # while True:
            #     time.sleep(86400)
            show_title = ",".join(title.split())
            start_time = x[2].string.strip().split('：')[1].split('---')[0]
            endtime = x[2].string.strip().split('：')[1].split('---')[1]
            zhanguan = x[3].contents[1].string.strip()
            hangye = x[4].contents[1].string.strip()
            # 06.21
            place = x[5].string.strip().split('：')[1].split('|')[1]
            zhuban = x[6].string.split('：')[1].strip()
            show_zhuban = ''
            show_zhuban = ",".join(zhuban.split())
            hold_num = ''
            hold_cycle = ''
            for i in range(1, 5):
                if ((x[-i].string.strip().find('举办届数')) != -1):
                    hold_num = x[-i].string.strip().split('：')[1]
                if (len(hold_num) > 0):
                    break

                for i in range(1, 5):
                    if ((x[-i].string.strip().find('举办周期')) != -1):
                        hold_cycle = x[-i].string.strip().split('：')[1]
                    if (len(hold_cycle) > 0):
                        break

            if (len(hold_num) == 0):
                hold_num = 'null'

            if (len(hold_cycle) == 0):
                hold_cycle = 'null'

            if (zhuban.find('平方米') != -1):
                show_zhuban = 'null'
        except Exception as e:
            print e.message
            # print 'not found'

        if len(c.select(table='eshow', title=title)) == 0:
            c.insert_eshow(table='eshow', start_time=start_time, endtime=endtime, title=show_title, url=href,
                           place=place, hangye=hangye, hold_num=hold_num, hold_cycle=hold_cycle, zhanguan=zhanguan,
                           zhuban=show_zhuban)
        else:
            print '存在'


    def get_news(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        res = requests.get(self.url, headers=headers)

        res.encoding = 'utf-8'
        bs = BeautifulSoup(res.text, 'html.parser')
        x = bs.find('div', class_='cityzhlistaa').find_all('ul')
        for i in x:
            li = i.find_all('li')
            for a in li:
                href = a.find('div', class_='lefttitle').find('a')['href']
                title = a.find('div', class_='lefttitle').find('a')['title']
                self.getshowurl(href, title)



#程序入口
if __name__ == '__main__':
    a = Eshow('http://www.eshow365.com/')