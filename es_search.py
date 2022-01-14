# encoding=utf-8
import jieba
import math
from collections import Counter


class Es_search():
    def __init__(self, path, is_bm=True):
        self.stop_words = self.read_txt(path)
        self.is_bm = is_bm   # 支持tf_idf、bm25
        self.index_doc = {}
        self.invert_index = {}
        self.idf = {}
        self.bm_idf = {}
        self.docs_len = {}
        self.docs_total_len = 0
        self.docs_avg_len = 0
        self.docs_nums = 0
        self.k1 = 1.5
        self.k2 = 0.25
        self.b = 0.75

    def read_txt(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return [w.strip() for w in file.readlines() if w.strip()]

    def make_invert_dic(self, docs_lis):
        self.docs_nums = len(docs_lis)
        self.index_doc = {index: doc for index, doc in enumerate(docs_lis)}
        for index, doc in enumerate(docs_lis):
            words_lis = [str(word).strip() for word in jieba.cut_for_search(doc) if str(word).strip() not in self.stop_words]
            self.docs_len[index] = len(words_lis)
            self.docs_total_len += len(words_lis)
            for word in words_lis:
                if word in self.invert_index:
                    if index not in self.invert_index[word]:
                        self.invert_index[word][index] = 0
                    self.invert_index[word][index] += 1
                else:
                    self.invert_index[word] = {index: 1}

        self.docs_avg_len = self.docs_total_len / self.docs_nums
        for word in self.invert_index:
            if self.is_bm:
                self.bm_idf[word] = math.log(1 + (self.docs_nums - len(self.invert_index[word]) + 0.5) / (len(self.invert_index[word]) + 0.5))
            else:
                self.idf[word] = math.log(1 + self.docs_nums / len(self.invert_index[word]))

    def search(self, query, num):
        sorted_score = {}
        words_lis = [str(word).strip() for word in jieba.cut_for_search(query) if str(word).strip() not in self.stop_words]
        word_fre = {word: fre for word, fre in Counter(words_lis).items()}
        print(word_fre)
        for word in word_fre:
            if word in self.invert_index:
                for index, fre in self.invert_index[word].items():
                    if self.is_bm:
                        len_punish = self.k1 * (1 - self.b + self.b * self.docs_len[index] / self.docs_avg_len)
                        fre_punish = fre * (self.k1 + 1) / (fre + len_punish)
                        query_punish = word_fre[word] * (self.k2 + 1) / (word_fre[word] + self.k2)
                        if index not in sorted_score:
                            sorted_score[index] = 0
                        sorted_score[index] += math.log(len_punish * fre_punish * query_punish) * self.bm_idf[word]
                    else:
                        tf_idf = math.log(1 + fre / self.docs_len[index]) * self.idf[word]
                        if index not in sorted_score:
                            sorted_score[index] = 0
                        sorted_score[index] += tf_idf
        sorted_score = sorted(sorted_score.items(), key=lambda x: -x[1])[:int(num)]
        sorted_res = [(self.index_doc[index], round(score, 2)) for index, score in sorted_score]
        return sorted_res


if __name__ == '__main__':
    lis = ['利用网络爬虫技术','文档倒排索引技术','向量空间模型技术','检索排序技术','编写一个搜索引擎系统']
    es = Es_search('stopword.txt', )
    es.make_invert_dic(lis)
    res = es.search('倒排索引网络爬虫技术', 3)
    print(res)
