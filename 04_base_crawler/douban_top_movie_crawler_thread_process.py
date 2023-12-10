# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-06 7:51
@Project  :   Hands-on Crawler with Python-douban_top_movie_crawler_thread_process
爬取豆瓣Top电影——线程进程版
http://42.194.197.95:8001/base
输出：
PID: 32884 - __main__.serial_run - 2.7260 seconds
PID: 32884 - __main__.thread_run - 0.7227 seconds
PID: 32884 - __main__.process_run - 2.3821 seconds
'''

# 导入所需的库
import re
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import pymongo
import requests
from bs4 import BeautifulSoup

from utils.decorators.func_tool import time_it

# 定义常量
urls = ['http://42.194.197.95:8001/base' for _ in range(20)]  # 待爬取链接列表，模拟有多个待爬取链接
cookies = {  # cookie
    'session': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZW3Ddw.8XN65U7-JTYaYya3zHavHwBKbLE'
}
client = pymongo.MongoClient(host='127.0.0.1', port=27017)  # MongoDB数据库连接
db = client.crawler
collection = db.douban_top_movie
num_workers = 5  # 并行数


def crawl_movie(url):
    '''单个链接爬取'''
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
        movie_info = re.sub(r'\s+', ' ',
                            movie.find('p').text.replace('\xa0', ' ').replace('\n', ''))  # 获取电影简介，并去除多余无效字符
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


@time_it
def serial_run():
    '''串行爬取'''
    for url in urls:
        crawl_movie(url)


@time_it
def thread_run():
    '''
    多线程爬取：
    较低的资源消耗、较小的上下文切换开销、共享父进程的内存空间以及较好的I/O处理能力，更适合I/O密集型任务（例如爬虫），提速更明显
    '''
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for url in urls:
            executor.submit(crawl_movie, url)


@time_it
def process_run():
    '''
    多进程爬取：
    较高的资源消耗、较高的上下文切换成本、拥有独立的内存空间以及较差的I/O处理能力，更适合CPU密集型任务（例如复杂计算），提速不明显
    '''
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for url in urls:
            executor.submit(crawl_movie, url)


if __name__ == '__main__':
    serial_run()
    thread_run()
    process_run()

    # 关闭数据库连接
    client.close()
