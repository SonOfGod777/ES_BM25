1、基于倒排索引、bm25/tfidf搭建简洁的搜索引擎；

2、对比依赖包genism中的bm25算法：
a:分别搭建基于bm25和tfidf的搜索引擎，可选择；
b:增加jieba分词：gensim--bm25算法源码中无jieba分词，对文本是逐字遍历；故想用词语创建bm25算法，只能修改源码；
c:增加单词和query的相关性：bm25算法中包含3部分：单词权重(idf)、单词和文档的相关性、单词和query的相关性；
但gensim--bm25算法源码中无单词和query的相关性；






