# """
# 作者：张健
# 时间：2024.10.20
# 这个模块制造伪的行数据，基于单个中文字，随机添加删除符号
# """
#
# from PIL import Image, ImageDraw
# import numpy as np
# import random
# # import string
# # import tensorflow as tf
# import time
# import multiprocessing
# import os
# from tqdm import tqdm
# import cv2  # OpenCV库，用于更快的图像处理
# from gen_scratch import apply_scratches
# import pickle
#
# # 加载需要制作哪些汉字的字典
# with open('chinese_data1018/char_dict', 'rb') as f:
#     char_dict = pickle.load(f)
# # 从字符字典中提取字符
# dict_list = list(char_dict.keys())
#
# def generate_random_line(length):
#     return ''.join(random.choices(dict_list, k=length))
#
#
# def load_local_images(image_directory):
#     """这个函数根据单子数据添加到一个字典结构中"""
#     mnist_data = {}
#     for filename in os.listdir(image_directory):
#         if filename.endswith('.jpg'):
#             # 根据文件名称提取标注，中文标注第一部分是字体名称，第二部分是标注内容
#             font_name, label = filename.split('_', 1)
#             label = label.split('.')[0]
#             filepath = os.path.join(image_directory, filename)
#             if label not in mnist_data:
#                 mnist_data[label] = []
#             image = Image.open(filepath).convert('L')  # 转为灰度图
#             mnist_data[label].append(np.array(image))
#     return mnist_data
#
#
# def create_handwritten_number_image(line_chars, output_path, mnist_data):
#     list_of_text = list(line_chars)
#     width = 70 * len(line_chars)
#     height = 70
#     cell_width = width // len(line_chars)
#
#     # 创建白色背景的新图像
#     image = Image.new('L', (width, height), 255)
#     draw = ImageDraw.Draw(image)
#
#     # rand_dash_all = random.randint(6, 9)
#     # rand_dash_inter = random.randint(1, 3)
#     # rand_dash_select = 1
#
#     for i, text_char in enumerate(line_chars):
#
#         if text_char not in mnist_data:
#             print(f"未找到字符的图像：{text_char}")
#             continue
#
#         char_images = mnist_data[text_char]
#         single_image = char_images[np.random.choice(len(char_images))]
#
#         # 调整颜色和大小
#         scaled_w = int(width / len(line_chars) * random.uniform(0.85, 1.0))
#         scaled_h = int(height * random.uniform(0.85, 1.0))
#         single_image = cv2.resize(single_image, (scaled_w, scaled_h), interpolation=cv2.INTER_LINEAR)
#         single_image = Image.fromarray(single_image)
#
#         # 加入划痕
#         if random.choice(range(11)) == 0:
#             single_image = apply_scratches(single_image)
#             list_of_text[i] = 'x'
#
#         offset_x = random.randint(0, width // len(line_chars) - scaled_w)
#         offset_y = random.randint(0, height - scaled_h)
#         paste_position = (i * cell_width + offset_x, offset_y)
#         image.paste(single_image, paste_position)
#
#         # # 绘制竖线
#         # if rand_dash_select == 1 and i > 0:
#         #     for y_dash in range(0, height, rand_dash_all):
#         #         draw.line([(i * cell_width, y_dash), (i * cell_width, y_dash + rand_dash_inter)], fill=0)
#         # elif rand_dash_select == 2 and i > 0:
#         #     draw.line([(i * cell_width, 0), (i * cell_width, height)], fill=0)
#
#     #draw.rectangle([0, 0, width - 1, height - 1], outline=0, width=3)
#
#     # 添加边距
#     left_margin = 15
#     right_margin = 15
#     top_margin = 15
#     bottom_margin = 15
#     larger_width = width + left_margin + right_margin
#     larger_height = height + top_margin + bottom_margin
#     larger_image = Image.new('L', (larger_width, larger_height), 255)
#     larger_image.paste(image, (left_margin, top_margin))
#
#     # random_angle = np.clip(np.random.normal(0, 5), -3, 3)
#     # rotated_img = larger_image.rotate(random_angle, fillcolor=(255))
#
#     # 保存图像
#     timestamp = int(time.time())
#     text_new = "".join(list_of_text)
#     output_file = f'{output_path}{timestamp}_{text_new}.jpg'
#     #rotated_img.save(output_file)
#
#     larger_image.save(output_file)
#
# def process_image_wrapper(args):
#     output_path, text, mnist_data = args
#     create_handwritten_number_image(text, output_path, mnist_data)
#     return output_path
#
#
# if __name__ == '__main__':
#     random.seed(42)
#     image_directory = '/Users/zhangjian/PycharmProjects/pseudo_chinese_print_images'
#
#     # 加载单个汉字图片
#     mnist_data = load_local_images(image_directory)
#     output_paths_and_texts = []
#     for i in range(200000):
#         length = random.randint(15, 20)
#         # 生成一串连续的文本
#         text = generate_random_line(length)
#         timestamp = int(time.time()) + i
#         output_path = f'../../psudo_chinese_data/gen_line_print_data/'
#         output_paths_and_texts.append((output_path, text))
#
#     num_processes = multiprocessing.cpu_count()
#
#     with multiprocessing.Pool(processes=num_processes) as pool:
#         results = list(tqdm(pool.imap_unordered(process_image_wrapper,
#                                                 [(path, text, mnist_data) for path, text in output_paths_and_texts]),
#                             total=len(output_paths_and_texts)))
#
#     # # 单线程处理
#     # for output_path, text in tqdm(output_paths_and_texts):
#     #     process_image_wrapper((output_path, text, mnist_data))


