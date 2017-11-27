# coding:utf8
import ctypes
import inspect
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import or_

from Softbei.grab_data.news.class_news import New
from Softbei.grab_data.weather.class_tufa_weather import TuFaWeather
from util import Util
from Softbei.grab_data.show.class_eshow_show import Eshow
from Softbei.grab_data.sing.class_damai_sing_onethread import get_content
from Softbei.grab_data.sing.class_idaocao_sing import IdaocaoSing
from Softbei.grab_data.sport.class_damai_sport import DamaiSport
from Softbei.grab_data.sport.class_yongle_sport import YongleSport
from Softbei.grab_data.void.class_yanchanhui import GetData
import config
from apscheduler.schedulers.blocking import BlockingScheduler
from decorators import login_required

import threading
import datetime
import sys
from selenium import webdriver

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 全局共享变量
global ids
lock = threading.RLock()
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
A = Util()
list_t = []


# 抛出系统级异常
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    print '-------------res------------', res  # res 值为1
    if res == 0:
        print 'hello'
        raise SystemError("invalid thread id")
    elif res == 1:
        # ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("invalid")
    elif res != 1:
        print "stoped"
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


# 线程类
class Thread2(threading.Thread):
    global ids

    def run(self):
        start_splider(id=ids)


# 创建用户模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(13), nullable=False)
    password = db.Column(db.String(50), nullable=False)


# 任务模型
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    types = db.Column(db.String(20), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=True)
    fre = db.Column(db.Integer, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': str(self.time),
            'types': self.types,
            'type': self.type,
            'status': self.status,
            'fre': self.fre
        }


# 演唱会表模型
class Sing(db.Model):
    __tablename__ = 'sing'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.String(255), nullable=True)
    endtime = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    changuan = db.Column(db.String(255), nullable=True)
    page_link = db.Column(db.String(255), nullable=True)
    tag = db.Column(db.Integer, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time,
            'end_time': self.endtime,
            'url': self.url,
            'changuan': self.changuan,
            'page_link': self.page_link,
            'tag ': self.tag
        }


# 体育表模型
class Sport(db.Model):
    __tablename__ = 'sport'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.String(255), nullable=True)
    endtime = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    changuan = db.Column(db.String(100), nullable=True)
    tag = db.Column(db.Integer, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time,
            'endtime': self.endtime,
            'url': self.url,
            'changuan': self.changuan,
            'tag ': self.tag
        }


# 新闻表模型
class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=True)
    start_time = db.Column(db.String(255), nullable=True)
    endtime = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    place = db.Column(db.String(100), nullable=True)
    contents = db.Column(db.Text, nullable=True)
    tag = db.Column(db.Integer, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time,
            'end_time': self.endtime,
            'url': self.url,
            'place': self.place,
            'contents': self.contents,
            'tag ': self.tag
        }


# 展会表模型
class eShow(db.Model):
    __tablename__ = 'eshow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=True)
    start_time = db.Column(db.String(255), nullable=True)
    endtime = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    place = db.Column(db.String(100), nullable=True)
    zhuban = db.Column(db.Text, nullable=True)
    tag = db.Column(db.Integer, nullable=True)
    hangye = db.Column(db.String(100), nullable=True)
    zhanguan = db.Column(db.String(100), nullable=True)
    hold_cycle = db.Column(db.String(100), nullable=True)
    hold_num = db.Column(db.String(100), nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time,
            'endtime': self.endtime,
            'url': self.url,
            'place': self.place,
            'zhanguan': self.zhanguan,
            'hangye': self.hangye,
            'tag': self.tag,
            'zhuban': self.zhanguan,
            'place': self.place,
            'hold_cycle': self.hold_cycle,
            'hold_num ': self.hold_num
        }


# 异常天气模型
class Weather(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(50), nullable=True)
    endtime = db.Column(db.String(255), nullable=True)
    tag = db.Column(db.Integer, nullable=True)

    def to_json(self):
        return {
            'city': 'null',
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time,
            'endtime': self.endtime,
            'url': self.url,
            'tag': self.tag

        }


db.create_all()


