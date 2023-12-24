# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-13 21:52
@Project  :   Hands-on Crawler with Python-bot_sannysoft_with_selenium
自动化工具控制浏览器被识别特征
https://bot.sannysoft.com/
'''

# 导入所需的库
import time

from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://bot.sannysoft.com/'


def crawl_with_header():
    '''
    正常访问：能检测到个别浏览器特征
    '''
    options = EdgeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Edge(options=options)
    browser.maximize_window()

    try:
        browser.get(url)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'user-agent-result')))
        browser.save_screenshot('../output/selenium/bot_sannysoft_header.png')
    finally:
        time.sleep(5)
        browser.quit()


def crawl_headless():
    '''
    无头浏览器访问：能检测到大部分浏览器特征
    '''
    options = EdgeOptions()
    options.add_argument('--headless')  # 设置无头浏览器
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Edge(options=options)
    browser.maximize_window()

    try:
        browser.get(url)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'user-agent-result')))
        browser.save_screenshot('../output/selenium/bot_sannysoft_headless.png')
    finally:
        time.sleep(5)
        browser.quit()


def crawl_headless_with_js():
    '''
    无头浏览器访问，同时执行JS脚本隐藏浏览器特征：无法检测到浏览器特征
    '''
    options = EdgeOptions()
    options.add_argument('--headless')  # 设置无头浏览器
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0')  # 添加请求头
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Edge(options=options)
    browser.maximize_window()

    # 读取JavaScript文件内容
    with open('../static/js/stealth.min.js', ) as f:
        js = f.read()

    # 在browser请求网页前执行隐藏浏览器特征的开源JS脚本
    browser.execute_cdp_cmd(  # 执行Chrome Devtools Protocol命令，可以获取返回结果
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': js}
    )

    # 执行JS后再以无头浏览器请求网页
    try:
        browser.get(url)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'user-agent-result')))
        browser.save_screenshot('../output/selenium/bot_sannysoft_js.png')
        with open('../output/selenium/bot_sannysoft_js.html', 'w') as f:
            f.write(browser.page_source)
    finally:
        time.sleep(5)
        browser.quit()


if __name__ == '__main__':
    crawl_with_header()
    crawl_headless()
    crawl_headless_with_js()
