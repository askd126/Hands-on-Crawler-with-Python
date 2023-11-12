# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-07 7:24
@Project  :   Hands-on Crawler with Python-list_methods
列表的常用方法：
['apple', 'pear', 'orange']
['apple', 'pear', 'orange', 'banana']
['apple', 'pear', 'orange', 'banana', 'lemon', 'pear']
2
3
['apple', 'pear', 'orange', 'mango', 'banana', 'lemon', 'pear']
['apple', 'orange', 'mango', 'banana', 'lemon', 'pear']
pear
5
'''

fruits = ['apple', 'pear', 'orange']
print(fruits)

# 1.append方法
fruits.append('banana')
print(fruits)

# 2.extend方法
fruits.extend(['lemon', 'pear'])
print(fruits)

# 3.count方法
print(fruits.count('pear'))

# 4.index方法
print(fruits.index('banana'))

# 5.insert方法
fruits.insert(3, 'mango')
print(fruits)

# 6.remove方法
fruits.remove('pear')
print(fruits)

# 7.pop方法
res = fruits.pop()
print(res)

# 8.len函数
print(len(fruits))
