# 作者：张健 Thomas Zhang
# 时间：2024/11/7,21:48

import numpy as np
from PIL import Image, ImageDraw, ImageFont

def rotate_text_image(image, angle=5):
    """
    对给定的图像应用旋转变换，不改变图像的拓扑结构。
    :param image: 要旋转的图像
    :param angle: 旋转的角度（单位：度）
    :return: 旋转后的图像
    """
    # 获取图像的尺寸
    width, height = image.size

    # 计算旋转后图像的尺寸
    rotated_image = image.rotate(angle, resample=Image.BICUBIC, expand=True)

    return rotated_image