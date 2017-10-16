#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from pyltp import *
import nltk
import pandas as pd
from nltk.tree import Tree
from nltk.grammar import DependencyGrammar
from nltk.parse import *
import re
from gensim.models import word2vec
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
from Softbei.common.class_database import DB

reload(sys)
sys.setdefaultencoding('utf8')
c = DB()
# 分词
segmentor = Segmentor()
segmentor.load('C:\BaiduNetdiskDownload\ltp_data\cws.model')
posttagger = Postagger()
# 词性标注
posttagger.load('C:\BaiduNetdiskDownload\ltp_data\pos.model')
# 语法依存树分析
parser = Parser()
parser.load("C:\BaiduNetdiskDownload\ltp_data\parser.model")

recognizer = NamedEntityRecognizer()  # 初始化实例
recognizer.load('C:\BaiduNetdiskDownload\ltp_data\er.model')  # 加载模型

labeller = SementicRoleLabeller()  # 初始化实例
labeller.load('C:\BaiduNetdiskDownload\ltp_data\srl')  # 加载模型
s = '峰会'
words = ['举行', '召开', '开幕', '举办']


def judge_words(index,sentsence):
    a = words[index] in sentsence
    return a


class NewsItplearning:
    # 分句，也就是将一片文本分割为独立的句子
    def sentence_splitter(self, sentence):
        sents = SentenceSplitter.split(sentence)  # 分句
        # print '\n'.join(sents)
        return sents

    # 角色标注
    def role_label(self, words, postags, netags, arcs):
        roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
        for role in roles:
            print role.index, "".join(
                ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
        labeller.release()  # 释放模型

    # 命名实体识别
    def ner(self, words, postags):
        netags = recognizer.recognize(words, postags)  # 命名实体识别
        for word, ntag in zip(words, netags):
            print word + '/' + ntag
        recognizer.release()  # 释放模型
        return netags

    def get_tree_by_index(self, arcs, indexes, root_index):
        indexes.append(root_index)
        for index, val in enumerate(arcs):
            if val.head == root_index + 1:
                self.get_tree_by_index(arcs, indexes, index)

    def coreference_resolution(self, words, arcs, name, obj_index):
        indexes = []
        print name[0]
        for i in range(len(words)):
            if i != obj_index and words[i] == words[name[0]]:
                indexes.append(i)

        if len(indexes) != 0:
            distance = []
            for i in indexes:
                distance.append(abs(i - obj_index))
            k = np.argmin(distance)
            indexes_return = []
            self.get_tree_by_index(arcs, indexes_return, indexes[k])
            return indexes_return
        else:
            return None

    # 属性获取
    def get_tree(self, words, arcs, postags, root_string, count):
        print count
        url_titles = c.select_news_info(value='url_title') #url_titles为 news表url_title的list集合
        p = url_titles[count]
        print p
        print '-----------------------hello----------------------------'
        root_index = -1
        relation = ''
        # 获取相应关键字的子树（如“召开”，“举行”）
        for i in xrange(len(words)):
            if words[i] == root_string:
                root_index = i
                relation = arcs[i].relation

        print relation
        if root_index == -1 or (not relation == 'COO' and not relation == 'ROOT'):
            return None
        else:
            print '111111111'
            print root_index

        # 得到相应关键词子树
        indexes = []
        # 得到子树
        self.get_tree_by_index(arcs, indexes, root_index)
        print root_index
        indexes.sort()
        print indexes
        for m in indexes:
            print words[m]
        # 移除COO子树
        self.remove_coo(arcs, indexes, root_index)
        # 获取会议名称
        obj_index, name = self.get_fob_sbv(arcs, indexes, root_index)
        title = ""
        if not name is None:
            # if len(name) == 1:
            #     # 尝试指代消解
            #     name_new = coreference_resolution(words, arcs, name, obj_index)
            #     if not name_new is None:
            #         name = name_new
            words_to_remove = ["主办", "承办", "举办"]
            print 'name-------------------?????????????????????????'
            # 移除主办方信息
            self.remove_tree_by_word(words, arcs, name, obj_index, words_to_remove)
            for m in name:
                print words[m]
                title += words[m]
            title = title.strip("“”")
            print title
            print '============================='
        else:
            # print name
            title = 'null'
            print '============================='
            print "没有获得会议名称"

        # 获取时间信息（带有nt词汇的adv子树）
        date = self.get_adv(arcs, indexes, postags, root_index, 'nt')
        time = ""
        # print date
        if not date is None:
            # 移除介词
            self.remove_preposition(date, postags)
            for m in date:
                print words[m]
                time += words[m]
            print time
            time = time.strip("，,")
            print time
            print '============================='
        else:
            # print date
            time = "null"
            print '============================='
            print "没有获得时间"
        # 获取时间信息（带有ns词汇或j词汇的adv子树）
        location = self.get_adv(arcs, indexes, postags, root_index, 'ns')
        # print location
        place = ""
        if location is None:
            location = self.get_adv(arcs, indexes, postags, root_index, 'j')
        # print '?????????????????????????????'
        if not location is None:
            # 移除介词
            self.remove_preposition(location, postags)
            for m in location:
                print words[m]
                place += words[m]
            print place
            print '============================='
            print time, title, place, p
            if time == "null":
                c.update_news_notime(title=title, place=place, url_title=p)
            else:
                c.update_part_news(start_time=time, title=title, place=place, url_title=p)
            return indexes
        else:
            # print location
            place = 'null'
            print '============================='
            print "没有获得地点"
            print time, title, place, p
            if time == "null":
                c.update_news_notime(title=title, place=place, url_title=p)
            else:
                c.update_part_news(start_time=time, title=title, place=place, url_title=p)

    def get_element(self, arcs, indexes, root_index, relation):
        list_indexes = []
        for index, val in enumerate(arcs):
            if val.head == root_index + 1 and index in indexes and val.relation == relation:
                tmp_indexes = []
                self.get_tree_by_index(arcs, tmp_indexes, index)
                tmp_indexes.sort()
                list_indexes.append(tmp_indexes)
        if len(list_indexes) == 0:
            return None
        else:
            print list_indexes
            return list_indexes

    def get_fob_sbv(self, arcs, indexes, root_index):
        print "会议："
        obj_index = 0
        tmp = self.get_element(arcs, indexes, root_index, 'SBV')
        if tmp is None:
            tmp = self.get_element(arcs, indexes, root_index, 'FOB')
        if tmp is None:
            return None
        else:
            distance = []
            for i in tmp:
                distance.append(abs(root_index - np.mean(i)))
            k = np.argmin(distance)
            for i in tmp[k]:
                if arcs[i].relation == 'SBV' or arcs[i].relation == 'FOB':
                    obj_index = i
            return obj_index, tmp[k]

    def get_time(self, word, data):
        for i in data:
            for m in i:
                if not word[m].find('日') == -1:
                    return i

    def get_adv(self, arcs, indexes, postags, root_index, pos):
        print
        print pos
        result = []
        tmp = self.get_element(arcs, indexes, root_index, 'ADV')
        if len(tmp) == 0:
            return None
        for i in tmp:
            for m in i:
                if postags[m] == pos:
                    result.append(i)

        if len(result) == 0:
            return None
        else:
            distance = []
            for i in result:
                distance.append(abs(root_index - np.mean(i)))
            k = np.argmin(distance)
            return result[k]

    def remove_preposition(self, indexes, postags):
        for i in indexes:
            if postags[i] == 'p':
                indexes.remove(i)

    def remove_tree_by_index(self, arcs, indexes, delete_root_index):
        coo_indexes = []
        indexes_t = []
        self.get_tree_by_index(arcs, indexes_t, delete_root_index)
        coo_indexes.extend(indexes_t)
        coo_indexes = set(coo_indexes)

        for i in coo_indexes:
            indexes.remove(i)

    def remove_tree_by_word(self, words, arcs, indexes, root_index, word):
        word_index = []

        for index, val in enumerate(arcs):
            if index in indexes and words[index] in word:
                if val.head == root_index + 1:
                    word_index.append(index)
                else:
                    word_index.append(val.head - 1)

        for i in word_index:
            self.remove_tree_by_index(arcs, indexes, i)

    def remove_coo(self, arcs, indexes, root_index):
        coo_index = []
        for index, val in enumerate(arcs):
            if val.head == root_index + 1 and index in indexes and val.relation == 'COO':
                coo_index.append(index)

        for i in coo_index:
            self.remove_tree_by_index(arcs, indexes, i)

    def main(self):
        # sentence = "由中国营销学会生态旅游度假养生分会、中国投资论坛组委会、中华生态旅游促进会联合主办的2017中国优秀旅游品牌推广峰会暨旅游投融资洽谈会6月18日在北京隆重召开。"
        # sentence = "2017年夏季达沃斯论坛新领军者年会将于6月27日至29日在大连举行，目前共有来自80多个国家的超过2000位政、商、学、文等各界领袖注册参会。本次会议主题为“在第四次工业革命中实现包容性增长”。"
        # sentence = "2017年亚洲媒体峰会6月6日在青岛举行，中共中央政治局委员、国务院副总理刘延东出席开幕式并致辞，强调要强化媒体责任，促进媒体合作，为落实联合国2030年可持续发展议程、构建人类命运共同体注入更多“正能量”。"
        # sentence = "记者从杭州市人民政府今天举行的新闻发布会获悉，2017全球私募基金西湖峰会将于6月24日在杭州召开。"
        # sentence = "士研咨询将召集国内外专业机构共同举办2017亚太金融数据与信息峰会，峰会将于9月14 - 15日在北京盛大召开。"
        # sentence = "中青在线杭州6月22日电（实习生 管婷婷 中国青年报·中青在线记者 董碧水）记者从杭州市人民政府今天举行的新闻发布会获悉，2017全球私募基金西湖峰会将于6月24日在杭州召开。"
        # sentence = "光明网讯（记者齐柳明）8月23日, 2017腾讯“云+未来”峰会于北京正式召开。"
        # sentence = "“2017年中国马铃薯淀粉产业峰会暨中淀协马铃薯淀粉专委会三届三次理事会”在呼和浩特召开。"
        # sentence = "由中国出版协会、百道网、法国《书业周刊》（Livre Hebdo）、国际书业研究机构RWCC，和美国《出版商周刊》（Publisher’s Weekly）联合主办的“2017全球知识服务峰会”在北京召开。"
        # sentence = "中新网8月23日电  今日，腾讯“云+未来”峰会于北京正式召开。"
        # sentence = "黄河新闻网讯（记者侯津刚 贺亚奇）8月24日，第三届山西文博会主要活动之一——“开放的山西”主题峰会在中国（太原）煤炭交易中心举行。"
        # sentence = "8月22日，由开放数据中心委员会(ODCC)主办，百度、腾讯、阿里巴巴、中国电信、中国移动、中国信息通信研究院和英特尔承办的“2017开放数据中心峰会”在京召开。"
        # sentence = "山西文博会主要活动之一——“开放的山西”主题峰会8月24日举行，图为会议现场"
        # sentence = "人民网太原8月25日电（李梦文）8月24日，第三届山西文博会重点活动“开放的山西”主题峰会在中国（太原）煤炭交易中心举行"
        # sentence = "（原标题：国际干细胞与免疫治疗领导者峰会在昆明举行）记者龙舟云南网讯26日，2017国际干细胞与免疫治疗领导者峰会在昆明启幕"
        # sentence = "光明网讯（记者齐柳明）8月23日,2017腾讯“云+未来”峰会于北京正式召开"
        # 分句
        # content = ["环球网报道记者赵怡蓁 据法国媒体8月27日报道，非洲和欧洲多国领导将于法国当地时间8月28日聚集在巴黎，就移民问题召开小型峰会"]
        # print content
        # contents = ["原标题：厦门金砖国家峰会即将召开多家上市公司获益金砖国家领导人第九次会晤将于9月3日开始在厦门举办"]
        # contents = ["由中国工业合作协会、上海决策者经济顾问股份有限公司主办，上海市工业合作协会、园区大会组委会、决策者金融研究院协办的中国经营性不动产金融创新峰会(REF2017)将于11月在上海隆重开幕"]
        # contents = ["由中国工业经济联合会和中国机械工业集团有限公司共同主办的“2017中国机器人产业创新峰会”于8月27日在广州盛大开幕"]
        contents = c.select_news_info(value='contents')  #contents为list集合

        for count, i in enumerate(contents):
            # print count
            # print i
            # print type(i)
            sents = self.sentence_splitter(str(i)) #分句
            for i in sents:
                if s in i:
                    if judge_words(0, i) or judge_words(1, i) or judge_words(2, i) or judge_words(3, i):
                        # words = segmentor.segment(sents[0])
                        print '-------------------************************-------------------------------------------'
                        print i
                        words = segmentor.segment(i)
                        postags = posttagger.postag(words)
                        for word, postag in zip(words, postags):
                            print word + "/" + postag,

                        arcs = parser.parse(words, postags)
                        arclen = len(arcs)
                        conll = ""
                        for i in xrange(arclen):
                            if arcs[i].head == 0:
                                arcs[i].relation = "ROOT"
                            conll += "\t" + words[i] + "(" + arcs[i].relation + "_" + postags[i] + ")" \
                                     + "\t" + postags[i] + "\t" + str(arcs[i].head) + "\t" + arcs[i].relation + "\n"
                        print conll
                        # 属性获取

                        try:
                            if self.get_tree(words, arcs, postags, "举行", count) is None:
                                if self.get_tree(words, arcs, postags, "召开", count) is None:
                                    if self.get_tree(words, arcs, postags, "开幕", count) is None:
                                        if self.get_tree(words, arcs, postags, "举办", count):
                                            print '举办'
                        except Exception as e:
                            print '没有分析信息'

                        break
                        # conlltree = DependencyGraph(conll)
                        # tree = conlltree.tree()
                        # tree.draw()




if __name__ == '__main__':
    NewsItplearning().main()
