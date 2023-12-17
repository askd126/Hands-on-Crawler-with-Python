# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-13 21:07
@Project  :   Hands-on Crawler with Python-anti_crawler_with_iframe
使用selenium操作Edge实现内嵌iframe网页反爬
http://42.194.197.95:8001/iframe_out
'''

# 导入所需的库
import time

from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'http://42.194.197.95:8001/iframe_out'
options = EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Edge(options=options)

try:
    browser.get(url)
    browser.add_cookie({'name': 'session',
                        'value': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw'})
    browser.get(url)

    # 等待输入框元素加载
    # WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, 'inputEmail'))) # 等待账号输入框元素加载，等待10秒，报错selenium.common.exceptions.TimeoutException，因为输入框在iframe中
    # 找到内嵌的iframe元素并将控制句柄切换到iframe中
    iframe = browser.find_element(By.ID, 'myiframe')
    browser.switch_to.frame(iframe)
    WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, 'inputEmail')))  # 等待账号输入框元素加载，此时成功定位

    # 输入邮箱
    email_input = browser.find_element(By.ID, 'inputEmail')
    email_input.clear()
    email_input.send_keys('username')  # 提交时前端会验证邮箱格式
    # 输入密码
    password_input = browser.find_element(By.ID, 'inputPassword')
    password_input.clear()
    password_input.send_keys('123456')

    # 点击登录按钮
    button = browser.find_element(By.TAG_NAME, 'button')
    button.click()

finally:
    time.sleep(5)
    browser.quit()