@app.route('/')
def hello_word():
    # user=User(account='admin',password='admin')
    # 增加数据
    # db.session.add(user)
    # 查找数据
    # result=User.query.filter(User.account=='admin').all()#查找所有数据
    # result=User.query.filter(User.account=='admin').first()#查找第一条数据
    # print result.password
    # 修改数据
    # result=User.query.filter(User.account=='admin').first()
    # result.username='bbb'
    # 删除数据
    # result=User.query.filter(User.account=='admin').first()
    # db.session.delete(result)
    # 事务提交
    # db.session.commit()
    return '提交成功'


# 跳转不同的页面逻辑判断
@login_required
@app.route('/index/page')
def to_page():
    page = request.args.get('p')
    print page
    if page == '0':
        return render_template('index.html')
    elif page == '1':
        return render_template('now_spilder.html')
    elif page == '2':
        return render_template('frequency_splider.html')
    elif page == '3':
        return render_template('showdata.html')
    elif page == '4':
        return render_template('time_spilder.html')
    elif page == '5':
        return render_template('analy_data.html')
    elif page == '6':
        return render_template('time_analy_data.html')


# 跳转到登陆页面,检测提交方法
@app.route('/login', methods=['GET', 'POST'])
def to_login():
    if session.get('user_id') is not None:
        return render_template('index.html')
    elif request.method == 'GET':
        return render_template('login.html')
    else:
        # 获取前端传过来的用户名和密码
        username = request.form.get('username')
        password = request.form.get('password')
        print username, password
        user = User.query.filter(User.account == username, User.password == password).first()
        if user:
            print user.id
            session['user_id'] = user.id
            return render_template('index.html')
        else:
            print '用户名和密码错误'
            return redirect(url_for('to_login'))


# 注销登录
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')


# 获取爬虫或者分析数据配置信息
@login_required
@app.route('/message', methods=['POST'])
def get_message():
    task_name = request.form.get('task_name')  # 任务名
    select_type = request.form.get('select_type')  # 任务
    splider_type = request.form.get('splider_type')  # 爬虫种类
    time = A.get_curtime()  # 当前系统时间
    print time
    print task_name
    print splider_type
    print select_type
    task = Task(name=task_name, time=time, types=select_type, type=splider_type, status=0)
    db.session.add(task)
    db.session.commit()


# 获取爬虫或者分析数据配置信息
@login_required
@app.route('/message1', methods=['POST'])
def get_message1():
    task_name = request.form.get('task_name')  # 任务名
    select_type = request.form.get('select_type')  # 任务
    splider_type = request.form.get('splider_type')  # 爬虫种类
    time = A.get_curtime()  # 当前系统时间
    fre = request.form.get('frequency')
    print time
    print task_name
    print splider_type
    print select_type
    print fre
    print '频率爬虫添加成功'
    task = Task(name=task_name, time=time, types=select_type, type=splider_type, status=0, fre=fre)
    db.session.add(task)
    db.session.commit()


# 查找分析任务配置数据
@login_required
@app.route('/json2', methods=['GET'])
def scan4():
    args = int(request.args.get('status'))
    result = Task.query.filter_by(status=args, type=2).all()

    temp = []
    if len(result) == 0:
        dict = {"message": "none"}
        return jsonify(dict)

    else:
        for x in result:
            temp.append(x.to_json())

        return jsonify(objects=temp)

        # 查找分析任务配置数据

@login_required
@app.route('/json2all', methods=['GET'])
def scan5():
    args = int(request.args.get('status'))
    result = Task.query.filter(Task.status == args, or_(Task.type == 2, Task.type == 3)).all()  # or
    temp = []
    if len(result) == 0:
        dict = {"message": "none"}
        return jsonify(dict)

    else:
        for x in result:
            temp.append(x.to_json())

        return jsonify(objects=temp)


# 查找任务数据
@login_required
@app.route('/json', methods=['GET'])
def scan():
    args = int(request.args.get('status'))
    result = Task.query.filter_by(status=args, type=0).all()
    temp = []
    if len(result) == 0:
        dict = {"message": "none"}
        return jsonify(dict)

    else:
        for x in result:
            temp.append(x.to_json())

        return jsonify(objects=temp)


# 查找任务数据
@login_required
@app.route('/json1', methods=['GET'])
def scan1():
    args = int(request.args.get('status'))
    type = request.args.get('type')
    result = Task.query.filter_by(status=args, type=type).all()
    temp = []
    if len(result) == 0:
        dict = {"message": "none"}
        return jsonify(dict)
    else:
        for x in result:
            temp.append(x.to_json())

        return jsonify(objects=temp)


