
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
from mapping_punct import chinesepun2englishpun
import json
from itertools import cycle, islice



# 上部标点
upper_punct = [
    '"', "'", "‘", "’", '“', '”', '`', '^']

# 下部标点
lower_punct = [
    '.', ',', '。', '、', '…'
]

middle_punct = ["-", "~", "<", ">", "[", "]", "(", ")", "{", "}"]

letter_A = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
letter_baseline = ['a', 'c', 'e', 'i', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'z']  # 基线字母
letter_ascender = ['b', 'd', 'h', 'k', 'l', 't', 'f']  # 上升部件字母
letter_descender = ['g', 'p', 'q', 'y', 'j']  # 下降部件字母

# 获取当前工作目录
current_working_directory = os.getcwd()

print("当前工作路径是:", current_working_directory)

length_max = 15

PREVIOUS_FONT_INDEX = 720


# 读取字典
char_dict = {}
with open('./merged_dict.txt', 'r', encoding='utf-8') as f:
    lenth_original = len(f.readlines())
    for line in f:
        char, code = line.strip().split(' : ')  # 按制表符分割
        char_dict[char] = int(code)  # 将编码转换为整数
    char_dict[" "] = lenth_original + 1
    print("char_dict space" ,char_dict[" "])
dict_list = list(char_dict.keys())


punct_dict = {}
with open('./标点符号.txt', 'r', encoding='utf-8') as f:
    for line in f:
        char, code = line.strip().split(' : ')  # 按制表符分割
        punct_dict[char] = int(code)  # 将编码转换为整数



