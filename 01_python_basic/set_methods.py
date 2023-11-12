# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-08 7:37
@Project  :   Hands-on Crawler with Python-set_methods
集合的方法：
{'Python', 'Go', 'Java'}
{'Python', 'Go', 'Java', 'C'}
{'Java', 'C', 'PHP', 'C++', 'Python', 'Go'}
{'Java', 'C', 'C++', 'Python', 'Go'}
{'Java', 'C', 'C++', 'Python', 'Go'}
Java
set()
['Python', 'Java', 'Go', 'PHP', 'Go', 'JavaScript', 'C', 'Go', 'Python', 'Java', 'C', 'C++']
['JavaScript', 'Java', 'C', 'PHP', 'C++', 'Python', 'Go']
{'Go', 'Java', 'Python'}
{'JavaScript', 'Java', 'C', 'PHP', 'C++', 'Python', 'Go'}
{'JavaScript', 'PHP'}
{'C++', 'JavaScript', 'C', 'PHP'}
'''

# 创建集合
langs = {'Python', 'Java', 'Go', 'Python'}
print(langs)  # 实现去重效果

# 1.add方法
langs.add('C')
print(langs)

# 2.update方法
langs.update(['Python', 'C++', 'PHP'])
print(langs)

# 3.remove方法
langs.remove('PHP')
print(langs)

# 4.discard方法
# langs.remove('PHP') # remove方法移除不存在的元素时，会报错KeyError: 'PHP'
langs.discard('PHP')  # discard方法移除不存在的元素时，不会报错
print(langs)

# 5.pop方法
res = langs.pop()
print(res)

# 6.clear方法
langs.clear()
print(langs)

# 7.利用集合给数据去重
langs = ['Python', 'Java', 'Go', 'PHP', 'Go', 'JavaScript', 'C', 'Go', 'Python', 'Java', 'C', 'C++']
print(langs)
langs = list(set(langs))
print(langs)  # 达到去重效果

# 8.集合操作
langs1 = {'Python', 'Java', 'Go', 'PHP', 'Go', 'JavaScript'}
langs2 = {'C', 'Go', 'Python', 'Java', 'C', 'C++'}
# 交集
print(langs1 & langs2)
# 并集
print(langs1 | langs2)
# 差集
print(langs1 - langs2)
# 对称差集
print(langs1 ^ langs2)
