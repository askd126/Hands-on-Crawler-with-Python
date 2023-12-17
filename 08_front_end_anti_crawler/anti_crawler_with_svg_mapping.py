# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-16 10:06
@Project  :   Hands-on Crawler with Python-anti_crawler_with_svg_mapping
SVG映射反爬
http://42.194.197.95:8001/svg
'''

# 导入所需的库
import re

import requests
from bs4 import BeautifulSoup

cookies = {
    'session': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw'
}

url = 'http://42.194.197.95:8001/svg'
svg_url = 'http://42.194.197.95:8001/static/number.svg'
css_url = 'http://42.194.197.95:8001/static/css/phone_svg.css'
font_size_pattern = re.compile(r'font-size:(\d+)px')

# 获取SVG内容与CSS样式内容
svg_content = requests.get(svg_url, cookies=cookies).text
css_content = requests.get(css_url, cookies=cookies).text


def get_location_from_css(css_content, class_name):
    '''
    从CSS中获取某个class对应的位置
    :param css_content: CSS原始代码
    :param class_name: class属性值
    :return: 当前class属性值对应的横纵坐标
    '''
    css_content = css_content.replace('\n', '').replace(' ', '')  # 去除CSS中的换行符和空格
    locations = re.findall('.%s{background:-(\d+)px-(\d+)px;}' % class_name, css_content)
    return int(locations[0][0]), int(locations[0][1])


def get_font_size_y_text_from_svg(svg_content):
    '''
    从SVG中获取字体大小、所有行的y轴坐标和文本
    :param svg_content: SVG原始代码
    :return: 字体大小、y轴坐标、文本
    '''
    sizes = font_size_pattern.findall(svg_content)
    font_size = int(sizes[0]) if sizes else 16  # SVG中默认字体大小为16

    dom = BeautifulSoup(svg_content, 'xml')  # 解析SVG
    text_tags = dom.find_all('text')  # 获取所有text标签
    y_locations = [int(tag.attrs['y']) for tag in text_tags]
    texts = [tag.text for tag in text_tags]

    return font_size, y_locations, texts


def get_num_from_class(class_name, font_size, y_locations, texts):
    '''
    根据class属性获取对应的数字
    :param class_name: class属性值
    :param font_size: 字体大小
    :param y_locations: SVG中所有的text标签的y属性值
    :param texts: SVG中所有的text标签的文本
    :return: 当前class值对应的数字
    '''
    css_x, css_y = get_location_from_css(css_content, class_name)  # 获取当前class属性对应的位置
    chosen_y = [y for y in y_locations if y >= css_y][0]  # CSS与SVG的y轴坐标关系：获取≥CSS的y轴坐标中的第1个，即最接近的1个
    chosen_text = texts[y_locations.index(chosen_y)]  # 被选择的行
    x_location = css_x // font_size  # 数字的x轴坐标
    num = chosen_text[x_location]  # 定位到x坐标对应的数字
    return num


def crawl():
    '''
    爬虫主程序：
    1.获取网页中的所有相关class属性；
    2.根据class从CSS中获取到相应数字的坐标；
    3.获取SVG文件中所有的纵坐标和文本值；
    4.根据CSS纵坐标获取数字所在的行；
    5.根据CSS横坐标和字体大小获取到所在行的对应数字。
    :return: 拼接后的电话号码
    '''
    # 获取共用信息：字体大小、y轴坐标、文本，执行一次即可
    font_size, y_locations, texts = get_font_size_y_text_from_svg(svg_content)

    response = requests.get(url, cookies=cookies)
    dom = BeautifulSoup(response.text, 'lxml')
    d_tags = dom.find('div', class_='media-body').find_all('p')[2].find_all(
        'd')  # 获取class属性为media-body的div标签下的第3个p标签下的所有d标签，定位到电话号码所在位置
    phone_number = [get_num_from_class(d.attrs['class'][0], font_size, y_locations, texts) for d in d_tags]
    return ''.join(phone_number)


if __name__ == '__main__':
    phone_number = crawl()
    print(phone_number)
