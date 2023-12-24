# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-13 7:16
@Project  :   Hands-on Crawler with Python-anti_crawler_with_edge_selenium
使用selenium操作Edge实现网页动态渲染反爬
http://42.194.197.95:8001/many_sign
'''

# 导入所需的库
import re
import time

import pymongo
from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'http://42.194.197.95:8001/many_sign'
options = EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 防止打印无用的日志
options.add_experimental_option('prefs', {  # 禁止图片和CSS加载，提高网页渲染速度、提升爬取速度
    'profile.managed_default_content_settings.images': 2,
    'profile.defaults.stylesheets': 2
})
browser = webdriver.Edge(options=options)
browser.maximize_window()
client = pymongo.MongoClient(host='127.0.0.1', port=27017)  # 连接MongoDB数据库
db = client.crawler
collection = db.douban_top_movie

movies = []
try:
    browser.get(url)
    browser.add_cookie({'name': 'session',
                        'value': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw'})
    browser.get(url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'app1')))
    for i in range(1, 6):
        movie = browser.find_element(By.ID, f'app{i}')
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
    print(f'crawl done, {len(movies)} movies crawled')
finally:
    collection.insert_many(movies)
    client.close()
    time.sleep(5)
    browser.quit()
