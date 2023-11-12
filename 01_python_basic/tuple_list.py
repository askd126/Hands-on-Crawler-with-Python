# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-07 21:29
@Project  :   Hands-on Crawler with Python-tuple_list
元组与列表的区别：
['China', 'Russia', 'South Africa', 'India', 'Brazil']
2621422436672
['China', 'Russia', 'RSA', 'India', 'Brazil']
2621422436672

('China', 'Russia', 'South Africa', 'India', 'Brazil')
2621422342032
2621422342032
2621421951472
'''

# 1.列表
# 创建列表
l = ['China', 'Russia', 'South Africa', 'India', 'Brazil']
print(l)

# 查看列表内存id
print(id(l))

# 修改列表元素
l[2] = 'RSA'
print(l)

# 再次查看列表内存id
print(id(l))  # id未改变
print()

# 2.元组
# 创建元组
t = ('China', 'Russia', 'South Africa', 'India', 'Brazil')
print(t)

# 查看元组内存id
print(id(t))

# t[2] = 'RSA' # 元组元素无法改变，报错TypeError: 'tuple' object does not support item assignment
t2 = t  # t2和t指向相同的元组对象
print(id(t2))  # id与t相同

t2 = ('PRC', 'RUS', 'RSA', 'IND', 'BRA')  # t2指向的元组对象发生改变
print(id(t2))  # id也相应改变
