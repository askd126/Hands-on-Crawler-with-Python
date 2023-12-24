# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-24 11:14
@Project  :   Hands-on Crawler with Python-anti_crawler_with_simple_graphic_captcha
简单图形验证码反爬
'''

import cv2
import paddlehub as hub
from PIL import Image


def recognize_captcha(image_path, model_name='chinese_ocr_db_crnn_server', threshold=160):
    '''
    图片二值化处理并识别验证码
    :param image_path: 图片路径
    :param model_name: 模型名
    :param threshold: 二值化阈值
    :return: 识别结果
    '''
    # 1.读取并处理图片
    gray_image = Image.open(image_path).convert('L')  # 读取图片
    image_table = [0 if i < threshold else 1 for i in range(256)]  # 定义二值化表
    image = gray_image.point(image_table, '1')  # 二值化映射
    image.save(image_path.replace('.png', '_binary.png'))
    # image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

    image = cv2.imread(image_path.replace('.png', '_binary.png'))  # 读取图片
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # 转为灰度图
    # _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY) # 对灰度图像进行二值化处理
    # binary_image = np.expand_dims(binary_image, -1)

    # 2.加载模型
    model = hub.Module(name=model_name) # 加载模型，相关模型文件和代码会保存到~/.paddlehub/modules/

    # 3.调用模型进行识别
    results = model.recognize_text(images=[image])
    return results


if __name__ == '__main__':
    image_path = '../data/imgs/captcha/Q6JR.png'
    results = recognize_captcha(image_path, threshold=128)
    print(results)
