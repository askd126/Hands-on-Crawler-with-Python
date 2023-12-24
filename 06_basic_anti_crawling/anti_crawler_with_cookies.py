# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-11 20:44
@Project  :   Hands-on Crawler with Python-anti_crawler_with_cookies
Cookies反爬
http://42.194.197.95:8001/movies_cookies
'''

# 导入所需的库
import requests

# 设置cookie
cookies = {
    'session': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw',
    'auth': '213VYFGM656175FQQ1702297941',
}
# 设置headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    # 'Cookie': 'session=.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw; auth=213VYFGM656175FQQ1702297941',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://42.194.197.95:8001/cookies',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
}

# 不带cookies
response = requests.get('http://42.194.197.95:8001/movies_cookies', headers=headers, verify=False)
print(len(response.text), '请登录' in response.text)  # 不带cookies，返回的html长度更短、内容更少（不包含电影列表）、提示请登录

# 带cookies
response = requests.get('http://42.194.197.95:8001/movies_cookies', cookies=cookies, headers=headers, verify=False)
print(len(response.text), '请登录' in response.text)  # 带cookies，返回的html长度更长、内容更多（包含电影列表）、已登录未提示