# 这是获取所有的爬虫，包括历史和非历史
@login_required
@app.route('/jsonall', methods=['GET'])
def scan3():
    args = int(request.args.get('status'))
    # result = Task.query.filter_by(status=args).all()
    result = Task.query.filter(Task.status == args, or_(Task.type == 0, Task.type == 1, Task.type == 4)).all()  # or
    print str(result)
    temp = []
    if len(result) == 0:
        dict = {"message": "none"}
        return jsonify(dict)
    else:
        for x in result:
            temp.append(x.to_json())
        return jsonify(objects=temp)


# 根据id获取爬虫配置信息
@login_required
@app.route('/querybyid', methods=['GET'])
def scan2():
    args = int(request.args.get('id'))
    result = Task.query.filter_by(id=args).first()
    if result:
        return jsonify(result.to_json())
    else:
        dict = {"message": "none"}
        return jsonify(dict)


# 查找五个表中未分析的数据
@login_required
@app.route('/noanalyse', methods=['GET'])
def search():
    args = request.args.get('table')
    if args == "sing":
        result = Sing.query.filter_by(tag=0).all()
        return to_json(result)
    elif args == "eshow":
        result = eShow.query.filter_by(tag=0).all()
        return to_json(result)
    elif args == "sport":
        result = Sport.query.filter_by(tag=0).all()
        return to_json(result)
    elif args == "news":
        result = News.query.filter_by(tag=0).all()
        return to_json(result)
    elif args == "weather":
        result = Weather.query.filter_by(tag=0).all()
        return to_json(result)


# 删除指定表的数据
@login_required
@app.route("/datadelete", methods=['GET'])
def deletebyid():
    tablename = request.args.get("table")
    id = request.args.get("id")
    print tablename
    print id
    if tablename == "sing":
        result = Sing.query.filter_by(id=id).first()
    elif tablename == "eshow":
        result = eShow.query.filter_by(id=id).first()
    elif tablename == "sport":
        result = Sport.query.filter_by(id=id).first()
    elif tablename == "news":
        result = News.query.filter_by(id=id).first()
    elif tablename == "weather":
        result = Weather.query.filter_by(id=id).first()
    db.session.delete(result)
    db.session.commit()
    message = {"delmes": "ok"}
    return jsonify(message)


def to_json(result):
    temp = []
    if len(result) == 0:
        dict = {"message": "none"}
        return jsonify(dict)

    else:
        for x in result:
            temp.append(x.to_json())

        return jsonify(objects=temp)


# 删除爬虫数据
@login_required
@app.route('/deljson', methods=['GET'])
def delete_task():
    args = request.args.get('delete')
    print args
    try:
        result = Task.query.filter_by(id=args).first()
        db.session.delete(result)
        db.session.commit()
        # 定义删除成功后返回的命令
        # print '删除id为%s任务成功'%str(args)
        message = {"delmes": "ok"}
        return jsonify(message)

    except Exception as e:
        # print '删除id为%s任务失败'%str(args)
        message = {"delmes": "fail"}
        return jsonify(message)


# 钩子函数，上下文处理器
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}

    return {}


# 爬虫任务
def start_splider(id):
    # 获取爬虫配置信息
    args = id
    result = Task.query.filter_by(id=args).first()

    print '----------------线程爬虫已经启动-------------------'
    if result:
        type = ["演唱会类", "展会类", "时政类", "体育赛事类", "异常天气类"]
        types = list(result.types.split(","))

        for x in types:
            if type[int(x)] == "演唱会类":
                # 大麦网演唱会数据获取，多线程请运行class_damai_sing.py文件
                print '开始爬去大麦网演唱会数据'
                a = GetData('https://www.damai.cn/projectlist.do?mcid=1')  # 实例化对象，去捉取大麦网的数据
                pages = a.get_pages()
                for i in range(1, int(pages) + 1):
                    url = 'https://www.damai.cn/projectlist.do?mcid=1&pageindex=%d' % (i)
                    get_content(url)
                # 获取爱稻草的数据
                print '开始爬取爱稻草网'
                IdaocaoSing().get_idaocao()
            elif type[int(x)] == "展会类":
                # 展会类
                print '开始爬取e展网'
                # e展网
                a = Eshow('http://www.eshow365.com/')
            elif type[int(x)] == "时政类":
                # 新浪网
                # a = XiLangNews('http://news.sina.com.cn/china/')
                # # 新华网
                # a = XiHuaNews('http://www.news.cn/politics/')
                New().get_news()
            elif type[int(x)] == "体育赛事类":
                # 体育类
                # 大麦网
                print '开始爬取大麦网体育类数据'
                a = DamaiSport('https://s.damai.cn/ticket/sports.html', driver=webdriver.Chrome())
                # 228网
                print '开始爬去永乐票务的体育类数据'
                a = YongleSport('http://www.228.com.cn/category/tiyusaishi/')
            elif type[int(x)] == "异常天气类":
                # 天气类
                # 中国天气网
                a = TuFaWeather('http://www.weather.com.cn/alarm/#')
                # 修改爬虫状态

        # 修改爬虫状态
        result.status = 1
        db.session.commit()

    else:
        tell(1)


