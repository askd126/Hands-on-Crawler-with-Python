# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-06 21:57
@Project  :   Hands-on Crawler with Python-douban_top_movie_crawler_aiohttp
爬取豆瓣Top电影——aiohttp版（达到真正协程）
http://42.194.197.95:8001/base
PID: 32884 - __main__.serial_run - 2.7260 seconds
PID: 32884 - __main__.thread_run - 0.7227 seconds
PID: 32884 - __main__.process_run - 2.3821 seconds
PID: 3968 - __main__.coroutine_run - 2.8184 seconds
PID: 6716 - __main__.aiohttp_run - 0.3655 seconds
'''

# 导入所需的库
import asyncio
import re

import aiohttp
import pymongo
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


def parse(html):
    '''
    解析HTML：
    BeautifulSoup不支持协程，只能同步解析，速度较慢，因此即使使用async关键字修饰也无法使解析HTML变成协程、从而加快解析速度
    '''
    dom = BeautifulSoup(html, 'lxml')

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


async def crawl_movie(session, url):
    '''
    单个链接爬取：
    aiohttp支持协程，异步请求，速度较快
    '''
    response = await session.get(url)  # session.get支持异步协程，在请求时可以使用await交出执行权，交给系统等待网络请求的响应
    html = await response.text()  # text方法也支持异步协程，在解析时也可以使用await交出执行权
    parse(html)


async def run():
    async with aiohttp.ClientSession(cookies=cookies) as session:
        tasks = [asyncio.create_task(crawl_movie(session, url)) for url in urls]
        await asyncio.wait(tasks)


@time_it
def aiohttp_run():
    '''
    协程版爬虫：
    网络请求使用aiohttp，支持协程、实现异步，在网络请求较慢时可以将执行权交给其他任务，速度较快。
    解析网页使用BeautifulSoup，不支持 协程、只能同步，必须被阻塞才能完成任务，因此解析速度较慢，并且无法避免。
    针对这种情况，一般的爬虫策略：
    （1）爬虫模块专门负责爬取原始数据，存入暂存数据库（如MongoDB）中；
    （2）解析模块再从暂存数据库中取值解析，或者通过队列（Kafka、RabbitMQ等）将两者连接。
    每个模块都负责自己的逻辑，将自己负责的部分最优化，爬虫提高爬取速度（协程）、解析提高解析速度（多进程+多线程）。
    总体上，使用aiohttp实现协程提速更快，甚至超过多线程，挖掘出了多协程的优势。
    '''
    asyncio.run(run())


if __name__ == '__main__':
    aiohttp_run()

    # 关闭数据库连接
    client.close()