"""
作者：张健
时间：2024.10.20
这个模块制造伪的行数据，基于单个中文字，随机添加删除符号
"""

from PIL import Image, ImageDraw
import numpy as np
import random
import time
import multiprocessing
import os
from tqdm import tqdm
import cv2  # OpenCV库，用于更快的图像处理
from gen_scratch import apply_scratches
from image_operation import *
import pickle

# 加载需要制作哪些汉字的字典
# with open('chinese_data1018/char_dict', 'rb') as f:
#     char_dict = pickle.load(f)
# # 从字符字典中提取字符
# dict_list = list(char_dict.keys())
char_dict = {}
with open('./char_dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        char, code = line.strip().split('\t')  # 按制表符分割
        char_dict[char] = int(code) - 1  # 将编码转换为整数

dict_list = list(char_dict.keys())

def generate_random_line(length,off_set, random_seq=False):
    if random_seq:
        return ''.join(random.choices(dict_list, k=length))
    else:
        temp_list = dict_list[off_set : min(off_set + length,len(dict_list))]
        # 打乱字符顺序
        random.shuffle(temp_list)
        return ''.join(temp_list)
    
def crop_off_whitespace(image):
    # 转换为NumPy数组
    # 将图像转换为灰度
    gray_image = image.convert('L')
    image_array = np.array(gray_image)
    threshold = 230
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

def load_local_images(image_directory):
    """这个函数根据单子数据添加到一个字典结构中"""
    mnist_data = {}
    font_style = []
    #files = sorted(os.listdir(image_directory))
    files = os.listdir(image_directory)
    filenames = [f for f in files if f.endswith('.jpg')]
    for filename in tqdm(filenames, desc="加载图像"):
        font_name, label = filename.split('_', 1)
        label = label.split('.')[0]
        if font_name not in font_style:
            font_style.append(font_name)
        filepath = os.path.join(image_directory, filename)
        image = Image.open(filepath).convert('L')  # 转为灰度图
        # if label not in mnist_data:
        #     mnist_data[label] = []
        # mnist_data[label].append(np.array(image))
        # 初始化字典结构
        if label not in mnist_data:
            mnist_data[label] = {}

        # 将图像数据存入相应的标签和字体名下
        mnist_data[label][font_name] = np.array(image)
        #font_style = list(set(font_style))
    return font_style, mnist_data
#
# def create_handwritten_number_image(line_chars, output_path, mnist_data, font_style, random_font=False):
#     list_of_text = list(line_chars)
#     width = 50 * len(line_chars)
#     height = 70
#     image = Image.new('L', (width, height), 255)
#
#     # 随机选择一次所有字符的图像
#     selected_images = []
#     style = random.choice(font_style)
#     #for char in line_chars:
#     for i_c, char in enumerate(line_chars):
#         if char in mnist_data:
#             char_images = mnist_data[char]
#             if random_font:
#                 selected_image = char_images.get(random.choice(font_style), char_images.get(random.choice(list(char_images.keys()))))
#             else:
#                 selected_image = char_images.get(style,char_images.get(random.choice(list(char_images.keys()))))
#
#             selected_images.append(selected_image)
#
#         else:
#             #print(f"未找到字符的图像：{char}")
#
#             #selected_images.append(np.zeros((height, width)))  # 如果找不到，填充空白图像
#             selected_images.append(np.ones((height, width)) * 255)  # 如果找不到，填充白色图
#             list_of_text[i_c] = ""
#     # 粘贴图像
#     cell_width = width // len(line_chars)
#     off_set_position = 0
#         # 加入多样性？
#     random_flag = False
#     if random.choice(range(2)) == 0:
#         random_flag = True
#     for i, single_image in enumerate(selected_images):
#         # 调整颜色和大小
#         scale_ratio = random.uniform(0.8, 1.0)
#         scaled_w = int(cell_width * scale_ratio)
#         scaled_h = int(height * scale_ratio)
#         single_image = cv2.resize(single_image, (scaled_w, scaled_h), interpolation=cv2.INTER_LINEAR)
#         single_image = Image.fromarray(single_image)
#         # 透视变换
#         if random_flag and random.choice(range(2)) == 0:
#             single_image = apply_perspective_transform(single_image)
#         # 应用旋转变换
#         #  # 旋转角度，可以调整
#         if random_flag and random.choice(range(2)) == 0:
#             angle_ratio = random.uniform(-1.0, 1.0)
#             angle = 10 * angle_ratio
#             single_image = rotate_text_image(single_image, angle)
#         single_width, single_height = single_image.size
#         if single_height > 70 or single_width > 50:
#             #single_image = single_image.resize((50, 70), Image.ANTIALIAS)
#             single_image = single_image.resize((50, 70), Image.Resampling.LANCZOS)
#
#
#         # 加入划痕
#         if random.choice(range(20)) == 0:
#             single_image = crop_off_whitespace(single_image)
#             single_image = apply_scratches(single_image)
#             list_of_text[i] = 'x'
#         single_width, single_height = single_image.size
#         #if cell_width - single_width >= 0:
#         offset_x = random.randint(0, cell_width - single_width)
#         ##else:
#         #    offset_x = single_width - cell_width
#
#         offset_y = random.randint(int(0.5*(height - single_height)), height - single_height)
#
#         #paste_position = (i * cell_width + offset_x, offset_y)
#         paste_position = (off_set_position + offset_x, offset_y)
#         off_set_position += offset_x + single_width
#         image.paste(single_image, paste_position)
#
#     # 切边
#     image = crop_off_whitespace(image)
#     width, height = image.size
#
#     draw = ImageDraw.Draw(image)
#     if random.choice(range(2)) == 0:
#         underline_y = height - random.randint(0,5)  # 下划线的位置
#         draw.line([(0, underline_y), (width, underline_y)], fill=0, width=2)
#
#
#     # 添加边距
#     min_margin = int(0.1 * height)
#     max_margin = int(0.18 * height)
#     left_margin = random.randint(min_margin, max_margin)
#     right_margin = random.randint(min_margin, max_margin)
#     top_margin = random.randint(min_margin, max_margin)
#     bottom_margin = random.randint(min_margin, max_margin)
#     larger_width = width + left_margin + right_margin
#     larger_height = height + top_margin + bottom_margin
#     larger_image = Image.new('L', (larger_width, larger_height), 255)
#     larger_image.paste(image, (left_margin, top_margin))
#
#     # 保存图像
#     timestamp = int(time.time())
#     text_new = "".join(list_of_text)
#     output_file = f'{output_path}{timestamp}_{text_new}.jpg'
#     larger_image.save(output_file)


def create_handwritten_number_image(line_chars, output_path, mnist_data, font_style, random_font=False):
    list_of_text = list(line_chars)

    width_goal = 70
    height_goal = 70

    # 整幅图片
    image = Image.new('L', (width_goal*len(line_chars), height_goal), 255)
    # 随机选择一次所有字符的图像
    selected_images = []
    style = random.choice(font_style)

    for i_c, char in enumerate(line_chars):
        if char in mnist_data:
            char_images = mnist_data[char]
            if random_font:
                selected_image = char_images.get(random.choice(font_style),
                                                 char_images.get(random.choice(list(char_images.keys()))))
            else:
                selected_image = char_images.get(style, char_images.get(random.choice(list(char_images.keys()))))

            selected_images.append(selected_image)

        else:
            # print(f"未找到字符的图像：{char}")

            # selected_images.append(np.zeros((height, width)))  # 如果找不到，填充空白图像
            selected_images.append(np.ones((height_goal, width_goal)) * 255)  # 如果找不到，填充白色图
            list_of_text[i_c] = ""
    # 粘贴图像
    #cell_width = width // len(line_chars)
    off_set_position = 0
    # 加入多样性？
    random_flag = False
    if random.choice(range(2)) == 0:
        random_flag = True
    for i, single_image in enumerate(selected_images):
        single_image = Image.fromarray(single_image)

        # 归一化文字部分的大小
        single_image = crop_off_whitespace(single_image)
        #single_image = cv2.resize(single_image, (width_goal, height_goal), interpolation=cv2.INTER_LINEAR)
        single_image = single_image.resize((width_goal, height_goal), Image.ANTIALIAS)


        # 调整颜色和大小
        # single_width, single_height = single_image.size
        # scale_ratio = random.uniform(0.8, 1.0)
        # scaled_w = int(single_width * scale_ratio)
        # scaled_h = int(single_height * scale_ratio)
        # #single_image = cv2.resize(single_image, (scaled_w, scaled_h), interpolation=cv2.INTER_LINEAR)
        # single_image = single_image.resize((scaled_w, scaled_h), Image.ANTIALIAS)

        # 透视变换
        if random_flag and random.choice(range(2)) == 0:
            single_image = apply_perspective_transform(single_image)
        # 应用旋转变换
        #  # 旋转角度，可以调整
        if random_flag and random.choice(range(2)) == 0:
            angle_ratio = random.uniform(-1.0, 1.0)
            angle = 10 * angle_ratio
            single_image = rotate_text_image(single_image, angle)
        single_width, single_height = single_image.size
        if single_height > height_goal or single_width > width_goal:
            single_image = single_image.resize((single_width, height_goal), Image.ANTIALIAS)
            #single_image = single_image.resize((single_width, height_goal), Image.Resampling.LANCZOS)

        # 加入划痕
        if random.choice(range(20)) == 0:
            single_image = crop_off_whitespace(single_image)
            single_image = apply_scratches(single_image)
            list_of_text[i] = 'x'
        # 切边
        single_image = crop_off_whitespace(single_image)

        # 此处可加入随机性
        single_image = single_image.resize((width_goal, height_goal), Image.ANTIALIAS)
        single_width, single_height = single_image.size
        # if cell_width - single_width >= 0:
        offset_x = 0#random.randint(0, 5)
        ##else:
        #    offset_x = single_width - cell_width

        offset_y = random.randint(0, height_goal - single_height)

        # paste_position = (i * cell_width + offset_x, offset_y)
        paste_position = (off_set_position + offset_x, offset_y)
        off_set_position += offset_x + single_width
        image.paste(single_image, paste_position)

    # 切边
    image = crop_off_whitespace(image)
    width, height = image.size

    draw = ImageDraw.Draw(image)
    if random.choice(range(2)) == 0:
        underline_y = height - random.randint(0, 5)  # 下划线的位置
        draw.line([(0, underline_y), (width, underline_y)], fill=0, width=2)

    # 添加边距
    min_margin = int(0.1 * height)
    max_margin = int(0.15 * height)
    left_margin = random.randint(min_margin, max_margin)
    right_margin = random.randint(min_margin, max_margin)
    top_margin = random.randint(min_margin, max_margin)
    bottom_margin = random.randint(min_margin, max_margin)
    larger_width = width + left_margin + right_margin
    larger_height = height + top_margin + bottom_margin
    larger_image = Image.new('L', (larger_width, larger_height), 255)
    larger_image.paste(image, (left_margin, top_margin))

    # 保存图像
    timestamp = int(time.time())
    text_new = "".join(list_of_text)
    output_file = f'{output_path}{timestamp}_{text_new}.jpg'
    larger_image.save(output_file)


def process_image_wrapper(args):
    output_path, text, mnist_data,font_style = args
    create_handwritten_number_image(text, output_path, mnist_data, font_style)
    return output_path

if __name__ == '__main__':
    random.seed(40)
    #image_directory = './single_font/pseudo_chinese_images_1111_checked'
    image_directory = '../../pseudo_chinese_images_1111_checked/'
    #output_path = './Chinese-app-digital/data/data_train/'
    #output_path = f'./psudo_chinese_data/gen_line_print_data_1110/'
    output_path = '../../psudo_chinese_data/gen_line_print_data_1118/'
    random_font = True
    random_seq = True
    os.makedirs(output_path, exist_ok=True)

    # 加载单个汉字图片
    font_style, mnist_data = load_local_images(image_directory)
    output_paths_and_texts = []
    off_set = 0
    for i in tqdm(range(1000)):
        length = random.randint(2, 5)
        # 生成一串连续的文本
        text = generate_random_line(length, off_set, random_seq)
        off_set += length
        if off_set > len(dict_list):
            off_set = 0
        if len(text) == 0:
            continue
        timestamp = int(time.time()) + i
        #output_paths_and_texts.append((output_path, text))
        create_handwritten_number_image(text, output_path, mnist_data, font_style, random_font)

    # num_processes = multiprocessing.cpu_count()
    #
    # with multiprocessing.Pool(processes=num_processes) as pool:
    #     results = list(tqdm(pool.imap_unordered(process_image_wrapper,
    #                                             [(path, text, mnist_data) for path, text in output_paths_and_texts]),
    #                         total=len(output_paths_and_texts)))
    # 单线程处理

    # for output_path, text in tqdm(output_paths_and_texts):
    #     process_image_wrapper((output_path, text, mnist_data, font_style))