# 调用acquire([timeout])时，线程将一直阻塞，
# 直到获得锁定或者直到timeout秒后（timeout参数可选）。
# 返回是否获得锁。

# #新爬虫任务
# def taks(id):
#     # 获取爬虫配置信息
#     args = id
#     result = Task.query.filter_by(id=args).first()
#     print '----------------线程爬虫已经启动-------------------'
#     if result:
#         type = ["演唱会类", "展会类", "时政类", "体育赛事类", "异常天气类"]
#         types = list(result.types.split(","))
#         for x in types:
#             print "将爬取以下数据", type[int(x)]
#             for x in types:
#                 if type[int(x)] == "演唱会类":
#                     # 大麦网演唱会数据获取，多线程请运行class_damai_sing.py文件
#                     print '开始爬去大麦网演唱会数据'
#                     a = GetData('https://www.damai.cn/projectlist.do?mcid=1')  # 实例化对象，去捉取大麦网的数据
#                     pages = a.get_pages()
#                     for i in range(1, int(pages) + 1):
#                         url = 'https://www.damai.cn/projectlist.do?mcid=1&pageindex=%d' % (i)
#                         get_content(url)
#                     # 获取爱稻草的数据
#                     print '开始爬取爱稻草网'
#                     IdaocaoSing().get_idaocao()
#                 elif type[int(x)] == "展会类":
#                     # 展会类
#                     print '开始爬取e展网'
#                     # e展网
#                     a = Eshow('http://www.eshow365.com/')
#                 elif type[int(x)] == "时政类":
#                     #新浪网
#                     a = XiLangNews('http://news.sina.com.cn/china/')
#                     #新华网
#                     a = XiHuaNews('http://www.news.cn/politics/')
#                 elif type[int(x)] == "体育赛事类":
#                     # 体育类
#                     # 大麦网
#                     print '开始爬取大麦网体育类数据'
#                     a = DamaiSport('https://s.damai.cn/ticket/sports.html', driver=webdriver.Chrome())
#                     # 228网
#                     print '开始爬去永乐票务的体育类数据'
#                     a = YongleSport('http://www.228.com.cn/category/tiyusaishi/')
#                 elif type[int(x)] == "异常天气类":
#                     # 天气类
#                     # 中国天气网
#                     a = Weathers('http://www.weather.com.cn/alarm/#')
#                     # 修改爬虫状态
#         result.status = 1
#         db.session.commit()
#     else:
#         tell(1)

# def Func_1(args, status):
#     global run
#     run = int(status)
#
#     while run:
#         print 'run的值是%s' % run
#         start_splider(args)
#         # taks(args)
#         lock.acquire()
#         lock.release()
#
#     print u"已退出"

#
# def Func_2(args):
#     print '打印协助线程的传过来的值%s' % args
#     lock.acquire()
#     global run
#     run = int(args)
#     lock.release()


# 启动线程
@login_required
@app.route('/start', methods=['GET'])
def start():
    args = request.args.get('id')
    status = request.args.get('status')
    global ids
    # t = threading.Thread(target=Func_1, args=(args, status))
    # t.start()
    ids = args
    if not any(list_t):
        t = Thread2()
        t.start()
        list_t.append(t)
    elif not list_t[0].isAlive():
        print "开启新的线程"
        del list_t[0]
        t = Thread2()
        t.start()
        list_t.append(t)
    return jsonify({"startmess": "ok"})