zidonghua_dict = {}
zidonghua_dict_reverse = {}
with open('merged_dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        char, code = line.strip().split(' : ')  # 按制表符分割
        zidonghua_dict[char] = int(code)  # 将编码转换为整数
        zidonghua_dict_reverse[int(code)] = char
zidonghua_list = list(zidonghua_dict.keys())


lenth_original = len(zidonghua_dict)
# 读取需要补充的字典
# char_complement_dict = {}
# with open('./需要添加的汉字', 'r', encoding='utf-8') as f:
#     for i_l, line in enumerate(f):
#         char = line.strip()
#         zidonghua_dict[char] = int(lenth_original + i_l + 1)
#         zidonghua_dict_reverse[int(lenth_original + i_l + 1)] = char

# 检查translate table
# E_pun = u'••,!?[][]()<><>‘~::---@#$￥%||;=/~aaeeno2福'
# C_pun = u'·•，！？【】［］（）〈〉＜＞\'~：ː—－­＠＃＄￥％｜∣；＝／～ɑàéëñö₂褔'
# print(len(E_pun), len(C_pun))
# for char in E_pun:
#     if char not in zidonghua_dict:
#         print('E_pun', char)
# for char in C_pun:
#     if char not in zidonghua_dict:
#         print('C_pun', char)


print("corpus exam finished")

# 定义伽马校正函数
def adjust_gamma(image, gamma=1.0):
    # 构建查找表来加快伽马校正的速度

    image = Image.fromarray(image)

    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype("uint8")

    # 将图像转换为灰度模式（如果图像为 RGB 模式）
    if image.mode != 'L':
        image = image.convert('L')

    # 应用查找表进行伽马校正
    image = image.point(table)

    return np.array(image)



# def generate_line_by_chinese_word(off_set, random_seq=False,length=1,):
#     # 用来处理单一逻辑的辅助函数
#     def process_result(result):
#         # 如果字符数大于20，随机截取连续的20个字符
#         if len(result) > length_max:
#             # 切割成词语（假设通过空格分隔）
#             line_list = result.split()
#             ratio = len("".join(line_list)) / len(line_list) # 计算比例
#             # 根据比例计算截取长度
#             result1 = random.sample(line_list, k=min(math.floor(length_max / ratio), len(line_list)))
#             result = ' '.join(result1)  # 连接成字符串
#         else:
#             # 如果字符数小于20，随机打乱字符
#             line_list = result.split()
#             random.shuffle(line_list)  # 打乱顺序
#             result = ' '.join(line_list)  # 连接成字符串
#         return result

#     # 根据random_seq的值选择不同的生成逻辑
#     if random_seq:
#         result = random.choice(chinese_words)  # 随机选择一个
#     else:
#         result = chinese_words[off_set]  # 使用给定的偏移量选取

#     return process_result(result)  # 处理并返回结果

def crop_off_whitespace(image ,direction=2):
    # 转换为NumPy数组
    # 将图像转换为灰度
    gray_image = image.convert('L')
    w ,h = gray_image.size
    image_array = np.array(gray_image)
    threshold = 230
    # 计算每一行和每一列的灰度值之和
    horizontal_sum = np.sum(image_array < threshold, axis=1)
    vertical_sum = np.sum(image_array < threshold, axis=0)

    if direction == 2:
        # 找到上边界和下边界
        top = np.argmax(horizontal_sum > 0)
        bottom = len(horizontal_sum) - np.argmax(horizontal_sum[::-1] > 0)

        # 找到左边界和右边界
        left = np.argmax(vertical_sum > 0)
        right = len(vertical_sum) - np.argmax(vertical_sum[::-1] > 0)
    else:
        # 找到左边界和右边界
        left = np.argmax(vertical_sum > 0)
        right = len(vertical_sum) - np.argmax(vertical_sum[::-1] > 0)
        top = 0
        bottom = h

    # # 找到上边界和下边界
    # top = np.argmax(horizontal_sum > 0)
    # bottom = len(horizontal_sum) - np.argmax(horizontal_sum[::-1] > 0)
    #
    # # 找到左边界和右边界
    # left = np.argmax(vertical_sum > 0)
    # right = len(vertical_sum) - np.argmax(vertical_sum[::-1] > 0)

    # 裁剪图像
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

def load_local_images(image_directory):
    """这个函数根据单子数据添加到一个字典结构中"""
    mnist_data = {}
    font_style = []
    # files = sorted(os.listdir(image_directory))
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
        # font_style = list(set(font_style))
    return font_style, mnist_data




def load_local_images_pub(image_directory ,num_font ,num_font_off_set):
    '''加载自动化所的单个手写字体'''
    zidonghua_data = {}

    # 获取所有子文件夹的列表
    # sub_files_list = [sub_files for sub_files in os.listdir(image_directory)
    #                   if len(sub_files) == 5 and sub_files.isdigit()]

    if os.path.exists(image_directory):
        sub_files_list = [sub_files for sub_files in os.listdir(image_directory)]
    else:
        print(f"Directory {image_directory} not found.")
    # 遍历所有有效子文件夹
    for sub_files in tqdm(sub_files_list, desc="加载图像"):
        # 获取对应的字符
        word = zidonghua_dict_reverse.get(int(sub_files[:-4]), None)
        if word is None:  # 如果字典中没有对应的字符，跳过
            continue

        folder_path = os.path.join(image_directory, sub_files)

        # 获取该文件夹中所有文件名
        files = os.listdir(folder_path)
        # files = [entry.name for entry in os.scandir(folder_path) if entry.is_file()]
        sorted_files = sorted(files, key=lambda x: x.split('.')[0])
        if len(sorted_files) < num_font_off_set + num_font:
            sorted_files = list(islice(cycle(sorted_files), num_font_off_set + num_font))

        files = sorted_files[num_font_off_set:num_font_off_se t +num_font]
        # print(len(files),'len_sorted_files')
        # 初始化当前字符的图像数据列表
        zidonghua_data[word] = []

        # 直接打开图像并转换为灰度图像，批量加载
        for filename in files:
            filepath = os.path.join(folder_path, filename)
            try:
                # 加载图像并转换为灰度模式
                image_data = Image.open(filepath).convert('L')
                zidonghua_data[word].append(np.array(image_data))  # 存储图像数据
            except Exception as e:
                print(f"Error loading image {filepath}: {e}")
    zidonghua_data[" "] = [np.ones((70, 70)) * 255]  # 空格
    return zidonghua_data


def create_handwritten_number_image_pub_by_corpus(index_font, index_line, line_chars, output_path, zidonghua_data, mnist_data=[]):
    '''根据自动化所的手写图像生成伪数据'''

    list_of_text = list(line_chars)

    width_goal = 70
    height_goal = 70
    off_set_max = 10
    # 整幅图片
    image = Image.new('L', ((width_goal + off_set_max ) *len(line_chars), int(height_goal * 1.5)), 255)
    gamma_value = 0.4  # 可以调整此值，0.5效果通常较为明显
    # 随机选择一次所有字符的图像
    selected_images = []
    for i_c, char in enumerate(line_chars):
        # if char not in zidonghua_data:
        #     list_of_text[i_c] = " "
        #     # 添加空白图片
        #     selected_images.append(zidonghua_data[" "][0])
        #     #print("warning not in dict", char, line_chars)
        #     continue
        if char in zidonghua_data:
            char_images = zidonghua_data[char]
            # random_indices = random.randint(0, len(char_images) - 1)
            # index_font = index_font % len(char_images)
            try:
                if char == " ":
                    selected_image = char_images[0]
                else:
                    selected_image = char_images[index_font]
            except IndexError as e:
                print(f"Error: {e}. Length of char_images: {len(char_images)}, index_font: {index_font}")

            # 调整伽马值，尝试低于1.0的值来增加黑色区域的深度
            selected_image = adjust_gamma(selected_image, gamma=gamma_value)
            selected_images.append(selected_image)
        # elif char in mnist_data:
        #     char_images = mnist_data[char]
        #     selected_image = char_images.get(random.choice(font_style),
        #                                          char_images.get(random.choice(list(char_images.keys()))))
        #
        #     selected_images.append(selected_image)

        else:
            # raise
            # selected_images.append(np.zeros((height, width)))  # 如果找不到，填充空白图像
            # selected_images.append(np.ones((height_goal, int(width_goal/2))) * 255)  # 如果找不到，填充白色图

            # ========================
            # if char != " ":
            #     print("未找到字符", char)
            list_of_text[i_c] = " "
            selected_images.append(zidonghua_data[" "][0])
    # 粘贴图像
    # 粘贴图像
    off_set_position = 0
    # 加入多样性？
    random_flag = False
    if random.choice(range(1)) == 0:
        random_flag = True
    for i, single_image in enumerate(selected_images):
        single_image = Image.fromarray(single_image)

        # 归一化文字部分的大小
        single_image = crop_off_whitespace(single_image)
        cur_width, cur_height = single_image.size
        ratio = min(width_goal / cur_width, height_goal / cur_height)

        if list_of_text[i] not in punct_dict:
            if random.choice(range(2)) == 0:
                # single_image = single_image.resize((int(cur_width*ratio), int(cur_height*ratio)), Image.ANTIALIAS)
                single_image = single_image.resize((int(cur_widt h *ratio), int(cur_heigh t *ratio)), Image.Resampling.LANCZOS)
        # elif list_of_text[i] in upper_punct:
        #     single_image = single_image.resize((int(cur_width*ratio * 0.4), int(cur_height*ratio * 0.4)), Image.Resampling.LANCZOS)
        # elif list_of_text[i] in lower_punct:
        #     single_image = single_image.resize((int(cur_width*ratio* 0.2), int(cur_height*ratio * 0.2)), Image.Resampling.LANCZOS)


        # elif list_of_text[i] in letter_descender:
        #     single_image = single_image.resize((int(cur_width*ratio), int(cur_height*ratio)), Image.Resampling.LANCZOS)
        # elif list_of_text[i] in letter_ascender:
        #     single_image = single_image.resize((int(cur_width*ratio), int(cur_height*ratio)), Image.Resampling.LANCZOS)
        # elif list_of_text[i] in letter_baseline:
        #     single_image = single_image.resize((int(cur_width * ratio * 0.5), int(cur_height * ratio * 0.5)),
        #                                        Image.Resampling.LANCZOS)
        #
        # elif list_of_text[i] in letter_A:
        #     single_image = single_image.resize((int(cur_width*ratio ), int(cur_height*ratio)), Image.Resampling.LANCZOS)
        elif ratio < 1:
            single_image = single_image.resize((int(cur_widt h *ratio * 0.9), int(cur_heigh t *ratio * 0.9)), Image.Resampling.LANCZOS)



        # 透视变换
        if random_flag  :# and random.choice(range(2)) == 0:
            single_image = apply_perspective_transform(single_image)
        # 应用旋转变换
        #  # 旋转角度，可以调整
        if random_flag:  # and random.choice(range(2)) == 0:
            angle_ratio = random.uniform(-1.0, 1.0)
            angle = 10 * angle_ratio
            single_image = rotate_text_image(single_image, angle)

        single_image = crop_off_whitespace(single_image)
        # 归一化大小
        if list_of_text[i] not in punct_dict:
            cur_width, cur_height = single_image.size
            # if cur_height > height_goal or cur_width > width_goal:
            # single_image = cv2.resize(single_image, (width_goal, height_goal), interpolation=cv2.INTER_LINEAR)
            ratio = min(width_goal / cur_width, height_goal / cur_height)
            # single_image = single_image.resize((int(cur_width * ratio), int(cur_height * ratio)), Image.ANTIALIAS)
            single_image = single_image.resize((int(cur_width * ratio), int(cur_height * ratio)),
                                               Image.Resampling.LANCZOS)
        if list_of_text[i] == " ":
            single_image = Image.fromarray(np.ones((height_goal,
                                                    random.randint(int(width_goal * 0.3), int(width_goal)))) * 255)

        # 调整大小
        single_width, single_height = single_image.size
        scale_ratio = random.uniform(0.9, 1.0)
        scaled_w = int(single_width * scale_ratio)
        scaled_h = int(single_height * scale_ratio)
        # single_image = single_image.resize((scaled_w, scaled_h), Image.ANTIALIAS)
        single_image = single_image.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)

        # 加入划痕
        if list_of_text[i] not in punct_dict and list_of_text[i] != " " and random.choice(range(100)) == 0:
            single_image = crop_off_whitespace(single_image)
            single_image = apply_scratches(single_image)
            list_of_text[i] = '\\'

        # 切边
        single_image = crop_off_whitespace(single_image)

        # 此处可加入随机性
        single_width, single_height = single_image.size
        offset_x = random.randint(0, min(off_set_max, int(single_width)))
        ##else:
        #    offset_x = single_width - cell_width

        # offset_y = random.randint(0, height_goal - single_height)
        # 适当调整位置
        if list_of_text[i] not in punct_dict:
            offset_y = random.randint(max(int(0.5 * height_goal - single_height), 0),
                                      min(int(0.5 * height_goal), height_goal - single_height))
        elif list_of_text[i] in upper_punct:
            offset_y = random.randint(0, int(0.1 * height_goal))
        elif list_of_text[i] in lower_punct:
            offset_y = random.randint(min(int(0.7 * height_goal), height_goal - single_height),
                                      height_goal - single_height)
        elif list_of_text[i] in middle_punct:
            offset_y = random.randint(int(0.5 * height_goal - single_height * 0.5 - 0.1 * single_height),
                                      int(0.5 * height_goal - single_height * 0.5 + 0.1 * single_height))

        # elif list_of_text[i] in letter_baseline:
        #     offset_y = random.randint(min(int(0.7 * height_goal), height_goal - single_height),
        #                               height_goal - single_height)
        # elif list_of_text[i] in letter_ascender:
        #     offset_y = random.randint(max(int(0.5 * height_goal - single_height * 0.5),0),
        #                               int(0.5 * height_goal))
        # elif list_of_text[i] in letter_descender:
        #     offset_y = random.randint(max(int(0.5 * height_goal - single_height * 0.3),0),
        #                               min(int(0.5 * height_goal), int(height_goal * 1.5) - single_height))

        elif list_of_text[i] in letter_A:
            offset_y = random.randint(height_goal - single_height - int(0.1 * single_height),
                                      height_goal - single_height)

        elif list_of_text[i] in letter_baseline:
            offset_y = random.randint(height_goal - single_height - int(0.1 * single_height),
                                      height_goal - single_height)
        elif list_of_text[i] in letter_ascender:
            offset_y = random.randint(height_goal - single_height - int(0.1 * single_height),
                                      height_goal - single_height)

        elif list_of_text[i] in letter_descender:
            # offset_y = random.randint(int(height_goal - single_height * 0.5 - 0.05 * single_height),
            #                           int(height_goal - single_height * 0.5))
            offset_y = random.randint(height_goal - single_height - int(0.1 * single_height),
                                      int(height_goal - single_height * 0.5))

        elif list_of_text[i] in punct_dict:
            # offset_y = random.randint(height_goal - single_height - int(0.1 * height_goal),
            #                           height_goal - single_height)
            offset_y = random.randint(int(0.5 * height_goal - single_height * 0.5 - 0.1 * single_height),
                                      int(0.5 * height_goal - single_height * 0.5 + 0.1 * single_height))
        else:
            offset_y = random.randint(int(height_goal * 0.5 - single_height * 0.5 - 0.1 * single_height),
                                      int(height_goal * 0.5 - single_height * 0.5 + 0.1 * single_height))

        # 这个地方需要对标点符号特殊处理。

        # paste_position = (i * cell_width + offset_x, offset_y)
        paste_position = (off_set_position + offset_x, offset_y)
        off_set_position += offset_x + single_width
        image.paste(single_image, paste_position)

    # 切左右
    image = crop_off_whitespace(image, direction=1)
    width, height = image.size
    draw = ImageDraw.Draw(image)
    if random.choice(range(3)) != 0:
        underline_y = height_goal - random.randint(0, 5)  # 下划线的位置
        draw.line([(0, underline_y), (width, underline_y)], fill=0, width=2)

    # 切边
    image = crop_off_whitespace(image)
    width, height = image.size

    # 添加边距
    min_margin = int(0.04 * height)
    max_margin = int(0.08 * height)
    left_margin = random.randint(min_margin, max_margin)
    right_margin = random.randint(min_margin, max_margin)
    top_margin = random.randint(min_margin, max_margin)
    bottom_margin = random.randint(min_margin, max_margin)
    larger_width = width + left_margin + right_margin
    larger_height = height + top_margin + bottom_margin
    larger_image = Image.new('L', (larger_width, larger_height), 255)
    larger_image.paste(image, (left_margin, top_margin))
    # 保存图像

    w_l, h_l = larger_image.size
    if h_l > 64:
        ratio = 64 / h_l
        larger_image = larger_image.resize((int(w_l * ratio), int(h_l * ratio)), Image.Resampling.LANCZOS)

    timestamp = int(time.time())
    text_new = "".join(list_of_text)
    output_sub = os.path.join(output_path, str(i_font + num_font_off_set + PREVIOUS_FONT_INDEX))
    os.makedirs(output_sub, exist_ok=True)
    # print(output_sub)
    output_file = os.path.join(output_sub,
                               f'{timestamp}_{i_font + num_font_off_set + PREVIOUS_FONT_INDEX}_{index_line}.jpg')

    try:
        larger_image.save(output_file)
        label_content[f'{timestamp}_{i_font + num_font_off_set + PREVIOUS_FONT_INDEX}_{index_line}'] = text_new

    except Exception as e:
        print(f"Error saving image {output_file}: {e}")

    # label_path = os.path.join(output_sub, 'labels')
    # os.makedirs(label_path, exist_ok=True)
    # label_file_name = os.path.join(label_path, f"{timestamp}_{i_font+num_font_off_set}_{index_line}.txt")

    # with open(label_file_name,'w',encoding='utf-8') as f:
    #     f.write(text_new)


