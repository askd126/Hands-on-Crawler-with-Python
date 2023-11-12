# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-06 7:48
@Project  :   Hands-on Crawler with Python-random_str
生成指定长度随机字符串：
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
['T', 'r', 'a', 'x', 'F', '8', 'S', 'M', 'J', 'O', 'j', '1', 'n', 'K', 'G']
TraxF8SMJOj1nKG
'''

import random
import string

length = 15  # 随机字符串长度

letters_digits = string.ascii_letters + string.digits  # 所有的字母和数字
print(letters_digits)

new_string = random.sample(letters_digits, length)  # 指定长度的随机字符列表
print(new_string)

new_string = ''.join(new_string)  # 将列表转为字符串
print(new_string)
