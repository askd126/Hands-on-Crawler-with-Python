# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-11-17 22:11
@Project  :   Hands-on Crawler with Python-snake_advanced
贪吃蛇进阶版——食物可动，蛇追食物：
1.控制的对象是食物，而不是蛇；
2.蛇可以自动加速；
3.蛇的身体可以自动变长；
4.蛇的大体移动方向是食物所在的方向
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
directions = [UP, DOWN, LEFT, RIGHT]  # 所有方向
MOVE_MAP = {LEFT: (0, -1), RIGHT: (0, 1), UP: (-1, 0), DOWN: (1, 0)}  # 移动方向与坐标变化的映射
is_dead = False  # 是否死亡

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
# 通过轮数来控制蛇的速度和体长
SPEED_STEP = 2  # 速度增长间隔
BODY_STEP = 5  # 身体增长间隔

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

    value = ''  # 键盘输入
    move = False  # 是否移动
    turn = 0  # 游戏轮数
    while value.lower() != 'q':  # 不退出
        value = term.inkey(timeout=1 / speed)  # 阻塞timeout参数指定的时间，获取键盘输入
        if value.code in directions:  # 只有按4个方向键之一，才会移动
            move = True
        if not move:  # 输入的不是方向键，则不移动，跳入下一次循环继续输入
            continue

        # 1.移动蛇
        head = snake[0]  # 蛇头
        y_delta = food[0] - head[0]  # 食物与蛇头的Y坐标差
        x_delta = food[1] - head[1]  # 食物与蛇头的X坐标差
        move_to = None  # 蛇希望移动的方向：食物所在位置的方向，向着坐标差距更大的方向移动
        if abs(y_delta) > abs(x_delta):  # 食物与蛇头的Y坐标差大于X坐标差
            if y_delta > 0:  # 食物在蛇头的下方
                move_to = DOWN
            else:  # 食物在蛇头的上方
                move_to = UP
        else:  # 食物与蛇头的Y坐标差小于X坐标差
            if x_delta > 0:  # 食物在蛇头的右方
                move_to = RIGHT
            else:  # 食物在蛇头的左方
                move_to = LEFT

        random.shuffle(directions)
        move_tos = [move_to] + directions  # 所有可能的方向，包含随机性
        next_move = None  # 下一个移动的方向
        for move_to in move_tos:
            movement = MOVE_MAP.get(move_to)
            head_ = copy(head)
            # 计算新蛇头的位置
            head_[0] += movement[0]
            head_[1] += movement[1]
            # 新蛇头位置的内容
            head_content = world[head_[0]][head_[1]]
            if head_content == BORDER:  # 新蛇头位置是边界
                continue
            elif head_content == BODY:  # 新蛇头位置是身体
                if head_ == snake[-1] and turn % BODY_STEP != 0:  # 新蛇头位置是蛇尾，但蛇身不变长，此时允许，可以进入下一步，否则失败、要退出游戏
                    next_move = head_
                    break
                else:  # 其他情况，要判断下一个方向
                    continue
            else:  # 其他情况，都允许进入下一步
                next_move = head_
                break

        # 所有动作都尝试后，依然无法移动
        if not next_move:
            break  # 退出游戏

        world[food[0]][food[1]] = SPACE  # 蛇移动前，需要清理当前食物的位置
        snake.appendleft(next_move)
        world[head[0]][head[1]] = BODY  # 蛇头移动之后，原来的蛇头位置设为身体
        world[next_move[0]][next_move[1]] = HEAD  # 蛇头移动之后，蛇头位置设为头部
        if turn % BODY_STEP != 0:  # 蛇身不变长
            tail = snake.pop()  # 为了保持蛇身不变长，需要将蛇尾弹出
            world[tail[0]][tail[1]] = SPACE  # 蛇尾移动之后，原来的蛇尾位置设为空白

        if turn % SPEED_STEP == 0:  # 速度增长
            speed = min(speed * 1.01, MAX_SPEED)

        # 2.移动食物
        food_ = copy(food)
        if value.code in directions:
            direction = value.code
            movement = MOVE_MAP.get(direction)
            # 食物移动的下一个方向
            food_[0] += movement[0]
            food_[1] += movement[1]
            food_content = world[food_[0]][food_[1]]

            if food_content == HEAD or food_content == BODY:  # 食物碰到头部或身体，则游戏结束
                is_dead = True
            elif food_content == SPACE:  # 只能移到空白处
                food = food_  # 食物移动到空白位置

            if not is_dead:  # 游戏未结束
                world[food[0]][food[1]] = FOOD  # 更新食物

            print(term.move_yx(0, 0))  # 移动光标到屏幕左上角
            # 重新绘制世界
            for row in world:
                print(' '.join(row))

            score += 1
            print(f'score: {score:2d} - speed: {speed:.2f}')

            if is_dead:
                break

        turn += 1

print('game over')
