import random
import numpy as np
import pandas
import pandas as pd
import ast
import json
import pickle
import os
import cv2
from PIL import Image, ImageDraw, ImageFont


def simulate_copy_effect(image, contrast_factor=0.6, brightness_black=50, brightness_white=100):
    # Adjust contrast and brightness
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=-brightness_black)

    # Clip values to ensure they stay within [0, 255] range
    final_image = np.clip(adjusted_image, brightness_black, 255 - brightness_white).astype(np.uint8)

    return final_image


with open('char_dict', 'rb') as f:
    char_dict = pickle.load(f)
df = pd.read_csv('数据.csv', encoding='utf-8')
name_li = ast.literal_eval(df.columns[0])
name_li = [i for i in name_li if i != '']
char_ran = ['笑', '牛', '虎', '龙', '洋']
count1 = 0
for name in name_li:
    z_name = ""
    if count1 >= 100:
        break
    name_pic_li = []
    name_wei = 0
    name_hei = 0
    for ch in name:
        name_ind = char_dict.get(ch)
        if name_ind is None:
            ch = random.choice(char_ran)
            name_ind = char_dict[ch]

        z_name += ch

        dir_c = 'pic_chinese_char/' + f'{name_ind:05}'
        pic_c_li = os.listdir(dir_c)
        pic_c = random.choice(pic_c_li)
        img = cv2.imread(dir_c + '/' + pic_c)
        height, width = img.shape[:2]
        name_wei += width
        if height > name_hei:
            name_hei = height
        name_pic_li.append(img)
    name_wei1 = int(name_wei * 1.4)
    name_hei1 = int(name_hei * 1.1)
    name_pic_type_li = ['line']
    name_pic_type = random.choice(name_pic_type_li)
    if name_pic_type == 'line':
        image_line = Image.new("RGB", (name_wei1, name_hei1), color="white")
        image_line = np.array(image_line)
        image_line = image_line.astype(np.uint8)
        name_w = 0
        for ch_pic in name_pic_li:
            height1, width1 = ch_pic.shape[:2]
            image_line[int(name_hei1 - 0.05 * name_hei) - height1:int(name_hei1 - 0.05 * name_hei),
            int(0.2 * name_wei) + name_w:int(0.2 * name_wei) + name_w + width1] = ch_pic
            name_w += width1
        line_h_li = [i for i in range(5, 16)]
        line_h = random.choice(line_h_li)
        cv2.line(image_line, (int(0.1 * name_wei), int(name_hei1 - 0.1 * name_hei)),
                 (int(0.9 * name_wei), int(name_hei1 - 0.1 * name_hei)), color=(0, 0, 0))
        filename = f'chinese_image/abc_{z_name}.jpg'
        pil_img = Image.fromarray(cv2.cvtColor(image_line, cv2.COLOR_BGR2RGB))  # 转换为 RGB 格式
        pil_img.save(filename)
    elif name_pic_type == 'square':
        name_hei1 = int(name_hei * 1.2)
        daik_w_li = [i for i in range(5, 30)]
        daik_w = random.choice(daik_w_li)
        daik_w1 = random.choice(daik_w_li)
        daik_h_li = [i for i in range(1, 20)]
        daik_h = random.choice(daik_h_li)
        daik_h1 = random.choice(daik_h_li)
        image_k = Image.new("RGB", (name_wei1, name_hei1), color="white")
        image_k = np.array(image_k)
        image_k = image_k.astype(np.uint8)
        start_x = daik_w * 0.01 * name_wei
        start_y = daik_h * 0.01 * name_hei
        end_x = name_wei1 - daik_w1 * 0.01 * name_wei
        end_y = name_hei1 - daik_h1 * 0.01 * name_hei

        name_w = 0

        for ch_pic in name_pic_li:
            height1, width1 = ch_pic.shape[:2]
            image_k[int(name_hei1 - 0.1 * name_hei) - height1:int(name_hei1 - 0.1 * name_hei),
            int(0.2 * name_wei) + name_w:int(0.2 * name_wei) + name_w + width1] = ch_pic
            name_w += width1
        cv2.rectangle(image_k, (int(start_x), int(start_y)), (int(end_x), int(end_y)), (0, 0, 0), 2)
        image_k1 = image_k[int(0.05 * name_hei):int(name_hei1 - 0.05 * name_hei),
                   int(0.1 * name_wei):name_wei1 - int(0.1 * name_hei)]
        filename = f'chinese_image/abc_{z_name}.jpg'
        pil_img = Image.fromarray(cv2.cvtColor(image_k1, cv2.COLOR_BGR2RGB))  # 转换为 RGB 格式
        pil_img.save(filename)
    else:
        image_n = Image.new("RGB", (name_wei1, name_hei1), color="white")
        image_n = np.array(image_n)
        image_n = image_n.astype(np.uint8)
        name_w = 0
        for ch_pic in name_pic_li:
            height1, width1 = ch_pic.shape[:2]
            image_n[int(name_hei1 - 0.05 * name_hei) - height1:int(name_hei1 - 0.05 * name_hei),
            int(0.2 * name_wei) + name_w:int(0.2 * name_wei) + name_w + width1] = ch_pic
            name_w += width1
        filename = f'chinese_image/abc_{z_name}.jpg'
        pil_img = Image.fromarray(cv2.cvtColor(image_n, cv2.COLOR_BGR2RGB))  # 转换为 RGB 格式
        pil_img.save(filename)
    count1 += 1
