# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-24 22:47
@Project  :   Hands-on Crawler with Python-capture_mouse_move_with_selenium
使用selenium捕获鼠标移动
http://42.194.197.95:8001/captcha_mousemove
'''

# 导入所需的库
import random
import time

from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'http://42.194.197.95:8001/captcha_mousemove'
cookies = {
    'name': 'session',
    'value': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw'
}

options = EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 防止打印无用的日志

browser = webdriver.Edge(options=options)
browser.maximize_window()
with open('../static/js/stealth.min.js') as f:  # 读取JavaScript脚本
    js = f.read()

browser.execute_cdp_cmd(  # 在browser请求网页前执行隐藏浏览器特征的开源JS脚本
    'Page.addScriptToEvaluateOnNewDocument',
    {'source': js}
)

try:
    browser.get(url)
    browser.add_cookie(cookies)
    browser.get(url)

    # 等待2个按钮加载出来
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'button1')))
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'button2')))

    # 定位2个按钮
    button1 = browser.find_element(By.CLASS_NAME, 'button1')
    button2 = browser.find_element(By.CLASS_NAME, 'button2')

    button1.click()  # 点击第1个按钮
    print(f'button1 clicked')
    time.sleep(random.random() * 3)  # 随机等待0~5秒
    browser.switch_to.alert.accept()  # 切换到alert弹出框并点击确定按钮
    browser.switch_to.default_content()  # 切换到默认的窗口

    time.sleep(random.random() * 5)  # 随机等待0~5秒
    button2.click()
    print(f'button2 clicked')
    time.sleep(random.random() * 3)  # 随机等待0~5秒
    browser.switch_to.alert.accept()
    browser.switch_to.default_content()

finally:
    time.sleep(random.random() * 5)  # 随机等待0~5秒、模拟用户行为
    print('simple sliding puzzle done')
    browser.quit()
