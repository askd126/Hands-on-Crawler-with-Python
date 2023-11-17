# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-10 7:17
@Project  :   Hands-on Crawler with Python-word_counter
词频统计器
'''

# 导入所需的库
from collections import Counter

import jieba

stopwords = ['的', '了', '就', '在', '', '，', '。', '、', '“', '”', '\n']  # 停用词，过滤高频且无意义的词
top_k = 20  # 返回前k个词及词频


# 1.读取文本
# 定义函数
def fead_file(file_path):
    with open(file_path, encoding='utf-8') as f:
        return f.read()


# 调用函数读取文件内容
content = fead_file('../data/news.txt')

# 2.进行分词
words = jieba.cut(content)
words = filter(lambda w: w not in stopwords, words)  # filter高阶函数过滤停用词

# 3.统计词语次数
counter = Counter(words)
total_count = len(counter)
print(f'Total word count: {total_count}')

# 4.排序：根据词频倒序排序
counter_sorted = sorted(counter.items(), key=lambda item: item[1], reverse=True)

# 5.计算并输出top_k词频
for word, count in counter_sorted[:top_k]:
    print(f'word freq of {word} is {count / total_count:.6f}')