# 启动分析任务的爬虫
@login_required
@app.route('/starts', methods=['GET'])
def starts():
    args = request.args.get('id')
    from analyse_data_task import taks
    taks(args)


# 停止爬虫线程
@login_required
@app.route('/stop', methods=['GET'])
def stop_threading():
    print '调用停止线程的方法----------'
    args = request.args.get('status')
    # global run
    # run = int(args)
    # t = threading.Thread(target=Func_2, args=(args,))
    # t.start()
    print '-------stop---------'
    print list_t
    if list_t:
        t = list_t[0]
        print t
        _async_raise(t.ident, SystemExit)
    else:
        print '线程未开启'
    return jsonify({"stopmess": "ok"})


# 爬虫信息告知
def tell(status):
    if status == 0:
        message = {"startmess": "ok"}
        print '爬虫成功启动了'
        return jsonify(message)
    else:
        message = {"startmess": "fail"}
        print '爬虫启动失败'
        return jsonify(message)


# 删除指定id的爬虫
def aps_date(id):
    scheduler.remove_job(id)
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "删除id为", id, "的爬虫"


# 暂停爬虫
@login_required
@app.route('/pause')
def pau():
    id = request.args.get('id')
    scheduler.pause_job(id)


# 恢复爬虫
@login_required
@app.route('/restart')
def restart():
    id = request.args.get('id')
    scheduler.resume_job(id)


# 添加定时爬虫
@login_required
@app.route('/adding', methods=['POST'])
def addjob():
    id = request.form.get('task_name')  # 爬虫名字
    time = request.form.get('task_time')  # 时间
    type = request.form.get('splider_type')  # 爬虫类型
    types = request.form.get('select_type')  # 爬虫任务
    # 将配置信息写入数据库
    task = Task(name=id, time=time, types=types, type=type, status=0)
    db.session.add(task)
    db.session.commit()
    print "爬虫名是", id
    print "爬虫时间是", time
    print "爬虫类型是", type
    print "爬虫任务是", types

@login_required
@app.route('/startings', methods=['GET'])
def startjobs():
    id = request.args.get('id')
    print '获得启动定时任务传过来的id', id
    # 查询数据库，获取爬虫的配置信息
    result = Task.query.filter_by(id=id).first()
    if result:
        from analyse_data_task import taks
        # 获得爬虫的任务及启动时间
        time = result.time
        print time
        # 将爬虫添加到任务队列
        scheduler.add_job(func=taks, args=(id,), next_run_time=time, id=id)
        print '任务添加成功'
        # 启动
        scheduler.start()
        return jsonify({"startmess": "ok"})


@login_required
@app.route('/starting', methods=['GET'])
def startjob():
    id = request.args.get('id')
    print '获得启动定时任务传过来的id', id
    # 查询数据库，获取爬虫的配置信息
    result = Task.query.filter_by(id=id).first()
    if result:
        # 获得爬虫的任务及启动时间
        time = result.time
        print time
        # 将爬虫添加到任务队列
        scheduler.add_job(func=start_splider, args=(id,), next_run_time=time, id=id)
        print '任务添加成功'
        # 启动
        scheduler.start()
        return jsonify({"startmess": "ok"})


# 启动频率爬虫
@login_required
@app.route('/addfre', methods=['GET'])
def start_j():
    id = request.args.get('id')
    print '获得启动定时任务传过来的id', id
    # 查询数据库，获取爬虫的配置信息
    result = Task.query.filter_by(id=id).first()
    if result:
        # 获得爬虫的任务及启动时间
        fre = result.fre
        print fre
        # 将频率爬虫添加到任务队列
        scheduler.add_job(func=start_splider, args=(id,), id=id, trigger='interval', hours=fre)
        print '任务添加成功'
        # 启动
        scheduler.start()
        return jsonify({"startmess": "ok"})


# 删除定时爬虫
@login_required
@app.route('/deling', methods=['GET'])
def deljob():
    id = request.args.get('id')
    aps_date(id)
    return jsonify({"message": "ok"})


# 查看任务队列
@login_required
@app.route('/spliderqueueshow', methods=['GET'])
def showQueue():
    # 简单返回任务的个数
    splider_list = []
    for x in scheduler.get_jobs():
        print '打印队列id-----'
        splider_list.append(x.id)
    dict = {"splider": splider_list}
    return jsonify(dict)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    app.run(host='0.0.0.0', threaded=True)
