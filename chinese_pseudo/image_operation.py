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
    rotated_image = image.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=255)

    return rotated_image

import cv2
import numpy as np
from PIL import Image

def apply_perspective_transform(image):
    # 将图像转换为 NumPy 数组
    image = np.array(image)

    # 获取图像的大小
    height, width = image.shape[:2]

    # 定义原始四个角点
    pts1 = np.float32([[0, 0], [width-1, 0], [0, height-1], [width-1, height-1]])

    # 定义透视变换后的四个角点
    pts2 = np.float32([[np.random.uniform(0, width*0.2), np.random.uniform(0, height*0.2)],
                       [np.random.uniform(width*0.8, width), np.random.uniform(0, height*0.2)],
                       [np.random.uniform(0, width*0.2), np.random.uniform(height*0.8, height)],
                       [np.random.uniform(width*0.8, width), np.random.uniform(height*0.8, height)]])

    # 计算透视变换矩阵
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # 应用透视变换
    #dst = cv2.warpPerspective(image, matrix, (width, height))
    dst = cv2.warpPerspective(image, matrix, (width, height), borderValue=(255, 255, 255))

    # 返回变换后的图像
    return Image.fromarray(dst)