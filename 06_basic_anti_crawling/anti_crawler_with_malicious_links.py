# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-12 7:54
@Project  :   Hands-on Crawler with Python-anti_crawler_with_malicious_links
恶意链接反爬
http://42.194.197.95:8001/poison_url
'''

import os

import requests
from bs4 import BeautifulSoup

image_root = '../output/douban_covers'
url = 'http://42.194.197.95:8001/poison_url'
cookies = {
    'session': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw',
    'auth': '210LNWPC217201PHR1702309731',
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'  # 不使用普通浏览器的User-Agent，模拟搜索引擎百度来应对恶意链接反爬
}


def download_image(url):
    image_path = os.path.join(image_root, url.split('/')[-1])
    response = requests.get(url, cookies=cookies, headers=headers, verify=True)
    with open(image_path, 'wb') as f:
        f.write(response.content)


def crawl():
    response = requests.get(url, cookies=cookies, headers=headers, verify=False)
    dom = BeautifulSoup(response.text, 'lxml')

    # movie_list = dom.find('div', class_='movie-list').find_all('a')  # 报错AttributeError: 'NoneType' object has no attribute 'find_next_sibling'
    movie_list = dom.find('div', class_='movie-list').find_all('a', class_='list-group-item')  # 获取a标签时增加条件
    for movie in movie_list:
        image_link = movie.find('p').find_next_sibling('p').get_text()  # 包含了隐藏起来的恶意链接http://42.194.197.95:8001/poison_img_url，请求后就会被封IP、1分钟内无法再次访问
        download_image(image_link)
        print(f'{image_link} downloaded.')


if __name__ == '__main__':
    crawl()
