# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-08 21:21
@Project  :   Hands-on Crawler with Python-copy_deepcopy
Python中的浅拷贝与深拷贝：
2240917146240 ['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic']]
2240917146240 ['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic']]
2240917151616 ['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic']]
2240917144448 ['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic']]

['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic'], 'Oceania']
['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic'], 'Oceania']
['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic']]
['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic']]

['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic', 'Indian Ocean'], 'Oceania']
['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic', 'Indian Ocean'], 'Oceania']
['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic', 'Indian Ocean']]
['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic']]
'''

import copy

l1 = ['Asia', 'Europe', 'Africa', ['Pacific', 'Atlantic']]
print(id(l1), l1)

l2 = l1  # 赋值引用：是对象的引用（别名）
print(id(l2), l2)  # 与l1的id相同

l3 = l1.copy()  # 等价于l3 = copy.copy(l1)，浅拷贝：l1和l3是独立的对象，但它们的子对象还是指向统一对象（是引用），拷贝程度较浅
print(id(l3), l3)

l4 = copy.deepcopy(l1)  # 深拷贝：l4完全拷贝了l1的父对象及其子对象，两者是完全独立的，拷贝程度较深
print(id(l4), l4)
print()

# 操作父对象
l1.append('Oceania')
print(l1)
print(l2)  # l2与l1指向同一对象，因此l2也发生改变
print(l3)  # l3为浅拷贝得到的独立父对象，因此不发生改变
print(l4)  # l4为深拷贝得到的独立父对象，因此不发生改变
print()

# 操作子对象
l1[3].append('Indian Ocean')
print(l1)
print(l2)  # l2与l1指向同一对象，因此l2也发生改变
print(l3)  # l3浅拷贝得到的子对象与l1相同，因此也发生改变
print(l4)  # l4深拷贝得到的独立子对象，因此不发生改变
