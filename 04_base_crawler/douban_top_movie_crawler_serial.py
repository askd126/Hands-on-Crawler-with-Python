# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-05 23:32
@Project  :   Hands-on Crawler with Python-douban_top_movie_crawler_serial
爬取豆瓣Top电影——串行版
http://42.194.197.95:8001/base
'''

# 导入所需的库
import re

import pymongo
import requests
from bs4 import BeautifulSoup

url = 'http://42.194.197.95:8001/base'  # 待爬取链接
cookies = {  # cookie
    'session': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZW3Ddw.8XN65U7-JTYaYya3zHavHwBKbLE'
}
client = pymongo.MongoClient(host='127.0.0.1', port=27017)  # MongoDB数据库连接
db = client.crawler
collection = db.douban_top_movie

# 发送请求，得到HTML
response = requests.get(url, cookies=cookies)
# 解析HTML
dom = BeautifulSoup(response.text, 'lxml')

# 获取电影列表：获取class属性为movie-list的div下的所有a标签
movie_list = dom.find('div', class_='movie-list').find_all('a')
movies = []
for movie in movie_list:
    image_link = movie.find('img').attrs.get('src')  # 获取海报链接，attrs获取标签的所有属性，返回字典
    movie_name = movie.find('h5').text  # 获取电影名称
    # 将多个空格替换为一个空格
    movie_info = re.sub(r'\s+', ' ', movie.find('p').text.replace('\xa0', ' ').replace('\n', ''))  # 获取电影简介，并去除多余无效字符
    movie_score = float(movie.find('small').text[:-2])  # 获取电影评分
    desc = movie.find('small').find_next_sibling('small').text  # 获取电影描述
    movies.append({
        'image_link': image_link,
        'movie_name': movie_name,
        'movie_info': movie_info,
        'movie_score': movie_score,
        'desc': desc
    })

# 将数据保存到MongoDB数据库中
collection.insert_many(movies)
# 关闭数据库连接
client.close()
