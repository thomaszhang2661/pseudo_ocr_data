# 作者：张健 Thomas Zhang
# 时间：2024/10/18,09:20
"""这个模块的功能是按照自动化所的字典和电脑中的字体制作单个汉字的伪数据"""

##############################
'''第一部分提取字典内容'''
import pickle
from tqdm import tqdm


# 加载需要制作哪些汉字的字典
with open('chinese_data1018/char_dict', 'rb') as f:
    char_dict = pickle.load(f)
print(char_dict)

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
output_dir = "../../pseudo_chinese_print_images"
os.makedirs(output_dir, exist_ok=True)

# 读取字符字典
with open('chinese_data1018/char_dict', 'rb') as f:
    char_dict = pickle.load(f)

# 从字符字典中提取字符
texts = list(char_dict.keys())  # char_dict 的键是想要的字符

def is_chinese_char(char):
    return '\u4e00' <= char <= '\u9fff'

# 定义要使用的字体列表
select_list = ["Wawati SC","Baoli SC"]
# select_list = [
#     "田英章硬笔楷书简体",
#     "锐字云字库行草体",
#     "于洪亮钢笔楷书简体",
#     "汉仪平安行简",
#     "钟齐吴嘉睿手写字",
#     "庞中华硬笔行书",
#     "汉仪伊宁隶简",
#     "钟齐余好建行艺体",
#     "方正字迹-子实行楷简体",
#     "方正字迹-刘毅硬笔行书简体",
#     "游狼美钢行书简",
#     "方正字迹-刘郢硬笔简体",
#     "陈旭东字体",
#     "逐浪大雪钢笔体",
#     "国祥手写体",
#     "全新硬笔楷书简",
#     "邢世新硬笔行书简体",
#     "钟齐立强行书简",
#     "汉仪晨妹子",
#     "孙运和酷楷",
#     "建刚草稿体",
#     "钟齐陈伟勋硬笔行书字库",
#     "方正字迹-刘毅硬笔楷书简体",
#     "平方雨桐体",
#     "陈继世硬笔行书",
#     "禹卫硬笔字体",
#     "字体管家印象体",
#     "默陌信笺手写体",
#     "蔡云汉硬笔行书简书法字体",
#     "林志秀硬笔楷书",
#     "于洪亮硬笔行楷手写字体",
#     "钟齐山文丰手写体",
#     "方正字迹-张亮硬笔行书简体",
#     "方正瘦金书简体",
#     "游狼软笔楷书",
#     "方正硬笔楷书简体",
#     "逐浪时尚钢笔体",
#     "庞中华简体",
#     "方正硬笔行书简体",
#     "逐浪小雪钢笔体",
#     "钟齐孟宪敏钢笔简体",
#     "方正字迹-杜慧田硬笔楷书简体",
#     "方正字迹-朱涛钢笔行书简体",
#     "汉仪瘦金书简",
#     "字体管家简行",
#     "方正字迹-王伟钢笔行书简体",
#     "字体管家青葱体",
#     "新蒂绿豆体",
#     "北风钢笔楷书"
# ]


# 设置图片尺寸和字体大小
image_width = 300
image_height = 300
font_size = 60

# # 用户字体目录（请根据实际路径进行修改）
#user_font_dir = os.path.expanduser("/Users/zhangjian/Library/Fonts")
# user_font_dir = os.path.expanduser("/System/Library/Fonts")
user_font_dir = os.path.expanduser("/Users/zhangjian/Downloads/free-font-master/assets/font/中文/selected/")
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
        # 每10个汉字一组
    #for idx in range(0, len(texts), 10):
        # # 获取当前组的汉字文本
        # text_group = ''.join(texts[idx:idx + 10])
        #
        # # 计算生成的图像数量（以文本中汉字的总数除以10）
        # num_images = len(texts) // 10 + (1 if len(texts) % 10 > 0 else 0)
        #
        # for idx in range(num_images):
            # 随机抽取10个汉字
            #text_group = ''.join(random.sample(texts, min(10, len(texts))))
            # 创建一张空白图片
        for text_group in texts:
            image = Image.new("RGB", (image_width, image_height), color="white")
            draw = ImageDraw.Draw(image)

            # 计算文本的大小和位置
            text_width, text_height = draw.textsize(text_group, font=font[0])
            text_width0, text_height_0 = draw.textsize(" ", font=font[0])

            # 调整图片尺寸以适应文本
            image_width = text_width + 10
            image_height = text_height + 10
            image = Image.new("RGB", (image_width, image_height), color="white")
            draw = ImageDraw.Draw(image)

            # 计算文本位置
            x = (image_width - text_width) / 2
            y = (image_height - text_height) / 2 - 2

            # 绘制文本
            draw.text((x, y), text_group, fill="black", font=font[0])

            # Add underline

            #under_line_hight = max(2, int(image_height / 32))
            #underline_y = random.randint(int(y + 0.9 * text_height), int(y + 1.1 * text_height)) # Adjust 2 according
            # to your
            # preference
            #underline_y = min(underline_y, image_height - 10)
            #draw.line([(x, underline_y), (x + text_width, underline_y)], fill="black",
            #          width=under_line_hight)  # Adjust width as needed

            # 保存图像
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