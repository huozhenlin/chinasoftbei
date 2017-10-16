#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from Softbei.analyse_data.class_age import Age
from Softbei.analyse_data.class_age_tf_idf import TfIdf
from Softbei.analyse_data.class_getcity import GetCity
from Softbei.analyse_data.class_getzhuban import ZhuBan
from Softbei.analyse_data.class_history import History
from Softbei.analyse_data.class_hot import Hot


class Test1(unittest.TestCase):
    def setUp(self):
        self.tf=TfIdf()
        self.hot=Hot()
        self.age=Age()
        self.zhuban=ZhuBan()
        self.getcity=GetCity()
        self.history=History()


    def tearDown(self):
        self.tf=None
        self.age=None
        self.hot=None
        self.zhuban=None
        self.getcity=None
        self.history=None


    def test_get_num(self):
        dd=self.tf.get_num(self.tf.fenci("2017[A CLASSIC TOUR学友.经典] 世界巡回演唱会—西安站"))#五月天LIFE《人生无限公司》2017 MAYDAY LIFE TOUR-北京站
        self.assertEqual(dd,['CLASSIC','TOUR','学友.'])#['人生无限公司','五月天','MAYDAY','TOUR-','北京站']，热词缺少('人生无限公司','MAYDAY','TOUR-')


    def test_get_age(self):
        ss = self.tf.fenci("2017周杰伦世界巡回演唱会厦门站（10月22日场次）")  # ss 为 关键字的list列表  ['杰伦' ,'巡回' ,'厦门站', '22日', '场次']
        abc = self.age.get_age(ss[:2][0])
        a = [u'1', u' 1', u' 2', u' 1', u' 1']
        self.assertEqual(abc, a)


    def test_get_more(self):
        csv_name = 'C:/untitled2/Softbei/removal_csv/csv/%s.csv' % ('eshow')
        dict = self.age.getmore(csv_name)
        print dict
        self.assertDictEqual(dict, {u'\u4e3b\u8981\u5f71\u54cd\u5e74\u9f84\u5c42\u4e3a\u6210\u5e74': ['1'], u'\u4e3b\u8981\u5f71\u54cd\u5e74\u9f84\u5c42\u4e3a\u9752\u5e74': ['0'], u'\u4e3b\u8981\u5f71\u54cd\u5e74\u9f84\u5c42\u4e3a\u8001\u5e74': ['0'], u'\u4e3b\u8981\u5f71\u54cd\u5e74\u9f84\u5c42\u4e3a\u513f\u7ae5': ['0']})


    def test_zhuban(self):
        result = self.zhuban.judge_xiehui("中国对外贸易广州展览总公司")
        self.assertEqual(result,"国内行业协会")


    def test_getcity(self):
        csv_name = 'C:/untitled2/Softbei/removal_csv/csv/%s.csv' % ("sport")
        dict = GetCity().to_place_csv(csv_name)
        print type(dict)
        self.assertDictEqual(dict,{u'\u5730\u70b9': [u'\u5929\u6d25\u5e02']})
        #{"经度":39.0803858425,"纬度":117.179856782,"城市名":"天津市"}


    def test_history(self):
        value = History().get_history(csv_name='C:/untitled2/Softbei/removal_csv/csv/eshow.csv')
        self.assertEqual(value,[3])


if __name__ == "__main__":
    unittest.main()

