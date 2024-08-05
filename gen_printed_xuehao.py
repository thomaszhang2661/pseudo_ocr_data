# from PIL import Image, ImageDraw, ImageFont
# import numpy as np
# import random
# import string
# import os
# import time
# import tqdm
#
#
# # 生成一个随机数字串，长度在5到15之间
# def generate_random_number_string(length):
#     return ''.join(random.choices(string.digits, k=length))
#
#
# def generate_image(text, fonts, output_path):
#     num_digits = len(text)
#     cell_width = 52
#     width = cell_width * num_digits
#     height = 82
#
#     # 创建一个背景图像
#     image = Image.new('RGB', (width, height), color='white')
#     draw = ImageDraw.Draw(image)
#
#     font_path = random.choice(fonts)
#     font_size = 45
#     font = ImageFont.truetype(font_path, font_size)
#
#     digit_positions = []
#
#     for i, number in enumerate(text):
#         digit_image = Image.new('L', (cell_width, height), color=255)
#         digit_draw = ImageDraw.Draw(digit_image)
#         digit_draw.text((cell_width // 4, height // 4), number, font=font, fill=0)
#
#         scaled_w = int(cell_width * random.uniform(0.7, 1.0))
#         scaled_h = int(height * random.uniform(0.7, 1.0))
#         digit_image = digit_image.resize((scaled_w, scaled_h), Image.ANTIALIAS)
#
#         offset_x = random.randint(0, cell_width - scaled_w)
#         offset_y = random.randint(0, height - scaled_h)
#         paste_position = (i * cell_width + offset_x, offset_y)
#         image.paste(digit_image, paste_position)
#
#         digit_positions.append((i * cell_width + offset_x, offset_y, scaled_w, scaled_h))
#
#     # 绘制竖直虚线
#     line_spacing = 10
#     for i in range(1, num_digits):
#         line_x = i * cell_width
#         if any(line_x > x and line_x < x + w for (x, y, w, h) in digit_positions):
#             continue
#         for y_dash in range(0, height, line_spacing):
#             draw.line([(line_x, y_dash), (line_x, min(y_dash + line_spacing // 2, height))], fill='black')
#
#     # 绘制边框
#     margin = 10
#     draw.rectangle(
#         [0, 0, width - 1, height - 1],
#         outline='black',
#         width=1
#     )
#
#     # 添加额外的边距来确保图像完整
#     left_margin = 15
#     right_margin = 15
#     top_margin = 15
#     bottom_margin = 15
#     larger_width = width + left_margin + right_margin
#     larger_height = height + top_margin + bottom_margin
#     larger_image = Image.new('RGB', (larger_width, larger_height), color='white')
#
#     # 创建一个实心矩形框
#     draw_larger = ImageDraw.Draw(larger_image)
#     draw_larger.rectangle(
#         [0, 0, larger_width - 1, larger_height - 1],
#         fill='black'  # 实心矩形的填充颜色
#     )
#
#     larger_image.paste(image, (left_margin, top_margin))
#
#     # 生成旋转角度并旋转图像
#     # mean = 0
#     # stddev = 5
#     # random_angle = np.random.normal(mean, stddev)
#     # random_angle = np.clip(random_angle, -5, 5)
#     # rotated_img = larger_image.rotate(random_angle, fillcolor='white')
#
#     larger_image.save(output_path)
#
#
# def main():
#     fonts = [
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-35-Thin.otf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-45-Light.otf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-55-Regular.otf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-65-Medium.otf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-2-75-SemiBold.otf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-3-35-Thin.ttf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-3-45-Light.ttf',
#         '/Users/zhangjian/Library/Fonts/AlibabaPuHuiTi-3-55-Regular.ttf',
#         '/Users/zhangjian/Library/Fonts/MSYHL.TTC',
#         '/Users/zhangjian/Library/Fonts/Autography.otf',
#         '/System/Library/Fonts/Supplemental/Times New Roman.ttf',
#         '/System/Library/Fonts/Supplemental/Arial.ttf',
#         '/System/Library/Fonts/Supplemental/Courier New.ttf',
#         '/System/Library/Fonts/Supplemental/Trebuchet MS.ttf',
#         '/Users/zhangjian/Library/Fonts/MSYHL.TTC',
#         '/System/Library/Fonts/PingFang.ttc',
#         '/System/Library/Fonts/Courier.dfont'
#     ]
#
#     dir = './output/'
#     os.makedirs(dir, exist_ok=True)
#
#     for i in tqdm.tqdm(range(100)):
#         length = random.randint(5, 15)
#         text = generate_random_number_string(length)
#         timestamp = int(time.time())
#         output_path = os.path.join(dir, f'{timestamp}_{text}.png')
#         generate_image(text, fonts, output_path)
#
#
# if __name__ == "__main__":
#     main()

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import string
import os
import time
import tqdm
from gen_scratch import apply_scratches


