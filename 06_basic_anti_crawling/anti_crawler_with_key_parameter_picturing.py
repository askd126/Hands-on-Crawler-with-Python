# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-12 7:21
@Project  :   Hands-on Crawler with Python-anti_crawler_with_key_parameter_picturing
关键参数图片化反爬
http://42.194.197.95:8001/phone_picture
'''

# 导入所需的库
import re
from urllib.parse import urljoin

import pytesseract
import requests
from PIL import Image
from bs4 import BeautifulSoup

base_url = 'http://42.194.197.95:8001/'
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
}
PHONE_PATTERN = re.compile('\d+')

# 发起请求
response = requests.get(urljoin(base_url, 'phone_picture'), cookies=cookies, headers=headers, verify=False)

# 解析网页
dom = BeautifulSoup(response.text, 'lxml')

# 获取图片元素
imgs = dom.find('tbody').find_all('img')

# 逐一获取图片链接并识别
for img in imgs:
    # 获取图片链接
    img_link = img.attrs.get('src')
    img_link = urljoin(base_url, img_link)  # 补全图片链接

    # 下载图片
    image = requests.get(img_link, stream=True).raw
    image = Image.open(image)

    # 识别图片中的手机号码
    phone_number = pytesseract.image_to_string(image)
    phone_number = PHONE_PATTERN.search(phone_number).group()
    print(f'URL: {img_link}, Phone Number: {phone_number}')