if __name__ == '__main__':
    random.seed(40)
    num_font = 5  # 字体数量
    num_font_off_set = 0
    # image_directory = './single_font/pseudo_chinese_images_1111_checked'
    # image_font_directory = '../../pseudo_chinese_images_1111_checked/'
    # image_font_directory = '../../pseudo_chinese_images_1111_checked/'
    # image_pub_directory = './chinese_data1018/pic_chinese_char'
    # image_pub_directory = '../../gnt_all/'.replace('/', os.sep)
    image_pub_directory = '/database/single_font_1222/'.replace('/', os.sep)

    # output_path = './Chinese-app-digital/data/data_train/'
    # output_path = f'./psudo_chinese_data/gen_line_print_data_1110/'
    # output_path = '../../psudo_chinese_data/gen_line_data_1210_delta/'.replace('/', os.sep)
    output_path = '/database/gen_line_data_250101_font_old/'.replace('/', os.sep)

    # label_path = f'{output_path}labels/'.replace('/', os.sep)
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    # if not os.path.exists(label_path):
    #    os.makedirs(label_path),,exist_ok=True
    random_font = True
    random_seq = True

    # 加载单个汉字图片
    zidonghua_data = load_local_images_pub(image_pub_directory, num_font, num_font_off_set)

    # 读取corpus #'all_chinese_dicts_standard.txt','all_english_dicts_standard.txt','xdhy_corpus2_standard.txt','xdhy_corpus_book.txt','xdhy_corpus_book.txt'
    corpus_list = ['all_corpus_standard.txt']
    corpus_path = './corpus/'
    corpus_content = []

    for file in corpus_list:
        print(file)
        path_corpus = os.path.join(corpus_path, file)
        with open(path_corpus, 'r', encoding='utf-8') as f:
            for line in f:
                translation = chinesepun2englishpun(line.strip())
                corpus_content.append(translation)
    print("corpus exam finished")

    # 遍历字体，每种字体生成一套数据，后面不够的轮回前面的字体 num_font
    for i_font in tqdm(range(num_font), total=num_font):
        # if i_font  < 67:
        #     print(i_font,"continue")
        #     continue

        label_content = {}
        for index_line, line in enumerate(corpus_content):
            create_handwritten_number_image_pub_by_corpus(i_font, index_line, line, output_path, zidonghua_data)
        # 输出labels
        output_sub = os.path.join(output_path, str(i_font + num_font_off_set + PREVIOUS_FONT_INDEX))
        print(output_sub)
        os.makedirs(output_sub, exist_ok=True)
        label_file = os.path.join(output_sub, 'label.json')
        with open(label_file, 'w', encoding='utf-8') as f:
            json.dump(label_content, f, ensure_ascii=False, indent=4)
    # 保存标签






