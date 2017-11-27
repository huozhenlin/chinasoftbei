---
date: 2017-06-21 14:45
status: draft
title: 基于互联网大数据的事件智能抓取和画像
---

# 大数据智能抓取和画像系统

- **项目简要介绍**
    
&emsp;&emsp;《大数据智能抓取和画像系统》是集互联网大数据事件爬取、事件属性提取和画像、可视化等功能于一体互联网软件。本软件能够自动爬取会议、展会、体育赛事、演唱会、突发异常天气等网站新闻，实现事件去重功能。本软件采用的技术有：网络爬虫、正文提取、分词、去重、生成语法树、语法树剪枝、大数据可视化、数据库、网页编程等。采用的编写语言为Python、Javascript和PHP。Python主要用于爬取分析存储数据，PHP用于实现事件的可视化。  
&emsp;&emsp;本项目使用的Python库有：`selenium`，`re`，`beautifulsoup`，`requests`，`newspaper`，`mysqldb`，`ltp`，`simhash`等。项目涉及到的Python库以及语料库资源均为开源免费。除此之外，为了利用海量的网络大数据，我们在实现相关功能时使用了免费的网络大数据资源。使用到的网络免费的网络资源有：百度搜索，百度指数，百度地图、百度新闻、百度Echarts。  

- **开发语言**
    
        1. Python(数据挖掘和分析)
       
        2. PHP(后台语言)

- **演示**
    ![演示视频1](http://qwe.cherwb.cn/data/demo.mp4)
    
    <iframe height=498 width=510 src="http://qwe.cherwb.cn/data/demo.mp4">
	
	![演示视频2](http://www.sinaegg.cn/demoshow.mp4)
	<iframe height=498 width=510 src="http://www.sinaegg.cn/demoshow.mp4">

-  **数据可视化地址**
    
    <http://123.207.88.152/softbei/visual/>

-  **软件体验方法**

	本项目已经部署于腾讯云远程桌面，利用windows自带的“远程桌面连接”软件即可登录。打开pycharm,运行下面两个文件即可。
	> `main_grab_data.py`数据爬取类
	`main_analyse_data.py`数据分析类

    IP：123.207.88.152
    
    Account：Administrator
    
    Password：Chinasoftbei123.
## 软件使用前准备工作

- **python版本号**(v2.7)

- **自动化测试驱动**(选其一，根据实际情况修改代码中的驱动调用即可)
        
        1.Chrome
        
        2.PhantomJS
>   例子:

    `driver=webdriver.PhantomJS`
  
- **主要使用到的框架，模块，请前往对应官网下载**

    | 模块 | 用途 |
    | -------- | -------- |
    | requests   | 进行网络请求   |
    | BeautifulSoup   | 将网页源代码生成树状结构，便于抽取想要的内容   |
    | selenium        |      自动化测试工具，用于请求网页中使用ajax技术调用的数据|
    | re        |     通过正则表达式匹配想要获取的内容|
    | echart|用于数据可视化|
    | pyltp|自然语言处理，分词用到|
    | pandas|数据处理|
    | Simhash|利用simhash，海明距离对重复事件去重|

    >   注意:

    分词模型采用本地化分词，[点击下载](http://pan.baidu.com/s/1hsceROC),导入方式如下

    ```python
    from pyltp import Segmentor
    segmentor = Segmentor()
    segmentor.load(r'C:\Users\hzl\PycharmProjects\untitled\chinasoftbei\analyse\ltp_data                \cws.model')  # 分句模型
    ```

## 特性和功能
1. **事件去重**
2. **准确的关键字提取**
3. **事件属性自动化提取**(包含时间，地点，影响人群，影响区域，主办方级别)
4. **简洁明了的可视化界面**
5. **丰富的事件来源**(爬取了发布事件的主流网站)
6. **事件标记**(由于每天都会从网络获取数据，对已分析过的数据会添加标记，下次分析时会直接从数据库中取出未分析的数据进行数据分析)
7. **定时爬取**(用户可根据自己需要，自定义数据爬取频率)
8. **良好的代码健壮性**(网络操作往往会发生大量异常，比如说某个数据请求不到等等，我们通过大量实验，逐步增强了代码健壮性)

## 软件安装及使用及注意事项
-   使用`git clone http://42.123.127.93:10080/huozhenlin/code.git`下载代码包
-   使用Pycharm导入代码包，选择对应的代码文件运行实现相应功能（具体文件功能请参考代码说明文档）
-   运行网络爬虫请保持良好的网络环境
-   若需要本地运行数据可视化前端代码，请配置好数据库，php环境，运行softbei/visual/index.php文件即可
-   更多帮助请参考源代码说明项目中的说明文档

## 未来计划
-   多线程支持，爬取爱稻草网数据我们实验性使用了多线程技术，爬取效率明显提升
-   覆盖更多的数据来源网站，分析事件对民航相关数据的影响
-   优化算法，提升数据分析能力
-   使用更多形式来数据可视化，让数据表现更直观易懂
-   前端可视化数据支持excel导出 

## 鸣谢
**尊敬的评委老师**，您辛苦了！

**Echarts**，一款js绘图工具包，数据可视化主要使用到了该开源工具包

**百度指数**，百度指数提供了判断事件影响人群的核心数据

**程序中使用到的python其它开源库**
