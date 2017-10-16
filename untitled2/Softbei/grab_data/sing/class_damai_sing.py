#coding:utf8
import Queue
import threading
import time
import requests
from bs4 import BeautifulSoup
from Softbei.common.class_database import DB
from Softbei.grab_data.void.class_yanchanhui import GetData
import sys

reload(sys)
sys.setdefaultencoding('utf8')
'''
这是一个使用多线程成去捉取大麦网演唱会类事件的类
使用多线程可以提高爬取速度
'''
# 锁对象
queueLock = threading.Lock()
# 队列数
workQueue = Queue.Queue()


class DamaiSing(threading.Thread):
    # 构造函数，闯入threadId，每一个任务list，队列
    # 参数1，线程id；参数2，线程名；参数3，队列数
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        # print threading.Thread
        self.threadID = threadID
        self.name = name
        self.q = q
        # self.exitFlag=exitFlag


    # def stop(self):
    #     self.__flag.clear()
    #     print 'clear'

    # 自动执行的run函数，里面的process_data就是我们具体执行的代码
    def run(self):
        print ("开启线程：" + self.name)
        self.process_data(self.name, self.q)
        print ("退出线程：" + self.name)


    def process_data(self, threadName, q):
        i=0
        exitFlag = 0
        # 如果没有退出，就获得锁对象
        while not exitFlag:
            i += 1
            # print '-------iiiiiiii------'
            # print i
            queueLock.acquire()
            if not workQueue.empty():
                # 从队列中获得任务
                print 'come in'
                data = q.get()
                # 获得任务后释放锁
                # 然后输出
                print "%s processing %s" % (threadName, data)
                self.get_content(data) #data为网页
                queueLock.release()
            else:
                # 否者，队列为空，直接释放锁
                queueLock.release()
                if i > 1:
                    print 'hi---------'
                    exitFlag = 1


            time.sleep(1)



    def get_content(self, data):
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

    @staticmethod
    def mytask():
        # 任务
        a = GetData('https://www.damai.cn/projectlist.do?mcid=1')  # 实例化对象，去捉取大麦网的数据
        pages = a.get_pages()  # 得到它的页数
        nameList = []
        for i in range(1, int(pages) + 1):
            url = 'https://www.damai.cn/projectlist.do?mcid=1&pageindex=%d' % (i)
            nameList.append(url)
        return nameList

    # @staticmethod
    def start_thread(self):
        # while True:
        threads = []
        # 线程id
        threadID = 1

        # 线程数
        threadList = []
        for b in range(4):
            threadList.append(b)
        # Create new threads
        for tName in threadList:
            # 参数1，线程id；参数2，线程名；参数3，队列数
            thread = DamaiSing(threadID, tName, workQueue)
            thread.start()
            threads.append(thread)
            threadID += 1

        # Fill the queue
        queueLock.acquire()
        for word in DamaiSing.mytask():
            workQueue.put(word)
        queueLock.release()

        # Wait for queue to empty
        while not workQueue.empty():
            pass

        # Notify threads it's time to exit
        # exitFlag = 1
        exitFlag=1

        # Wait for all threads to complete
        # print threads
        # while True:
        # print "---------**********************************--------------"
        # for t in threads:
        #     print t
            # self.process_data(threadName=t.getName, q=workQueue, exitFlag=1)
            # print t.join()
            # print type(t)
            # print t.isAlive()
            # print t.getName()
        # print "Exiting Main Thread"
        
if __name__ == "__main__":
    # print workQueue
    DamaiSing(threadID=1,name=None, q=None).start_thread()

