# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-08 22:42
@Project  :   Hands-on Crawler with Python-while_for
Python中的while和for循环：
0 -> even
1 -> odd
2 -> even
3 -> odd
4 -> even
5 -> odd
6 -> even
7 -> odd
8 -> even
9 -> odd

0
1
2
4
5
6
7
'''

# while循环
count = 0
while count < 10:
    if count % 2 == 0:
        print(f'{count} -> even')
    else:
        print(f'{count} -> odd')
    count += 1
print()

# for循环
for i in range(count):
    if i == 3:
        continue  # 跳过本次循环
    if i > 7:
        break  # 中断循环
    print(i)
