#coding:utf8
from Softbei.common.class_database import *

'''
数据入口为:http://www.idaocao.com/yulenews/yanchu_sort.do?sid=8
这里是捉取爱稻草网的演唱会类事件，是演唱会类事件的数据来源之一
提供两个方法
第一个：获取演唱会事件共有多少页
第二个：分析网页结构获取数据
'''

class IdaocaoSing:
    #获取页数
    def get_page(self):
        content = requests.get('http://www.idaocao.com/yulenews/yanchu_sort.do?sid=8')
        if content.status_code == 200:
            bsobj=BeautifulSoup(content.content,'html.parser')
            a=bsobj.find('div',class_='pagelist').find_all('a')[-2].string
            return a

    #开始捕获爱稻草网的数据,地点先留空
    # @staticmethod
    def get_idaocao(self):
        a=self.get_page()#获取一共有多少页数据
        for i in range(1,int(a)/20):
            url="http://www.idaocao.com/yulenews/yanchu_sort.do?sid=8&page=%d"%i
            print url
            time.sleep(10)
            content=requests.get(url)
            if content.status_code==200:
                a=DB()#实例化DB对象
                bsobj=BeautifulSoup(content.content,'html.parser')
                try:
                    li=bsobj.find('div',class_='mainList').find('ul',class_='wen').find_all('li')
                    for i in li:
                        href=i.find_all('a')[0]['href'][2:]
                        href="http://www.idaocao.com"+href  #爱稻草网页中演唱会的链接
                        title=i.find('span',class_='title').string#爱稻草网页中演唱会的标题
                        data=i.find('span',class_='date').string#爱稻草网页中演唱会的时间

                        #插入之前对数据库进行查询，确保爬取到的标题在数据库中不存在才插入
                        num = a.select(table='sing', title=title)
                        print len(num)
                        if len(num)==0:
                            #往sing表中插入数据
                            a.insert(table='sing',title=title,start_time=data,changuan='null',url=href,page_link=url)
                            print href
                            print title
                            print data
                except Exception as e:
                    print e.message


if __name__ == '__main__':
    IdaocaoSing().get_idaocao()

    # I = Idaocao_sing()
    # I.get_idaocao()

    # Idaocao_sing.get_idaocao()