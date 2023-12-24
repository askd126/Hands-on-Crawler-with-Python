# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-11 19:52
@Project  :   Hands-on Crawler with Python-anti_crawler_with_user_agent
User-Agent反爬
http://42.194.197.95:8001/user_agent
'''

# 导入所需的库
import requests

url = 'http://42.194.197.95:8001/user_agent'
# 使用cookies进行登录
cookies = {
    'session': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZW3Ddw.8XN65U7-JTYaYya3zHavHwBKbLE'
}
# 设置请求头：带有User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
}

# 不带User-Agent
response = requests.get(url, cookies=cookies)
print(response.text)
print(len(response.text), 'Error 400' in response.text)  # 不带User-Agent，返回的html长度更短、内容更少（不包含电影列表）、包含Error 400

# 带有User-Agent
response = requests.get(url, cookies=cookies, headers=headers)
print(len(response.text), 'Error 400' in response.text)  # 带有User-Agent，返回的html长度更长、内容更多（包含电影列表）、不包含Error 400
