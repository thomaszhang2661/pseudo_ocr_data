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
import os
from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import pickle

# 加载需要制作哪些汉字的字典
# with open('chinese_data1018/char_dict', 'rb') as f:
#     char_dict = pickle.load(f)
# # 从字符字典中提取字符
# dict_list = list(char_dict.keys())
char_dict = {}
char_dict_reverse = {}

with open('char_dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        char, code = line.strip().split('\t')  # 按制表符分割
        char_dict[char] = int(code)  # 将编码转换为整数
        char_dict_reverse[int(code)] = char
dict_list = list(char_dict.keys())

def generate_random_line(length,off_set,random_seq=False):
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

# def load_local_images_pub(image_directory):
#     '''加载自动化所的单个手写字体'''
#     mnist_data = {}
#     #files = sorted(os.listdir(image_directory))
#     sub_files_list = os.listdir(image_directory)
#     for sub_files in tqdm(sub_files_list, desc="加载图像"):
#         word = char_dict_reverse[int(sub_files)]
#         folder_path = os.path.join(image_directory, sub_files)
#         files = os.listdir(folder_path)
#         mnist_data[word] = []
#         for filename in files:
#             filepath = os.path.join(folder_path, filename)
#             image = Image.open(filepath).convert('L')  # 转为灰度图
#             mnist_data[word].append(np.array(image))
#             #font_style = list(set(font_style))
#     return mnist_data


def load_image(filepath):
    """加载并转换单个图像为灰度图"""
    image = Image.open(filepath).convert('L')  # 转为灰度图
    return np.array(image)


def load_local_images_pub(image_directory):
    '''加载自动化所的单个手写字体'''
    mnist_data = {}
    sub_files_list = os.listdir(image_directory)

    # 创建线程池，最大线程数可以根据系统的核心数调整
    with ThreadPoolExecutor() as executor:
        # 结果存储
        future_to_image = {}

        for sub_files in tqdm(sub_files_list, desc="加载图像"):
            if not len(sub_files) == 5 and sub_files.isdigit:
                continue
            word = char_dict_reverse[int(sub_files)]
            folder_path = os.path.join(image_directory, sub_files)
            files = os.listdir(folder_path)
            mnist_data[word] = []

            # 为每个文件提交加载任务
            for filename in files[:5]:
                filepath = os.path.join(folder_path, filename)
                future = executor.submit(load_image, filepath)
                future_to_image[future] = word  # 关联图像与标签

        # 获取所有任务的结果
        for future in as_completed(future_to_image):
            word = future_to_image[future]
            image_data = future.result()
            mnist_data[word].append(image_data)

    return mnist_data

def create_handwritten_number_image(line_chars, output_path, mnist_data, font_style, random_font=False):
    list_of_text = list(line_chars)
    width = 50 * len(line_chars)
    height = 70
    image = Image.new('L', (width, height), 255)

    # 随机选择一次所有字符的图像
    selected_images = []
    style = random.choice(font_style)
    for i_c, char in enumerate(line_chars):
        if char in mnist_data:
            char_images = mnist_data[char]
            # if random_font:
            #     selected_image = char_images[random.choice(font_style)]
            # else:
            # #selected_image = char_images[np.random.choice(len(char_images))]
            #     selected_image = char_images[style]
            if random_font:
                selected_image = char_images.get(random.choice(font_style), char_images.get(random.choice(list(char_images.keys()))))
            else:
                selected_image = char_images.get(style, char_images.get(random.choice(list(char_images.keys()))))
            selected_images.append(selected_image)
        else:
            print(f"未找到字符的图像：{char}")
            #raise
            #selected_images.append(np.zeros((height, width)))  # 如果找不到，填充空白图像
            selected_images.append(np.ones((height, width)) * 255)  # 如果找不到，填充白色图
            list_of_text[i_c] = " "
    # 粘贴图像
    cell_width = width // len(line_chars)
    off_set_position = 0
    # 加入多样性？
    random_flag = False
    if random.choice(range(2)) == 0:
        random_flag = True
    for i, single_image in enumerate(selected_images):
        # 调整颜色和大小
        scale_ratio = random.uniform(0.8, 1.0)
        scaled_w = int(cell_width * scale_ratio)
        scaled_h = int(height * scale_ratio)
        single_image = cv2.resize(single_image, (scaled_w, scaled_h), interpolation=cv2.INTER_LINEAR)
        single_image = Image.fromarray(single_image)
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
        if single_height > 70 or single_width > 50:
            single_image = single_image.resize((50, 70), Image.ANTIALIAS)
            #single_image = single_image.resize((50, 70), Image.Resampling.LANCZOS)

        # single_width, single_height = single_image.size
        # # 加入划痕
        # if random.choice(range(20)) == 0:
        #     single_image = apply_scratches(single_image)
        #     list_of_text[i] = 'x'

        # 加入划痕
        if random.choice(range(20)) == 0:
            single_image = crop_off_whitespace(single_image)
            single_image = apply_scratches(single_image)
            list_of_text[i] = 'x'
        single_width, single_height = single_image.size

        #if cell_width - single_width >= 0:
        offset_x = random.randint(0, cell_width - single_width)
        ##else:
        #    offset_x = single_width - cell_width

        offset_y = random.randint(int(0.5*(height - single_height)), height - single_height)

        #paste_position = (i * cell_width + offset_x, offset_y)
        paste_position = (off_set_position + offset_x, offset_y)
        off_set_position += offset_x + single_width
        image.paste(single_image, paste_position)
    # 切边
    image = crop_off_whitespace(image)
    width, height = image.size

    draw = ImageDraw.Draw(image)
    if random.choice(range(2)) == 0:
        underline_y = height - random.randint(3, 7)  # 下划线的位置
        draw.line([(0, underline_y), (width, underline_y)], fill=0, width=2)

    min_margin = int(0.1 * height)
    max_margin = int(0.18 * height)
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


# 定义伽马校正函数
def adjust_gamma(image, gamma=1.0):
    # 构建查找表来加快伽马校正的速度
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype("uint8")

    # 将图像转换为灰度模式（如果图像为 RGB 模式）
    if image.mode != 'L':
        image = image.convert('L')

    # 应用查找表进行伽马校正
    image = image.point(table)

    return image


def create_handwritten_number_image_pub(line_chars, output_path, mnist_data):
    '''根据自动化所的手写图像生成伪数据'''

    list_of_text = list(line_chars)
    width = 80 * len(line_chars)
    height = 80
    image = Image.new('L', (width, height), 255)

    # 随机选择一次所有字符的图像
    selected_images = []
    for i_c, char in enumerate(line_chars):
        if char in mnist_data:
            char_images = mnist_data[char]
            random_indices = random.randint(0, len(char_images) - 1)

            # if random_font:
            #     selected_image = char_images[random.choice(font_style)]
            # else:
            # #selected_image = char_images[np.random.choice(len(char_images))]
            #     selected_image = char_images[style]
            selected_image = char_images[random_indices]
            selected_images.append(selected_image)
        else:
            print(f"未找到字符的图像：{char}")
            #raise
            #selected_images.append(np.zeros((height, width)))  # 如果找不到，填充空白图像
            #selected_images.append(np.ones((height, width)) * 255)  # 如果找不到，填充白色图
            list_of_text[i_c] = ""
    # 粘贴图像
    cell_width = width // len(line_chars)
    off_set_position = 0
    # 加入多样性？
    random_flag = False
    if random.choice(range(2)) == 0:
        random_flag = True
    for i, single_image in enumerate(selected_images):
        # 调整颜色和大小
        # 取原图尺寸
        pic_width, pic_height = Image.fromarray(single_image).size
        # 取随机数
        scale_ratio = random.uniform(0.8, 1.0)
        # 缩放之后的图片大小
        resize_ratio = min(64/pic_width, 64/pic_height)
        single_image = cv2.resize(single_image,
                                  (int(pic_width * resize_ratio * scale_ratio),
                                   int(pic_height * resize_ratio * scale_ratio)),
                                  interpolation=cv2.INTER_LINEAR)
        single_image = Image.fromarray(single_image)
        single_width, single_height = single_image.size

        left_margin_single = int((cell_width - single_width)/2)
        top_margin_single = int((height - single_height)/2)
        single_blank = Image.new('L', (cell_width, height), 255)

        single_blank.paste(single_image, (left_margin_single, top_margin_single))
        single_image = single_blank
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
        if single_height > height or single_width > cell_width:
            single_image = single_image.resize((cell_width, height), Image.ANTIALIAS)
            #single_image = single_image.resize((50, 70), Image.Resampling.LANCZOS)

        # 加入划痕
        if random.choice(range(20)) == 0:
            single_image = crop_off_whitespace(single_image)
            single_image = apply_scratches(single_image)
            list_of_text[i] = 'x'
        single_width, single_height = single_image.size

        #if cell_width - single_width >= 0:
        offset_x = random.randint(0, cell_width - single_width)
        ##else:
        #    offset_x = single_width - cell_width

        offset_y = random.randint(int(0.5*(height - single_height)), height - single_height)

        #paste_position = (i * cell_width + offset_x, offset_y)
        paste_position = (off_set_position + offset_x, offset_y)
        off_set_position += offset_x + single_width
        image.paste(single_image, paste_position)
    # 切边
    image = crop_off_whitespace(image)
    width, height = image.size

    draw = ImageDraw.Draw(image)
    if random.choice(range(2)) == 0:
        underline_y = height - random.randint(3, 7)  # 下划线的位置
        draw.line([(0, underline_y), (width, underline_y)], fill=0, width=2)
    # 调整伽马值，尝试低于1.0的值来增加黑色区域的深度
    gamma_value = 0.4  # 可以调整此值，0.5效果通常较为明显
    image = adjust_gamma(image, gamma=gamma_value)

    min_margin = int(0.1 * height)
    max_margin = int(0.18 * height)
    left_margin = random.randint(min_margin, max_margin)
    right_margin = random.randint(min_margin, max_margin)
    top_margin = random.randint(min_margin, max_margin)
    bottom_margin = random.randint(min_margin, max_margin)
    larger_width = width + left_margin + right_margin
    larger_height = height + top_margin + bottom_margin
    larger_image = Image.new('L', (larger_width, larger_height), 255)
    larger_image.paste(image, (left_margin, top_margin))

    # 保存图像
    width, height = larger_image.size
    # 计算新的宽度以保持纵横比
    target_height = 70
    new_width = int((target_height / height) * width)
    resized_image = larger_image.resize((new_width, target_height), Image.Resampling.LANCZOS)

    timestamp = int(time.time())
    text_new = "".join(list_of_text)
    output_file = f'{output_path}{timestamp}_{text_new}.jpg'
    resized_image.save(output_file)

def process_image_wrapper(args):
    output_path, text, mnist_data,font_style = args
    create_handwritten_number_image(text, output_path, mnist_data, font_style)
    return output_path

if __name__ == '__main__':
    random.seed(42)
    #image_directory = '../../pseudo_chinese_images_1110'
    image_directory = './chinese_data1018/pic_chinese_char'
    output_path = f'../../psudo_chinese_data/gen_line_print_data_1113_test/'
    random_font = False
    random_seq = True
    font_from = "public_zidonghua"
    #font_from = "psudo"
    os.makedirs(output_path, exist_ok=True)

    # 加载单个汉字图片
    if font_from == "public_zidonghua":
        mnist_data = load_local_images_pub(image_directory)
    else:
        font_style, mnist_data = load_local_images(image_directory)
    # 检查单个字体
    #Image.fromarray(mnist_data["张"][0]).save('../../psudo_chinese_data/test.png')

    output_paths_and_texts = []
    off_set = 0
    for i in tqdm(range(1000)):
        length = random.randint(15, 20)
        # 生成一串连续的文本
        text = generate_random_line(length, off_set, random_seq)
        off_set += length
        if off_set > len(dict_list):
            off_set = 0
        if len(text) == 0:
            continue
        timestamp = int(time.time()) + i
        #output_paths_and_texts.append((output_path, text))
        if font_from == "public_zidonghua":
            create_handwritten_number_image_pub(text, output_path, mnist_data)
        else:
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