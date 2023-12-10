# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-06 19:18
@Project  :   Hands-on Crawler with Python-func_tool
函数工具
'''

import os
import time
from functools import wraps


def time_it(func):
    '''
    计算函数运行时间
    '''

    @wraps(func)  # 保留原函数的__name__等属性
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # 开始时间
        res = func(*args, **kwargs)
        end = time.perf_counter()  # 结束时间
        print(f'PID: {os.getpid()} - {func.__module__}.{func.__name__} - {end - start:.4f} seconds')
        return res

    return wrapper
