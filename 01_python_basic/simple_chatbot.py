# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-06 7:17
@Project  :   Hands-on Crawler with Python-simple_chatbot
while循环简单聊天机器人：
提问：今天天气好吗？
回答：今天天气好！
提问：吃了吗？
回答：吃了！
提问：好吃吗？
回答：好吃！
'''

# 无限循环
while True:
    q = input('提问：')  # 接收用户输入
    a = q.strip('吗？')  # 对字符串进行处理
    print('回答：' + a + '！')  # 打印输出
