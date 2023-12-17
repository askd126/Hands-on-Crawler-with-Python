# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-13 22:15
@Project  :   Hands-on Crawler with Python-anti_crawler_with_browser_feature
使用selenium操作Edge实现浏览器特征检测反爬
http://42.194.197.95:8001/webdriver
'''

# 导入所需的库
import re

import pymongo
from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'http://42.194.197.95:8001/webdriver'
cookies = {
    'name': 'session',
    'value': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw'
}
options = EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 防止打印无用的日志
options.add_experimental_option('prefs', {  # 禁止图片和CSS加载
    'profile.managed_default_content_settings.images': 2,
    'profile.defaults.stylesheets': 2
})

client = pymongo.MongoClient(host='127.0.0.1', port=27017)  # 连接MongoDB数据库
db = client.crawler
collection = db.douban_top_movie


def crawl_with_header(execute_js=True):
    browser = webdriver.Edge(options=options)
    browser.maximize_window()

    movies = []
    try:
        # 读取JavaScript脚本
        with open('../static/js/stealth.min.js') as f:
            js = f.read()

        if execute_js:  # 在browser请求网页前执行隐藏浏览器特征的开源JS脚本
            browser.execute_cdp_cmd(  # 执行JS脚本
                'Page.addScriptToEvaluateOnNewDocument',
                {'source': js}
            )

        # 执行JS脚本后，再请求页面
        browser.get(url)
        browser.add_cookie(cookies)
        browser.get(url)
        if execute_js:  # 执行JS，再请求页面
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'list-group-item')))  # 已执行JS脚本，等待电影列表标签加载
            print(len(browser.page_source), 'Error 400' in browser.page_source)  # 执行JS脚本后，隐藏浏览器特征，返回正常页面，内容更长、不包含异常信息
            movie_list = browser.find_elements(By.CLASS_NAME, 'list-group-item')
            for movie in movie_list:
                image_link = movie.find_element(By.TAG_NAME, 'img').get_attribute('src')
                movie_name = movie.find_element(By.CLASS_NAME, 'mb-1').text
                movie_info = re.sub(r'\s+', ' ',
                                    movie.find_element(By.TAG_NAME, 'p').text.replace('\xa0', ' ').replace('\n', ''))
                smalls = movie.find_elements(By.TAG_NAME, 'small')
                score = float(smalls[0].text[:-2])
                desc = smalls[1].text
                movies.append({
                    'image_link': image_link,
                    'movie_name': movie_name,
                    'movie_info': movie_info,
                    'movie_score': score,
                    'desc': desc
                })
        else:  # 不执行JS，请求页面
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'jumbotron')))  # 未执行JS脚本，等待class属性为container的main标签加载完成，即主页面加载完成
            print(len(browser.page_source),
                  'Error 400' in browser.page_source)  # 被网站识别出浏览器特征、判断为自动化程序，返回异常页面，内容更短、包含异常信息
    finally:
        print(f'crawl done, {len(movies)} movies crawled')
        if movies:
            collection.insert_many(movies)
        browser.quit()


if __name__ == '__main__':
    crawl_with_header(execute_js=True)
    crawl_with_header(execute_js=False)
    client.close()
