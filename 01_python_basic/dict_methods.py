# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-08 7:17
@Project  :   Hands-on Crawler with Python-dict_methods
字典的方法：
{'China': 'Beijing', 'Russia': 'Moscow', 'Brazil': 'Brasilia'}
{'China': 'Beijing', 'Russia': 'Moscow', 'Brazil': 'Brasilia'}
2423953513408 2423953513664
True False
China
Russia
Brazil

Beijing
Moscow
Brasilia

China Beijing
Russia Moscow
Brazil Brasilia

Brasilia
{} {'China': 'Beijing', 'Russia': 'Moscow', 'Brazil': 'Brasilia'}
'''

# 定义字典
country_capitals = {'China': 'Beijing', 'Russia': 'Moscow', 'Brazil': 'Brasilia'}
print(country_capitals)

# 1.copy方法
cc = country_capitals.copy()  # 浅拷贝：深拷贝父对象（一级目录），子对象（二级目录）不拷贝（浅拷贝）、还是引用
print(cc)
print(id(country_capitals), id(cc))  # 深拷贝父对象，所以id不同

# 2.in关键字
print('China' in country_capitals, 'India' in country_capitals)

# 3.keys方法
for country in country_capitals.keys():
    print(country)
print()

# 4.values方法
for capital in country_capitals.values():
    print(capital)
print()

# 5.items方法
for country, capital in country_capitals.items():
    print(country, capital)
print()

# 6.pop方法
capital = country_capitals.pop('Brazil')
print(capital)

# 7.clear方法
country_capitals.clear()
print(country_capitals, cc)  # 深拷贝父对象，所以country_capitals发生改变、而cc不变
