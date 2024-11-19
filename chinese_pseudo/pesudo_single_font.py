# 作者：张健 Thomas Zhang
# 时间：2024/10/18,09:20
"""这个模块的功能是按照自动化所的字典和电脑中的字体制作单个汉字的伪数据"""

##############################
'''第一部分提取字典内容'''
import pickle
from tqdm import tqdm
import numpy as np


# 加载需要制作哪些汉字的字典
# with open('chinese_data1018/char_dict', 'rb') as f:
#     char_dict = pickle.load(f)
# print(char_dict)

# from fontTools.ttLib import TTFont
#
#
# def extract_chinese_characters(font_path, font_number=0):
#     # 打开字体文件
#     font = TTFont(font_path, fontNumber=font_number)
#
#     # 获取字形表
#     cmap = font['cmap'].tables[0].cmap
#
#     # 提取所有汉字字符
#     chinese_chars = []
#     for codepoint, glyph_name in cmap.items():
#         if 0x4E00 <= codepoint <= 0x9FFF:  # CJK Unified Ideographs
#             chinese_chars.append(chr(codepoint))
#
#     return chinese_chars
#
#
#
# # 示例字体文件路径
# font_path = "/System/Library/Fonts/PingFang.ttc"  # 替换为实际的字体文件路径
#
# # 提取中文字符
# chinese_characters = extract_chinese_characters(font_path, font_number=0)
#
# # 打印中文字符
# print("提取的中文字符:")
# print(''.join(chinese_characters))
# print(len(chinese_characters))

####################
# """第二部分根据字体和字典生成伪数据"""
import regex as re
import os
import random
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager
import pickle

# 定义用于保存生成图片的输出目录
output_dir = "../../pseudo_chinese_images_1118_熠"
os.makedirs(output_dir, exist_ok=True)

# 读取字符字典
# with open('chinese_data1018/char_dict', 'rb') as f:
#     char_dict = pickle.load(f)
#
# # 从字符字典中提取字符
# texts = list(char_dict.keys())  # char_dict 的键是想要的字符
char_dict = {}
with open('char_dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        char, code = line.strip().split('\t')  # 按制表符分割
        char_dict[char] = int(code)  # 将编码转换为整数

texts = list(char_dict.keys())

def is_chinese_char(char):
    return '\u4e00' <= char <= '\u9fff'

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
    # 转换为NumPy数组
    # 将图像转换为灰度
    gray_image = image.convert('L')
    image_array = np.array(gray_image)
    threshold = 220
    # 计算每一行和每一列的灰度值之和
    horizontal_sum = np.sum(image_array < threshold, axis=1)
    vertical_sum = np.sum(image_array < threshold, axis=0)

    # 找到上边界和下边界
    top = np.argmax(horizontal_sum > 0)
    bottom = len(horizontal_sum) - np.argmax(horizontal_sum[::-1] > 0)

    # 找到左边界和右边界
    left = np.argmax(vertical_sum > 0)
    right = len(vertical_sum) - np.argmax(vertical_sum[::-1] > 0)

    # 裁剪图像
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

# 设置图片尺寸和字体大小
image_width = 300
image_height = 300
font_size = 70

# # 用户字体目录（请根据实际路径进行修改）
#user_font_dir = os.path.expanduser("/Users/zhangjian/Library/Fonts")
# user_font_dir = os.path.expanduser("/System/Library/Fonts")
user_font_dir = os.path.expanduser("/Users/zhangjian/Downloads/free-font-master/assets/font/中文/selected_hw/")
#user_font_dir = os.path.expanduser("/Users/zhangjian/Downloads/free-font-master/assets/font/中文/selected/")

# 获取系统中已安装的字体列表
installed_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=user_font_dir, fontext='ttf')
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

        ################################
        # 打印所有含有汉字的字体
        # for match in matches:
        #     matched_text = match.group()  # 提取匹配的字符串
        #     if any(is_chinese_char(char) for char in matched_text):
        #         print(matched_text)  # 输出匹配的汉字

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

for font in tqdm(valid_fonts):
    for text_group in texts:
        if text_group != "熠":
            continue
        # image = Image.new("RGB", (image_width, image_height), color="white")
        # draw = ImageDraw.Draw(image)

        # 计算文本的大小和位置
        #text_width, text_height = draw.textsize(text_group, font=font[0])
        #text_width0, text_height_0 = draw.textsize(" ", font=font[0])
        text_width, text_height = font[0].getsize(text_group)
        # 动态计算图片尺寸
        if text_width == 0 or text_height == 0:
            continue

        # 调整图片尺寸以适应文本
        image_width = text_width + 10
        image_height = text_height + 10
        image = Image.new("RGB", (image_width, image_height), color="white")
        draw = ImageDraw.Draw(image)

        # 计算文本位置
        x = (image_width - text_width) / 2
        y = (image_height - text_height) / 2

        # 绘制文本
        # if 语句确保字体没问题，否则可能出现空白图片
        if font[0].getsize(text_group)[0] > 0:
            draw.text((x, y), text_group, fill="black", font=font[0])
        else:
            continue


        if not is_blank_image(image):
        # 保存图像
            # 剪裁四周多余空白
            #image = crop_off_whitespace(image)
            image_filename = os.path.join(output_dir, f"{font[1]}_{text_group}.jpg")
            image.save(image_filename)

            # 打印生成的信息
            #print(f"生成图像 {image_filename}，文本: {text_group}，字体: {font[1]}")

############################
# """查找系统中的汉字字体"""
# import os
# import regex as re
# import matplotlib.font_manager
#
#
# # # # 用户字体目录（请根据实际路径进行修改）
# user_font_dir = os.path.expanduser("/Users/zhangjian/Library/Fonts")
# # 获取系统中已安装的字体列表
# installed_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=user_font_dir, fontext='ttf')
#
# # 创建空列表存储有效的字体文件
# valid_fonts = []
#
# # 遍历已安装的字体列表，筛选出支持所需字符的字体
# for font_path in installed_fonts:
#     try:
#         #font = ImageFont.truetype(font_path, font_size)
#         # 检查字体是否支持所有字符
#         # if all(font.getsize(char)[0] != 0 for char in texts):
#         #     valid_fonts.append(font)
#         #pattern = r'/([^/]+)\.'
#         pattern = r'[^/]+(?=\.[^.]+$)'
#
#         matches = re.finditer(pattern, font_path)
#
#         for match in matches:
#             matched_text = match.group()  # 提取匹配的字符串
#             if any(is_chinese_char(char) for char in matched_text):
#                 print(matched_text)  # 输出匹配的汉字
#
#         # # 遍历所有匹配项
#         # for match in matches:
#         #     matched_text = match.group()
#         #
#         #     # 检查匹配的文本是否在 select_list 中
#         #     if matched_text in select_list:
#         #         print(matched_text)
#         #         font = ImageFont.truetype(font_path, font_size)
#         #         valid_fonts.append(font)
#
#     except Exception as e:
#         print(f"Error loading font file: {font_path}")
#         print(e)
#
# # 打印有效的字体文件列表
# print(f"有效字体数量: {len(valid_fonts)}")

######################################

