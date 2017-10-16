#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from Softbei.removal_csv.class_removal import Removal


class Test_a(unittest.TestCase):
    def setUp(self):
        removal=Removal()
    def tearDown(self):
        removal=None
    def test_drop_repet(self):
        self.before_csv_name = 'C:/untitled2/Softbei/to_csv/before_csv/before_test.csv'
        self.csv_name = 'C:/untitled2/Softbei/removal_csv/csv/test.csv'
        self.a=Removal().drop_repet(self.before_csv_name,'标题', self.csv_name)
        # pd.DataFrame(self.a).to_csv(self.csv_name, encoding='utf8', index=None)
        print self.a



if __name__=="__main__":
    unittest.main()

