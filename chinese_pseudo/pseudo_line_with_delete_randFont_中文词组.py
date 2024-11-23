# # 先校验一下是否有字典之外的汉字
# # 加载需要制作哪些汉字的字典
# char_dict = {}
# with open('./char_dict.txt', 'r', encoding='utf-8') as f:
#     for line in f:
#         char, code = line.strip().split('\t')  # 按制表符分割
#         char_dict[char] = int(code) - 1  # 将编码转换为整数
#
# dict_list = list(char_dict.keys())
#
# # 读取词组
#
# #读取文件中的每一个汉字检查是否超出dict_list范围
# with open('./all_chinese_dicts.txt', 'rb') as f:
#     for line in f:
#         line = line.decode('utf-8').strip()
#         for char in line:
#             if char == " ":
#                 continue
#             if char not in dict_list:
#                 # 补充字典char_dict
#                 print(f'字典中没有的汉字：{char}')
#                 with open('./char_dict.txt', 'a', encoding='utf-8') as f:
#                     f.write(f'{char}\t{len(dict_list)+2}\n')
#
#                 with open('./char_added_1123.txt', 'a', encoding='utf-8') as f:
#                     f.write(f'{char}\n')
#                 #update dict_list
#                 dict_list.append(char)

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
import math

length_max = 15


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

chinese_words = []
with open('./all_chinese_dicts.txt', 'r', encoding='utf-8') as f:
    for line in f:
        chinese_words.append(line.strip())

def generate_random_line(length,off_set, random_seq=False):
    if random_seq:
        return ''.join(random.choices(dict_list, k=length))
    else:
        temp_list = dict_list[off_set : min(off_set + length,len(dict_list))]
        # 打乱字符顺序
        random.shuffle(temp_list)
        return ''.join(temp_list)


def generate_line_by_chinese_word(off_set, random_seq=False,length=1,):
    # 用来处理单一逻辑的辅助函数
    def process_result(result):
        # 如果字符数大于20，随机截取连续的20个字符
        if len(result) > length_max:
            # 切割成词语（假设通过空格分隔）
            line_list = result.split()
            ratio = len("".join(line_list)) / len(line_list) # 计算比例
            # 根据比例计算截取长度
            result1 = random.sample(line_list, k=min(math.floor(length_max / ratio), len(line_list)))
            result = ' '.join(result1)  # 连接成字符串
        else:
            # 如果字符数小于20，随机打乱字符
            line_list = result.split()
            random.shuffle(line_list)  # 打乱顺序
            result = ' '.join(line_list)  # 连接成字符串
        return result

    # 根据random_seq的值选择不同的生成逻辑
    if random_seq:
        result = random.choice(chinese_words)  # 随机选择一个
    else:
        result = chinese_words[off_set]  # 使用给定的偏移量选取

    return process_result(result)  # 处理并返回结果

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



def create_handwritten_number_image(line_chars, output_path, mnist_data, font_style, random_font=False):
    list_of_text = list(line_chars)

    width_goal = 70
    height_goal = 70
    off_set_max = 5
    # 整幅图片
    image = Image.new('L', ((width_goal + off_set_max)*len(line_chars), height_goal), 255)
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
            selected_images.append(np.ones((height_goal, int(width_goal/2))) * 255)  # 如果找不到，填充白色图
            if char != " ":
                print("未找到字符",char)
            list_of_text[i_c] = ""
    # 粘贴图像
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
        single_width, single_height = single_image.size
        ratio = min(height_goal/single_height, width_goal/single_width)
        single_image = single_image.resize((int(ratio*single_width), int(ratio*single_height)), Image.ANTIALIAS)
        #single_image = single_image.resize((int(ratio*single_width), int(ratio*single_height)),
        # Image.Resampling.LANCZOS)


        # 调整颜色和大小
        single_width, single_height = single_image.size
        scale_ratio = random.uniform(0.8, 1.0)
        scaled_w = int(single_width * scale_ratio)
        scaled_h = int(single_height * scale_ratio)
        single_image = single_image.resize((scaled_w, scaled_h), Image.ANTIALIAS)
        #single_image = single_image.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)


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
            single_width, single_height = single_image.size
            ratio = min(height_goal/single_height, width_goal/single_width)
            single_image = single_image.resize((int(single_width * ratio), int(single_height*ratio)), Image.ANTIALIAS)
            #single_image = single_image.resize((int(single_width * ratio), int(single_height*ratio)),
            # Image.Resampling.LANCZOS)

        # 加入划痕
        if random.choice(range(50)) == 0:
            single_image = crop_off_whitespace(single_image)
            single_image = apply_scratches(single_image)
            list_of_text[i] = 'x'
        # 切边
        single_image = crop_off_whitespace(single_image)

        # 此处可加入随机性
        single_width, single_height = single_image.size

        # if cell_width - single_width >= 0:
        offset_x = random.randint(0, off_set_max)
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
    output_path = '../../psudo_chinese_data/gen_line_print_data_1123/'
    random_font = True
    random_seq = True
    os.makedirs(output_path, exist_ok=True)

    # 加载单个汉字图片
    font_style, mnist_data = load_local_images(image_directory)
    output_paths_and_texts = []
    off_set = 0
    for i in tqdm(range(1000)):
        #length = random.randint(2, 5)
        # 生成一串连续的文本
        #text = generate_random_line(length, off_set, random_seq)
        text = generate_line_by_chinese_word(off_set, random_seq)

        off_set += 1
        if off_set > len(dict_list):
            off_set = 0
        if len(text) == 0:
            continue
        timestamp = int(time.time()) + i
        #output_paths_and_texts.append((output_path, text))
        create_handwritten_number_image(text, output_path, mnist_data, font_style, random_font)