# 生成一个随机数字串，长度在5到15之间
def generate_random_number_string(length):
    return ''.join(random.choices(string.digits, k=length))


def generate_image(text, fonts, dir):
    num_digits = len(text)
    #cell_width = 52
    cell_width = 40
    width = cell_width * num_digits
    height = 64
    #height = 82
    list_of_text = list(text)

    # 创建一个背景图像
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    font_path = random.choice(fonts)
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)

    digit_positions = []

    for i, number in enumerate(text):
        digit_image = Image.new('L', (cell_width, height), color=255)
        digit_draw = ImageDraw.Draw(digit_image)

        digit_draw.text((cell_width // 4, height // 10), number, font=font, fill=0)

        scaled_w = int(cell_width * random.uniform(0.9, 1.0))
        scaled_h = int(height * random.uniform(0.9, 1.0))
        digit_image = digit_image.resize((scaled_w, scaled_h), Image.ANTIALIAS)

        # 加入涂抹
        if random.choice((0,1,2,3,4,5,6,7,8,9,10)) == 0:
            digit_image = apply_scratches(digit_image)
            # 修改标注文件
            list_of_text[i] = 'x'


        offset_x = random.randint(0, cell_width - scaled_w)
        offset_y = random.randint(0, height - scaled_h)
        #offset_y = max(-10,offset_y -10)
        paste_position = (i * cell_width + offset_x, offset_y)
        image.paste(digit_image, paste_position)

        digit_positions.append((paste_position[0], paste_position[1], scaled_w, scaled_h))

    # 绘制竖直虚线
    line_spacing = 10
    for i in range(1, num_digits):
        line_x = i * cell_width
        if any(line_x > x and line_x < x + w for (x, y, w, h) in digit_positions):
            continue
        for y_dash in range(0, height, line_spacing):
            draw.line([(line_x, y_dash), (line_x, min(y_dash + line_spacing // 2, height))], fill='black')

    # 添加边距
    left_margin = 15
    right_margin = 15
    top_margin = 15
    bottom_margin = 15
    larger_width = width + left_margin + right_margin
    larger_height = height + top_margin + bottom_margin

    # 创建一个带有边距的图像
    larger_image = Image.new('RGB', (larger_width, larger_height), color='white')

    # 将生成的图像粘贴到大图上
    larger_image.paste(image, (left_margin, top_margin))

    # 在大图上绘制一个黑色矩形框
    draw_larger = ImageDraw.Draw(larger_image)
    draw_larger.rectangle(
        [left_margin, left_margin, larger_width - left_margin, larger_height - left_margin],
        outline='black',  # 边框颜色
        width=2  # 边框宽度
    )

    # 绘制内边框，使其留白区域在图像四周
    # draw_larger.rectangle(
    #     [left_margin - 1, top_margin - 1, larger_width - right_margin, larger_height - bottom_margin],
    #     fill='white'
    # )

    # 将生成的图像粘贴到大图上
    #larger_image.paste(image, (left_margin, top_margin))

    # 保存最终图像
    timestamp = int(time.time())
    test_new = "".join(list_of_text)
    output_path = os.path.join(dir, f'{timestamp}_{test_new}.png')
    larger_image.save(output_path)


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
        '/System/Library/Fonts/Supplemental/Trebuchet MS.ttf',
        '/Users/zhangjian/Library/Fonts/MSYHL.TTC',
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/Courier.dfont'
    ]

    dir = '../pseudo_ocr_data_xuehao/printed_xuehao/'
    os.makedirs(dir, exist_ok=True)

    for i in tqdm.tqdm(range(10000)):
        length = random.randint(5, 15)
        text = generate_random_number_string(length)

        generate_image(text, fonts,dir)


if __name__ == "__main__":
    main()
