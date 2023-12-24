# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-12 23:24
@Project  :   Hands-on Crawler with Python-edge_baidu_with_selenium
使用selenium操作edge访问百度
https://www.baidu.com/
'''

# 导入所需的库
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://www.baidu.com/'
browser = webdriver.Edge()  # 定义Edge浏览器，默认会加载当前Python虚拟环境目录下的Scripts目录下的msedgedriver.exe，也可以通过executable_path参数指定路径
browser.maximize_window()  # 最大化窗口

try:
    browser.get(url)
    input_box = browser.find_element(By.ID, 'kw')  # 定位网页中id为kw的元素，即百度搜索输入框
    input_box.clear()  # 清空输入框
    input_box.send_keys('Python')  # 输入搜索关键词
    input_box.send_keys(Keys.ENTER)  # 按下回车键
    WebDriverWait( # 隐式等待
        browser, 10 # 超时时间为10秒，默认每隔0.5秒检查一次
    ).until(EC.presence_of_element_located((By.ID, 'content_left')))  # 等待网页加载完成
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.title)
    print(len(browser.page_source), type(browser.page_source))
finally:
    time.sleep(5)
    browser.close()
