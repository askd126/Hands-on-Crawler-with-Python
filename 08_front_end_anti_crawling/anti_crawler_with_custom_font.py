# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-16 14:44
@Project  :   Hands-on Crawler with Python-anti_crawler_with_custom_font
自定义字体反爬
http://42.194.197.95:8001/font
'''

# 导入所需的库
import re
from itertools import chain

import pytesseract
import requests
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

cookies = {
    'session': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw'
}
url = 'http://42.194.197.95:8001/font'
# 人工整理，得到字符与数字的映射表，也可以通过后面的ttf2num方法自动获取得到映射表
number_mapping = {
    'xee76': '0',
    'xf57b': '1',
    'xe7df': '2',
    'xf19a': '3',
    'xf593': '4',
    'xea16': '5',
    'xe339': '6',
    'xe9c7': '7',
    'xefd4': '8',
    'xe624': '9'
}
NONFONT_PATTERN = re.compile(r'.botdef|nonmarkingreturn|.null')
PHONE_PATTERN = re.compile('\d+')
OCR_CONFIG = '--oem 3 --psm 13 -c tessedit_char_whitelist=0123456789 outputbase digits'


def load_font(font_path):
    '''加载字体、获取字体中的所有字符'''
    with TTFont(font_path) as ttf:
        chars = chain.from_iterable([[y + (Unicode[y[0]],) for y in x.cmap.items()] for x in ttf[
            'cmap'].tables])  # 等价于chars = [y + (Unicode[y[0]],) for x in ttf['cmap'].tables for y in x.cmap.items()]
        chars = set(chars)
        chars = sorted(chars, key=lambda x: int(x[0]))
    return chars


def ttf2num(ttf_path, font_size=120, width=200, height=200):
    '''将ttf字体转换为图片并识别，返回字符到对应数字的映射'''
    # 加载字体
    chars = load_font(ttf_path)
    # 创建字体对象
    font = ImageFont.truetype(ttf_path, font_size)
    # 绘制图片进行识别，并一一映射
    font_mapping = {}
    for dec_num, hex_str, _ in chars:  # 十进制Unicode编码、十六进制字符串（以uni开头）
        if NONFONT_PATTERN.match(hex_str) or len(hex_str) <= 1:
            continue
        # 创建画板
        image = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        # 获取字体大小
        _, _, char_width, char_height = font.getbbox(chr(dec_num))
        # 计算字体开始绘制的位置
        x_start = (width - char_width) // 2
        y_start = (height - char_height) // 2
        # 绘制字符
        draw.text((x_start, y_start), chr(dec_num), (255, 255, 255), font=font)

        phone_number = pytesseract.image_to_string(image, config=OCR_CONFIG)  # 识别生成的图片为数字
        phone_number = PHONE_PATTERN.search(phone_number).group()  # 清洗数字字符串
        font_mapping[hex_str.replace('uni', 'x').lower()] = phone_number
    return font_mapping


def crawl(font_mapping):
    '''爬虫主函数：获取网页中的字体字符串，并根据映射关系转化为数字'''
    response = requests.get(url, cookies=cookies)

    phone_number_string = re.findall('&#(.+)', response.text)[0]
    phone_number_string = phone_number_string.split('&#')
    phone_number = [font_mapping[number] for number in phone_number_string]
    return ''.join(phone_number)


if __name__ == '__main__':
    font_mapping = ttf2num('../static/font/myword.woff')
    phone_number = crawl(font_mapping)
    print(phone_number)
