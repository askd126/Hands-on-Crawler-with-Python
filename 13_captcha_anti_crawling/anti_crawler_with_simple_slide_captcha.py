# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-24 17:02
@Project  :   Hands-on Crawler with Python-anti_crawler_with_simple_slide_captcha
简单滑块验证码反爬
http://42.194.197.95:8001/captcha_slide
'''

# 导入所需的库
import random
import time

from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'http://42.194.197.95:8001/captcha_slide'
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
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'sliderblock')))  # 等待滑块加载出来
    slider_block = browser.find_element(By.ID, 'sliderblock')
    action = webdriver.ActionChains(browser)  # 创建ActionChains对象、用于执行拖动动作
    action.click_and_hold(slider_block)  # 点击鼠标并按住不放
    action.move_by_offset(250, 0)  # 向右移动鼠标到相应的位置，滑轨宽度（300）滑块大小（50）=250
    action.release()  # 松开鼠标
    action.perform()  # 真正执行动作
finally:
    time.sleep(random.random() * 5)  # 随机等待0~5秒、模拟用户行为
    print('sliding done')
    browser.quit()
