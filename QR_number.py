# # 作者：张健 Thomas Zhang
# # 时间：2024/6/29,21:50
# from PIL import Image, ImageDraw, ImageFont
# import random
# import string
#
#
# # 生成一个随机数字串，长度在5到15之间
# def generate_random_number_string(length):
#     return ''.join(random.choices(string.digits, k=length))
#
#
# # 生成图片的函数
# def generate_image(text, fonts, output_path):
#     # 创建一个空白图片
#     width, height = 400, 100
#     image = Image.new('RGB', (width, height), color='white')
#     draw = ImageDraw.Draw(image)
#
#     # 随机选择一种字体
#     font = ImageFont.truetype(random.choice(fonts), 40)
#
#     # 计算文本的宽度和高度
#     text_width, text_height = draw.textsize(text, font=font)
#
#     # 计算文本位置
#     x = (width - text_width) / 2
#     y = (height - text_height) / 2
#
#     # 绘制文本
#     draw.text((x, y), text, font=font, fill='black')
#
#     # 绘制边框
#     draw.rectangle([(0, 0), (width - 1, height - 1)], outline='black')
#
#     # 保存图片
#     image.save(output_path)
#
#
# # 主函数
# def main():
#     fonts = [
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-35-Thin.otf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-45-Light.otf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-55-Regular.otf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-65-Medium.otf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-75-SemiBold.otf',
#         '/Users/zhangjian/Library/Fonts/MSYHL.TTC',
#         '/Users/zhangjian/Library/Fonts/Baby\ Doll.otf',
#         '/Users/zhangjian/Library/Fonts/Autography.otf'
#     ]
#
#     for i in range(5):
#         length = random.randint(5, 15)
#         text = generate_random_number_string(length)
#         output_path = f'{i + 1}_{text}_.jpg'
#         generate_image(text, fonts, output_path)
#         print(f'Generated image {output_path} with text: {text}')
#
#
# if __name__ == "__main__":
#     main()

import os
from PIL import Image, ImageDraw, ImageFont
import random
import string
import time
import numpy as np
import tqdm

# 生成一个随机数字串，长度在5到15之间
def generate_random_number_string(length):
    return ''.join(random.choices(string.digits, k=length))


# 生成图片的函数
def generate_image(text, fonts, output_path):
    # 创建一个空白图片
    width, height = 800, 100
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    # 随机选择一种字体
    font_path = random.choice(fonts)

    # # 尝试不同的字体大小，确保文本不会超出图像的视野
    # max_font_size = 45
    # min_font_size = 35
    # for font_size in range(max_font_size, min_font_size - 1, -1):
    #     print(font_path)
    #     font = ImageFont.truetype(font_path, font_size)
    #     text_width, text_height = draw.textsize(text, font=font)
    #     if text_width <= width - 10 and text_height <= height - 10:  # 留出一些边距
    #         break
    # else:
    #     return

    font_size = 45
    font = ImageFont.truetype(font_path, font_size)



    # 计算文本的宽度和高度
    text_width, text_height = draw.textsize(text, font=font)

    # 计算文本位置
    center_x = (width - text_width) / 2
    center_y = (height - text_height) / 2
    center_y += -5
    # x += random.randint(-40, 40)
    # y += random.randint(10, 10)

    # # 定义最大偏移量，确保文本不会移到图片之外
    # max_offset_x = (width - text_width) / 2 - 10  # 10 是留出的边距
    # max_offset_y = (height - text_height) / 2 - 10  # 10 是留出的边距
    #
    # # 生成随机偏移量
    # offset_x = random.uniform(-max_offset_x, max_offset_x)
    # offset_y = random.uniform(-max_offset_y, max_offset_y)
    offset_x,offset_y = 0,0
    # 计算最终文本位置
    x = center_x + offset_x
    y = center_y + offset_y
    # 绘制文本
    draw.text((x, y), text, font=font, fill='black')

    # 绘制边框
    margin = 10  # 边框和文本的间距
    draw.rectangle(
        [x - margin, y - margin + 10, x + text_width + margin, y + text_height + margin],
        outline='black',
        width=random.randint(1, 2)
        # 边框的宽度
    )
    left = int((width - text_width - 40) / 2)
    top = int((height - text_height - 40) / 2)
    right = image.width - left
    bottom = image.height - top
    # 检查裁剪区域是否在图片范围内
    if left < 0 or top < 0 or right > image.width or bottom > image.height:
        print("裁剪区域超出了图片边界，请调整裁剪参数。")
    else:
        cropped_img = image.crop((left, top, right, bottom))

        # 定义旋转角度（逆时针方向）
        # 生成符合正态分布的随机角度
        mean = 0  # 均值
        stddev = 5  # 标准差
        random_angle = np.random.normal(mean, stddev)

        # 限制角度在 [-10, 10] 范围内
        random_angle = np.clip(random_angle, -5, 5)
        # 对图片进行旋转
        rotated_img = cropped_img.rotate(random_angle,fillcolor=(255, 255, 255))

        # 保存旋转后的图片
        # 保存图片
        rotated_img.save(output_path)

    return


# 主函数
def main():
    fonts = [
        '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-35-Thin.otf',
        '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-45-Light.otf',
        '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-55-Regular.otf',
        '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-65-Medium.otf',
        '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-75-SemiBold.otf',
        '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-3-35-Thin.ttf',
        '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-3-45-Light.ttf',
        '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-3-55-Regular.ttf',
        '/Users/zhangjian/Library/Fonts/MSYHL.TTC',
        '/Users/zhangjian/Library/Fonts/Autography.otf',
        '/System/Library/Fonts/Supplemental/Times New Roman.ttf',
        '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/System/Library/Fonts/Supplemental/Courier New.ttf',
        '/System/Library/Fonts/Supplemental/Trebuchet MS.ttf'
    ]

    dir = 'fifty_thousand/output_allfont_angle5/'
    for i in tqdm.tqdm(range(50000)):
        length = random.randint(5, 15)
        text = generate_random_number_string(length)
        # 获取当前时间戳（精确到秒）
        timestamp = int(time.time())
        output_path = dir + f'{timestamp}_{text}.png'
        generate_image(text, fonts, output_path)
        #print(f'Generated image {output_path} with text: {text}')


if __name__ == "__main__":
    main()
