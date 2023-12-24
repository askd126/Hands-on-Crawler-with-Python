# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-24 23:07
@Project  :   Hands-on Crawler with Python-anti_crawler_with_mouse_track_detection
鼠标轨迹检测反爬
http://42.194.197.95:8001/captcha_slide_puzzle_canvas_mousemove
'''

# 导入所需的库
import random
import time

from PIL import Image, ImageChops
from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

before_canvas_path = '../output/selenium/canvas_before.png'
after_canvas_path = '../output/selenium/canvas_after.png'
url = 'http://42.194.197.95:8001/captcha_slide_puzzle_canvas_mousemove'
cookies = {
    'name': 'session',
    'value': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw'
}
vis_script = '''
var crawler_missblock = document.getElementById("missblock");
crawler_missblock.style["visibility"] = "{}";
'''


def get_position_offset(before_path, after_path):
    '''对比获取Canvas背景图中缺口的位置'''
    # 读取的图片是PngImageFile对象、为RGBA模式，需要转换为RGB模式，来使用ImageChops进行对比
    before_img = Image.open(before_path).convert('RGB')
    after_img = Image.open(after_path).convert('RGB')
    diff = ImageChops.difference(before_img, after_img)  # 对比2张图片中像素不同的位置
    diff_positions = diff.getbbox()  # 获取图片差异位置坐标：左、上、右、下
    return diff_positions[0]  # 返回缺口的左边坐标，即为缺口滑块的左边界


def get_track(distance):
    '''
    根据移动距离生成轨迹模拟用户鼠标点击行为，加速度a、时间t、初速度v0：
    当前速度v = v0 + a·t
    距离s = v0·t + a·t²/2
    '''
    traces = []  # 记录鼠标每次移动的距离
    total_move = 0  # 当前位移
    midway = distance * 0.6  # 减速的距离阈值
    t = 0.2  # 移动时间
    v0 = 1  # 初始速度
    while total_move < distance:
        if total_move < midway:
            a = 5  # 加速阶段，加速度为正
        else:
            a = -3  # 减速阶段，加速度为负
        move = v0 * t + a * t * t / 2  # 计算当前移动距离
        v0 = v0 + a * t  # 计算当前速度
        total_move += move  # 更新当前位移
        traces.append(round(move))  # 记录每次移动的距离
    return traces


options = EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 防止打印无用的日志
browser = webdriver.Edge(options=options)
browser.maximize_window()

with open('../static/js/stealth.min.js') as f:  # 读取JavaScript脚本
    js = f.read()
browser.execute_cdp_cmd(  # 在browser请求网页前执行隐藏浏览器特征的开源JS脚本
    'Page.addScriptToEvaluateOnNewDocument',
    {'source': js}
)

try:
    browser.get(url)
    browser.add_cookie(cookies)
    browser.get(url)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'jigsawCanvas')))  # 等待Canvas背景图加载出来
    jigsawCanvas = browser.find_element(By.ID, 'jigsawCanvas')  # 定位Canvas背景图
    jigsawCanvas.screenshot(before_canvas_path)  # 截图保存不包含缺口的背景图

    action = webdriver.ActionChains(browser)  # 创建ActionChains对象执行滑动操作
    jigsawCircle = browser.find_element(By.ID, 'jigsawCircle')  # 获取圆形滑块按钮
    action.click_and_hold(jigsawCircle).move_by_offset(1, 0).release().perform()  # 轻微移动滑块按钮，显现出目标缺口
    browser.execute_script(vis_script.format('hidden'))  # 执行JS，隐藏移动滑块
    jigsawCanvas.screenshot(after_canvas_path)  # 截图保存包含缺口的背景图

    target_left = get_position_offset(before_canvas_path, after_canvas_path)  # 图片对比，计算获取缺口滑块的左边坐标
    missblock = browser.find_element(By.ID, 'missblock')  # 定义移动滑块
    miss_left = missblock.value_of_css_property('left')  # 获取移动滑块的style属性的左边坐标

    browser.execute_script(vis_script.format('visible'))  # 执行JS，重新显示拖动滑块，方便可视化移动过程、同时还原网站
    x_offset = target_left - float(miss_left[:-2])  # 计算目标缺口滑块和移动滑块的差值，得到滑块的偏移量，即需要移动的距离

    traces = get_track(x_offset)  # 得到滑块先加速后减速的移动轨迹
    action.click_and_hold(jigsawCircle)
    for x_trace in traces:
        if random.random() > 0.6:  # 模拟60%概率发生抖动
            y_offset = random.random() * 5
            if random.random() > 0.5:  # 模拟发生向上或向下移动各50%概率
                y_offset = -y_offset
        else:
            y_offset = 0
        action.move_by_offset(x_trace, y_offset)  # 横向先加速后减速，纵向上下随机抖动
    action.perform()  # 执行滑动操作
    time.sleep(random.random() * 2)
    action.release().perform()  # 等待片刻再释放鼠标

    time.sleep(random.random() * 3)
    browser.switch_to.alert.accept()  # 切换到alert弹出框并点击确定按钮
finally:
    time.sleep(random.random() * 5)  # 随机等待0~5秒、模拟用户行为
    print('mouse track randomly done')
    browser.quit()
