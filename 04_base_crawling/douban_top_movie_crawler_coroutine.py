# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-06 20:36
@Project  :   Hands-on Crawler with Python-douban_top_movie_crawler_coroutine
爬取豆瓣Top电影——协程版（未达到真正协程）
http://42.194.197.95:8001/base
PID: 32884 - __main__.serial_run - 2.7260 seconds
PID: 32884 - __main__.thread_run - 0.7227 seconds
PID: 32884 - __main__.process_run - 2.3821 seconds
PID: 3968 - __main__.coroutine_run - 2.8184 seconds
'''

# 导入所需的库
import asyncio
import re

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


async def crawl_movie(url):  # 虽然使用了async，但实际上并没有真正的异步，因为函数内部没有使用yield或await交出函数的执行权限
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


async def run():
    '''协程任务'''
    tasks = [asyncio.create_task(crawl_movie(url)) for url in urls]
    await asyncio.wait(tasks)


@time_it
def coroutine_run():
    '''
    多协程爬取：
    协程的本质是异步模型，因为它允许任务在等待外部事件时主动让出控制权，并在准备好时重新获取执行权，这样，多个协程可以在单个线程上交替执行，从而避免了上下文切换的开销。协程的异步特性则是因为其轻量级以及其完全由程序控制的特性。
    但在爬取主函数crawl_movie中，虽然用async关键字修饰函数，但是函数内部的requests和BeautifulSoup的操作都是不支持asyncio的，因此无法通过协程来加速。
    因此通过简单的协程甚至可能比串行更慢。
    '''
    asyncio.run(run())


if __name__ == '__main__':
    coroutine_run()

    # 关闭数据库连接
    client.close()
