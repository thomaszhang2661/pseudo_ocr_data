# 作者：张健 Thomas Zhang
# 时间：2024/10/18,09:20
"""这个模块的功能是按照自动化所的字典和电脑中的字体制作单个汉字的伪数据"""

##############################
'''第一部分提取字典内容'''
import pickle
from tqdm import tqdm
import numpy as np


####################
# """第二部分根据字体和字典生成伪数据"""
import regex as re
import os
import random
#import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager



texts_dict = {}
with open('merged_dict_new.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # 使用 split() 和 strip() 来分割和去除换行符
        char, value = line.strip().split(" : ", 1)
        texts_dict[char] = value


# def is_chinese_char(char):
#     return '\u4e00' <= char <= '\u9fff'


def is_blank_image(image, threshold=5):
    pixels = np.array(image)

    # 计算图片中所有像素与白色（255, 255, 255）的差异
    diff = np.abs(pixels - 255)
    diff_sum = np.sum(diff)

    # 如果所有像素都与白色像素差异小于阈值，则认为是空白图像
    if diff_sum < threshold:
        return True
    return False


def crop_off_whitespace(image):
    # 转换为灰度图像
    gray_image = image.convert('L')

    # 转为NumPy数组
    image_array = np.array(gray_image)

    # 动态计算阈值或固定阈值
    #threshold = np.max(image_array)
    threshold = 100
    # 计算每一行和列的灰度值之和
    horizontal_sum = np.sum(image_array < threshold, axis=1)
    vertical_sum = np.sum(image_array < threshold, axis=0)

    # 查找非空白行和列
    rows = np.where(horizontal_sum > 0)[0]
    cols = np.where(vertical_sum > 0)[0]

    # 检查是否存在非空白区域
    if rows.size == 0 or cols.size == 0:
        return image  # 如果全是空白，返回原图

    # 获取裁剪边界
    # 获取裁剪边界
    top, bottom = rows[0], rows[-1]
    left, right = cols[0], cols[-1]

    # 计算适当的边距，避免裁剪掉内容
    h_margin = max(0, int((bottom - top) * 0.05))  # 边距可以调整为5%
    w_margin = max(0, int((right - left) * 0.05))  # 边距可以调整为5%

    top = max(0, top - h_margin)
    bottom = min(image_array.shape[0], bottom + h_margin)
    left = max(0, left - w_margin)
    right = min(image_array.shape[1], right + w_margin)
    # 裁剪图像
    cropped_image = image.crop((left, top, right, bottom))

    # 恢复原图像模式
    if image.mode != 'L':
        cropped_image = cropped_image.convert(image.mode)

    return cropped_image


# 设置图片尺寸和字体大小
image_width = 300
image_height = 300
font_size = 70

# # 用户字体目录（请根据实际路径进行修改）
#user_font_dir = os.path.expanduser("/Users/zhangjian/Library/Fonts")
# user_font_dir = os.path.expanduser("/System/Library/Fonts")
#user_font_dir = os.path.expanduser("/Users/zhangjian/Downloads/free-font-master/assets/font/中文/selected_hw/")
#user_font_dir = "C:/Users/ThomasZhang/Downloads/办公常用字体-网盘"  #"/Volumes/Samsung SSD/字体/办公常用字体-网盘/"
#user_font_dir = "D:/字体/selected_hw"
user_font_dir = "/database/selected_hw/"
#user_font_dir = os.path.expanduser("/Users/zhangjian/Downloads/free-font-master/assets/font/中文/selected/")

# 定义用于保存生成图片的输出目录
#output_dir = "../../pseudo_chinese_images_1213"
#output_dir = "C:/Users/ThomasZhang/PycharmProjects/pseudo_chinese_images_1218/"  #"/Volumes/Samsung SSD/字体/1213_font/"
output_dir = "/database/single_font_1218/"
os.makedirs(output_dir, exist_ok=True)
# 获取系统中已安装的字体列表
installed_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=user_font_dir)
#installed_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

# 列出所有已安装的字体
font_list = matplotlib.font_manager.findSystemFonts()
font_list = font_list
for font in font_list:
    print(font)
# 创建空列表存储有效的字体文件
valid_fonts = []

# 遍历已安装的字体列表，筛选出支持所需字符的字体
for font_path in installed_fonts:
    try:
        font = ImageFont.truetype(font_path, font_size)

        # 检查字体是否支持所有字符
        # if all(font.getsize(char)[0] != 0 for char in texts):
        #     valid_fonts.append(font)
        #pattern = r'/([^/]+)\.'
        pattern = r'[^/]+(?=\.[^.]+$)'

        matches = re.finditer(pattern, font_path)


        # 遍历所有匹配项
        for match in matches:
            matched_text = match.group()

            # 检查匹配的文本是否在 select_list 中
            #if matched_text in select_list:
            print(matched_text)
            font = ImageFont.truetype(font_path, font_size)
            valid_fonts.append((font, matched_text))



    except Exception as e:
        print(f"Error loading font file: {font_path}")
        print(e)

# 打印有效的字体文件列表
print(f"有效字体数量: {len(valid_fonts)}")

# 遍历文本列表，为每个文本使用不同的字体生成图片并保存

for ind_f, font in tqdm(enumerate(valid_fonts), total=len(valid_fonts)):
    for text_group, index in texts_dict.items():
        sub_file_name = int(index)
        sub_file_name = f"{sub_file_name:05d}"
        sub_file_name = sub_file_name+"_fnt"
        sub_path = output_dir + str(sub_file_name) #os.path.join(output_dir, str(sub_file_name))
        os.makedirs(sub_path, exist_ok=True)
        sub_path = sub_path + '/'
        #text_width, text_height = font[0].getsize(text_group)
        text_width, text_height = font[0].getbbox(text_group)[2] - font[0].getbbox(text_group)[0], \
                                 font[0].getbbox(text_group)[3] - font[0].getbbox(text_group)[1]

        # 动态计算图片尺寸
        if text_width == 0 or text_height == 0:
            continue

        # 调整图片尺寸以适应文本
        image_width = text_width + 100
        image_height = text_height + 100
        image = Image.new("RGB", (image_width, image_height), color="white")
        draw = ImageDraw.Draw(image)

        # 计算文本位置
        x = (image_width - text_width) / 2
        y = (image_height - text_height) / 2

        # 绘制文本
        # if 语句确保字体没问题，否则可能出现空白图片
        # if font[0].getsize(text_group)[0] > 0:
        #     draw.text((x, y), text_group, fill="black", font=font[0])
        # else:
        #     continue
        bbox = font[0].getbbox(text_group)
        text_width = bbox[2] - bbox[0]  # right - left

        if text_width > 0:
            draw.text((x, y), text_group, fill="black", font=font[0])
        else:
            continue

        if not is_blank_image(image):
            # 保存图像
            # 剪裁四周多余空白
            font_name = font[1].replace(' ', '_').split("\\")[-1]
            #image.save(f'{sub_path}{font_name}_{ind_f}_{index}_origin.jpg')
            image = crop_off_whitespace(image)
            width, height = image.size
            #ratio = min(font_size/width, font_size/height)
            #image = image.resize((int(width*ratio), int(height*ratio)), Image.ANTIALIAS)

            image_filename =f'{sub_path}{font_name}_{ind_f}_{index}.jpg' #os.path.join(sub_path, f"{font[1]}_{ind_f}_{index}.jpg")
            try:
                image.save(image_filename)
            except Exception as e:
                print(f"Error saving image: {image_filename}")
                print(e)

            # 打印生成的信息
            #print(f"生成图像 {image_filename}，文本: {text_group}，字体: {font[1]}")
