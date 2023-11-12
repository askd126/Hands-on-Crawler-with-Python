# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-08 23:15
@Project  :   Hands-on Crawler with Python-exception
Python中的异常处理：
file random_str.py has 27 lines, file random_str.py processed
file list_methods.py has 51 lines, file list_methods.py processed
file tuple_list.py has 50 lines, file tuple_list.py processed
Can not open file copy_depcopy.py, file copy_depcopy.py processed
file while_for.py has 46 lines, file while_for.py processed

cannot division by zero

cannot division by zero
'''

# 文件列表
files = ['random_str.py', 'list_methods.py', 'tuple_list.py', 'copy_depcopy.py', 'while_for.py']

# try-except-else-finally语句
for file in files:
    try:
        f = open(file, encoding='utf-8')
    except IOError:
        print(f'Can not open file {file}', end=', ')
    else:
        print(f'file {file} has {len(f.readlines())} lines', end=', ')  # 输出文本文件行数
        f.close()
    finally:
        print(f'file {file} processed')
print()

# assert断言：主动抛出异常
a = 3
b = 0
try:
    assert b != 0, 'cannot division by zero'
except AssertionError as e:
    print(e.args[0])
print()

# raise主动抛出异常
try:
    raise ZeroDivisionError('cannot division by zero')
except ZeroDivisionError as e:
    print(e.args[0])
