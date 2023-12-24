# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-15 22:04
@Project  :   Hands-on Crawler with Python-anti_crawler_with_css_offset
CSS偏移反爬
http://42.194.197.95:8001/flight
'''

# 导入所需的库
import re

import requests
from bs4 import BeautifulSoup

url = 'http://42.194.197.95:8001/flight'
cookies = {
    'session': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}
width_pattern = re.compile(r'width:(\d+)px')
offset_pattern = re.compile(r'left:(-\d+)px')

response = requests.get(url, cookies=cookies, headers=headers)
dom = BeautifulSoup(response.text, 'lxml')

with open('flight.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
movies = dom.find_all('div', class_='row')  # 找到所有class属性为row的div，包含了单条电影信息，其中就包括价格信息
for movie in movies:
    movie_name = movie.find('h5', class_='mb-1').text
    span = movie.find('span', class_='fix_price')  # 找到class属性为fix_price的span标签，包含价格信息
    price_bs = span.find_all('b')  # 找到span标签下的所有b标签

    # 处理第1个b标签
    first_b = price_bs[0]  # 找到第1个b标签，包含原始价格
    style = first_b.attrs['style']  # 获取第1个b标签的style属性
    first_b_width = int(width_pattern.findall(style)[0])  # 提取出宽度字符串，并将其转换为整数
    first_b_nums = first_b.text.strip().replace('\n', '')  # 提取出原始价格字符串，并清洗

    # 处理剩余的b标签
    offset_bs = []  # 保存剩余b标签的宽度和数值信息
    for b in price_bs[1:]:
        style = b.attrs['style']
        b_width = int(offset_pattern.findall(style)[0])
        b_num = b.text
        offset_bs.append((b_width, b_num))  # 保存格式为元组：(宽度, 数值)

    # 替换偏移数值、得到最终价格bbbbb
    per_width = first_b_width // len(first_b_nums)  # 每一个b标签的宽度
    price = list(first_b_nums)  # 价格字符串转化为列表
    for b_width, b_num in offset_bs:
        offset_index = b_width // per_width  # 根据当前b标签向左偏移的宽度计算片以后的索引（为负值）
        price[offset_index] = b_num  # 按照偏移索引替换为新的数值
    price = int(''.join(price))
    print(f'movie: {movie_name}, price: {price}')
