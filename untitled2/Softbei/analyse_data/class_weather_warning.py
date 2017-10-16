#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pyltp import *
import pandas as pd
from Softbei.analyse_data.class_weather_warning_level import Weather_Wanring_Level

reload(sys)
sys.setdefaultencoding('utf8')

places = []

class WeatherWarning:
    def get_att_obj(self, words, arcs, target):
        l_list = list(words)#分词好的句子转换为list
        if target not in l_list:
            return ''
        result = ""
        head = []
        relation = []
        for i in arcs:
            head.append(i.head)
            relation.append(i.relation)
        index = l_list.index(target)
        # print index#预警的下标是6
        result = result + target#刚开始是result为预警
        while index in head:
            simliar = self.find_all_index(list(head),index)
            for index in simliar:
                result = l_list[index] + result
                simliar = self.find_all_index(list(head), index)
                simliar.reverse()
                for index in simliar:
                    result=l_list[index] + result
        return result


    def find_all_index(self, arr, item):
        return [i for i, a in enumerate(arr) if a == item]

    # 分句，也就是将一片文本分割为独立的句子
    def sentence_splitter(self, sentence):
        sents = SentenceSplitter.split(sentence)  # 分句
        # print '\n'.join(sents)


    # 角色标注
    def role_label(self, words, postags, netags, arcs):
        labeller = SementicRoleLabeller()  # 初始化实例
        labeller.load(r'C:\BaiduNetdiskDownload\ltp_data\srl')  # 加载模型
        roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
        # for role in roles:
        #     print role.index, "".join(
        #         ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
        labeller.release()  # 释放模型

    # 命名实体识别
    def ner(self, words, postags):
        recognizer = NamedEntityRecognizer()  # 初始化实例
        recognizer.load(r'C:\BaiduNetdiskDownload\ltp_data\ner.model')  # 加载模型
        netags = recognizer.recognize(words, postags)  # 命名实体识别
        # print netags
        place=''
        for word, ntag in zip(words, netags):
            # pass
            # print word + '/' + ntag
            if(ntag.find('Ns')!=-1):
                place+=word
        # 地点
        print place
        places.append(place)
        recognizer.release()  # 释放模型
        return netags

    def get_level(self, types):
        # C: / untitled2 / getData / Softbei /
        # df = pd.read_csv('../../csv/weather.csv')
        csv_name='C:/untitled2/Softbei/removal_csv/csv/%s.csv'%(types)
        df=pd.read_csv(csv_name)
        title=list(df['标题'])
        tag=df['标记']
        segmentor = Segmentor()
        posttagger = Postagger()
        parser = Parser()
        segmentor.load(r'C:\BaiduNetdiskDownload\ltp_data\cws.model')
        posttagger.load(r'C:\BaiduNetdiskDownload\ltp_data\pos.model')
        parser.load(r"C:\BaiduNetdiskDownload\ltp_data\parser.model")
        target='预警'
        levels = []

        #index为下标，j为标记数
        for index,j in enumerate(tag):
            if(j == 1):
                continue
            else:
                title_non_repeat=title[index]

                self.sentence_splitter(title_non_repeat)
                words = segmentor.segment(title_non_repeat)
                postags = posttagger.postag(words)

                for word, postag in zip(words, postags):
                    print word + "/" + postag

                arcs = parser.parse(words, postags)
                arclen = len(arcs)
                conll = ""
                for i in xrange(arclen):
                    if arcs[i].head == 0:
                        arcs[i].relation = "ROOT"
                    # 累加后逐个打印
                    conll += "\t" + words[i] + "(" + postags[i] + ")" \
                             + "\t" + postags[i] + "\t" + str(arcs[i].head) + "\t" + arcs[i].relation + "\n"

                # print conll

                netags = self.ner(words, postags)
                self.role_label(words, postags, netags, arcs)
                # result为xxx预警
                result = self.get_att_obj(words, arcs, target)
                print result
                level = Weather_Wanring_Level().weather_warning(result)
                levels.append(level)
                print '----------------------------------------------------------------------------------------'

        return levels


    def weather_part_csv(self, places, types):
        # 天气预警
        levels=self.get_level(types)
        # print level
        # print places
        if (len(levels) == 0):
            return 'null'

        dict={

            u'天气预警等级': levels, u'地点': places
            # levels, places
        }

        return dict


    def main_weather_warning(self, types):
        # C: / untitled2 / getData / Softbei /
        # file_name = '../common/csv/weather/weather_warining_level.csv'
        file_name = 'C:/untitled2/Softbei/analyse_data/common/csv/weather/weather_warining_level.csv'
        print file_name
        dict=self.weather_part_csv(places , types)
        print dict
        if(dict=='null'):
            print '没有可生成的数据'
        else:
            pd.DataFrame(dict).to_csv(file_name, encoding='utf8', index=None )
        print '-------------------------------*********************-------------------------------------'


if __name__ == '__main__':
    # main_weather_warning()
    WeatherWarning().main_weather_warning(types='weather')

