# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-17 7:11
@Project  :   Hands-on Crawler with Python-snake_basic
贪吃蛇基础版
'''

import random
from collections import deque
from copy import copy

from blessed import Terminal

# 定义常量
term = Terminal()  # 终端

# 方向常量
UP = term.KEY_UP
DOWN = term.KEY_DOWN
LEFT = term.KEY_LEFT
RIGHT = term.KEY_RIGHT
direction = RIGHT  # 初始默认方向

# 图标
BORDER = '-'  # 边界
HEAD = 'O'  # 头部
BODY = 'o'  # 身体
FOOD = '*'  # 食物
SPACE = ' '  # 空白

# 游戏参数
WIDTH = 30  # 屏幕宽度
HEIGHT = 20  # 屏幕高度
snake = deque([[6, 5], [6, 4], [6, 3]])  # 贪吃蛇
food = [15, 10]  # 食物
score = 0  # 得分
speed = 3  # 游戏速度
MAX_SPEED = 10  # 最大速度

# 随机获取游戏空间的空白位置
get_random_space = lambda world: random.choice(
    [[i, j] for j in range(WIDTH) for i in range(HEIGHT) if world[i][j] == SPACE])

with term.cbreak(), term.hidden_cursor():  # 上下文管理器，隐藏光标
    # 清空屏幕
    print(term.home + term.clear)

    # 构造世界
    world = [[SPACE for _ in range(WIDTH)] for _ in range(HEIGHT)]
    # 构造边界
    for i in range(WIDTH):  # 横线
        world[0][i] = BORDER
        world[-1][i] = BORDER
    for i in range(HEIGHT):  # 竖线
        world[i][0] = BORDER
        world[i][-1] = BORDER

    # 绘制贪吃蛇
    for i in snake:  # 绘制身体
        world[i[0]][i[1]] = BODY
    # 绘制头
    world[snake[0][0]][snake[0][1]] = HEAD
    # 绘制食物
    world[food[0]][food[1]] = FOOD

    # 绘制世界
    for row in world:
        print(' '.join(row))

    value = ''
    move = False  # 是否移动
    while value.lower() != 'q':  # 不退出
        value = term.inkey(timeout=1 / speed)  # 阻塞timeout参数指定的时间，获取键盘输入
        if value.code in [UP, DOWN, LEFT, RIGHT]:  # 只有按4个方向键之一，才会移动
            move = True
        if not move:  # 输入的不是方向键，则不移动，跳入下一次循环继续输入
            continue

        # 按了方向键并且不与之前的方向相反，才进行移动
        if value.code == UP and direction != DOWN:
            direction = UP
        elif value.code == DOWN and direction != UP:
            direction = DOWN
        elif value.code == LEFT and direction != RIGHT:
            direction = LEFT
        elif value.code == RIGHT and direction != LEFT:
            direction = RIGHT

        # 移动蛇头
        head = copy(snake[0])
        if direction == UP:  # 上移，Y坐标减1
            head[0] -= 1
        elif direction == DOWN:  # 下移，Y坐标加1
            head[0] += 1
        elif direction == LEFT:  # 左移，X坐标减1
            head[1] -= 1
        elif direction == RIGHT:  # 右移，X坐标加1
            head[1] += 1

        # 蛇头移动之后的新位置的内容
        head_ = world[head[0]][head[1]]
        ate_food = False  # 是否吃到食物
        if head_ == FOOD:  # 吃到食物
            score += 1  # 得分加1
            ate_food = True
            food = get_random_space(world)  # 获取新的食物位置
            world[food[0]][food[1]] = FOOD  # 放置食物
            speed = min(MAX_SPEED, speed * 1.01)
        elif head_ == BORDER:  # 吃到边界
            break  # 退出游戏
        elif head_ == BODY and head_ != snake[-1]:  # 吃到身体，并且不是蛇尾（是蛇尾时，会形成环，并且蛇前进时，头会前进一格、尾部也会前进格，此时不会相交，因此是允许的）
            break  # 退出游戏

        if not ate_food:  # 未吃到食物，则长度保持不变，需要从尾部弹出一个元素
            tail = snake.pop()
            world[tail[0]][tail[1]] = SPACE  # 绘制尾部为空白

        # 增加蛇头
        snake.appendleft(head)
        # 重新绘制蛇
        for i in snake:
            world[i[0]][i[1]] = BODY
        world[snake[0][0]][snake[0][1]] = HEAD
        print(term.move_yx(0, 0))  # 移动光标到屏幕左上角
        # 重新绘制世界
        for row in world:
            print(' '.join(row))

        print(f'score: {score:2d} - speed: {speed:.2f}')

print('game over')
