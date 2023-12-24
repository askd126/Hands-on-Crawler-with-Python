# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-24 18:27
@Project  :   Hands-on Crawler with Python-anti_crawler_with_slide_puzzle_captcha
拼图滑动验证码反爬
http://42.194.197.95:8001/captcha_slide_puzzle
http://42.194.197.95:8001/captcha_slide_puzzle_canvas
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

cookies = {
    'name': 'session',
    'value': '.eJyrViotTi1SsqpWyiyOT0zJzcxTsjLQUcrJTwexSopKU3WUcvOTMnNSlayUDM3gQEkHrDE-M0XJyhjCzkvMBSmKKTU3NbKIKTUzMjZXqq0FAN1MHbY.ZXcBDQ.EQ1PisBh-GQTUOfEjYBwWL3dRXw'
}


def simple_slide_puzzle():
    '''模拟简单滑块拼图验证码'''
    url = 'http://42.194.197.95:8001/captcha_slide_puzzle'

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

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'jigsawCircle')))  # 等待滑块按钮和滑轨加载出来
        jigsawCircle = browser.find_element(By.ID, 'jigsawCircle')  # 获取圆形滑块按钮

        action = webdriver.ActionChains(browser)  # 创建ActionChains对象执行滑动操作
        action.click_and_hold(jigsawCircle).move_by_offset(1, 0).release().perform()  # 轻微移动滑块按钮，显现出滑块和目标缺口
        # 移动滑块按钮后，等待targetblock元素属性会发生改变、出现style属性
        WebDriverWait(browser, 10).until(
            EC.element_attribute_to_include((By.ID, 'targetblock'), 'style'))
        # 同时，因为targetblock的style属性是动态加载的、加载后短时内left属性可能没有被JS运算获得、此时left为auto，需要等待style属性的left值不再为auto（变为xxxpx、同时后面跟有top值）时即为正确的left坐标像素值，此时可计算具体的移动距离
        WebDriverWait(browser, 20).until(
            EC.text_to_be_present_in_element_attribute((By.ID, 'targetblock'), 'style', 'px; top'))

        targetblock = browser.find_element(By.ID, 'targetblock')  # 定位目标滑块缺口
        missblock = browser.find_element(By.ID, 'missblock')  # 定位移动滑块
        target_left = targetblock.value_of_css_property('left')  # 获取目标缺口滑块的style属性的left值
        miss_left = missblock.value_of_css_property('left')  # 获取移动滑块的style属性的left值
        x_offset = float(target_left[:-2]) - float(miss_left[:-2])  # 计算目标缺口滑块和移动滑块的差值，得到滑块的偏移量，即需要移动的距离
        action.click_and_hold(jigsawCircle).move_by_offset(x_offset, 0).release().perform()  # 执行滑动操作

        time.sleep(random.random() * 5)
        browser.switch_to.alert.accept()  # 切换到alert弹出框并点击确定按钮
    finally:
        time.sleep(random.random() * 5)  # 随机等待0~5秒、模拟用户行为
        print('simple sliding puzzle done')
        browser.quit()


def get_position_offset(before_path, after_path):
    '''对比获取Canvas背景图中缺口的位置'''
    # 读取的图片是PngImageFile对象、为RGBA模式，需要转换为RGB模式，来使用ImageChops进行对比
    before_img = Image.open(before_path).convert('RGB')
    after_img = Image.open(after_path).convert('RGB')
    diff = ImageChops.difference(before_img, after_img)  # 对比2张图片中像素不同的位置
    diff_positions = diff.getbbox()  # 获取图片差异位置坐标：左、上、右、下
    return diff_positions[0]  # 返回缺口的左边坐标，即为缺口滑块的左边界


def canvas_slide_puzzle(before_canvas_path='../output/selenium/canvas_before.png',
                        after_canvas_path='../output/selenium/canvas_after.png'):
    '''模拟Canvas滑块拼图验证码'''
    url = 'http://42.194.197.95:8001/captcha_slide_puzzle_canvas'
    script = '''
    var crawler_missblock = document.getElementById("missblock");
    crawler_missblock.style["visibility"] = "{}";
    '''

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
        browser.get(url)  # 1.selenium访问网页

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'jigsawCanvas')))  # 等待Canvas背景图加载出来
        jigsawCanvas = browser.find_element(By.ID, 'jigsawCanvas')  # 2.定位Canvas背景图
        jigsawCanvas.screenshot(before_canvas_path)  # 3.截图保存不包含缺口的背景图

        action = webdriver.ActionChains(browser)  # 创建ActionChains对象执行滑动操作
        jigsawCircle = browser.find_element(By.ID, 'jigsawCircle')  # 获取圆形滑块按钮
        action.click_and_hold(jigsawCircle).move_by_offset(1, 0).release().perform()  # 4.轻微移动滑块按钮，显现出目标缺口
        browser.execute_script(script.format('hidden'))  # 5.执行JS，隐藏移动滑块
        jigsawCanvas.screenshot(after_canvas_path)  # 6.截图保存包含缺口的背景图

        target_left = get_position_offset(before_canvas_path, after_canvas_path)  # 7.图片对比，计算获取缺口滑块的左边坐标
        missblock = browser.find_element(By.ID, 'missblock')  # 定义移动滑块
        miss_left = missblock.value_of_css_property('left')  # 获取移动滑块的style属性的左边坐标

        browser.execute_script(script.format('visible'))  # 执行JS，重新显示拖动滑块，方便可视化移动过程、同时还原网站
        x_offset = target_left - float(miss_left[:-2])  # 计算目标缺口滑块和移动滑块的差值，得到滑块的偏移量，即需要移动的距离
        action.click_and_hold(jigsawCircle).move_by_offset(x_offset, 0).perform()  # 8.执行滑动操作
        time.sleep(random.random() * 2)
        action.release().perform()  # 等待片刻再释放鼠标

        time.sleep(random.random() * 3)
        browser.switch_to.alert.accept()  # 切换到alert弹出框并点击确定按钮
    finally:
        time.sleep(random.random() * 5)  # 随机等待0~5秒、模拟用户行为
        print('canvas sliding puzzle done')
        browser.quit()


if __name__ == '__main__':
    simple_slide_puzzle()
    # canvas_slide_puzzle()
