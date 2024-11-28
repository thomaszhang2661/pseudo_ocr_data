# 作者：张健 Thomas Zhang
# 时间：2024/11/28,10:00
# https://blog.csdn.net/DaGongJiGuoMaLu09/article/details/107050519

import struct
import os
import cv2 as cv
import numpy as np
from tqdm import tqdm

def read_from_dgrl(dgrl):
    if not os.path.exists(dgrl):
        print('DGRL not exis!')
        return

    dir_name, base_name = os.path.split(dgrl)
    label_dir = dir_name + '_label'
    image_dir = dir_name + '_images'
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    with open(dgrl, 'rb') as f:
        # 读取表头尺寸
        header_size = np.fromfile(f, dtype='uint8', count=4)
        header_size = header_size.astype(int)
        header_size = sum([j << (i * 8) for i, j in enumerate(header_size)])
        # print(header_size)

        # 读取表头剩下内容，提取 code_length
        header = np.fromfile(f, dtype='uint8', count=header_size - 4)
        header = header.astype(int)
        code_length = sum([j << (i * 8) for i, j in enumerate(header[-4:-2])])
        # print(code_length)

        # 读取图像尺寸信息，提取图像中行数量
        image_record = np.fromfile(f, dtype='uint8', count=12)
        image_record = image_record.astype(int)
        height = sum([j << (i * 8) for i, j in enumerate(image_record[:4])])
        width = sum([j << (i * 8) for i, j in enumerate(image_record[4:8])])
        line_num = sum([j << (i * 8) for i, j in enumerate(image_record[8:])])
        #print('图像尺寸:')
        #print(height, width, line_num)

        # 读取每一行的信息
        for k in range(line_num):
            #print(k + 1)

            # 读取该行的字符数量
            char_num = np.fromfile(f, dtype='uint8', count=4)
            char_num = char_num.astype(int)
            char_num = sum([j << (i * 8) for i, j in enumerate(char_num)])
            #print('字符数量:', char_num)

            # 读取该行的标注信息
            label = np.fromfile(f, dtype='uint8', count=code_length * char_num)
            label = label.astype(int)
            label = [label[i] << (8 * (i % code_length)) for i in range(code_length * char_num)]
            label = [sum(label[i * code_length:(i + 1) * code_length]) for i in range(char_num)]
            label = [struct.pack('I', i).decode('gbk', 'ignore')[0] for i in label]
            #print('合并前：', label)
            label = ''.join(label)
            label = ''.join(label.split(b'\x00'.decode()))  # 去掉不可见字符 \x00，这一步不加的话后面保存的内容会出现看不见的问题
            #print('合并后：', label)

            # 读取该行的位置和尺寸
            pos_size = np.fromfile(f, dtype='uint8', count=16)
            pos_size = pos_size.astype(int)
            y = sum([j << (i * 8) for i, j in enumerate(pos_size[:4])])
            x = sum([j << (i * 8) for i, j in enumerate(pos_size[4:8])])
            h = sum([j << (i * 8) for i, j in enumerate(pos_size[8:12])])
            w = sum([j << (i * 8) for i, j in enumerate(pos_size[12:])])
            # print(x, y, w, h)

            # 读取该行的图片
            bitmap = np.fromfile(f, dtype='uint8', count=h * w)
            bitmap = bitmap.astype(int)
            bitmap = np.array(bitmap).reshape(h, w)

            # 保存信息
            label_file = os.path.join(label_dir, base_name.replace('.dgrl', '_' + str(k) + '.txt'))
            with open(label_file, 'w') as f1:
                f1.write(label)
            bitmap_file = os.path.join(image_dir, base_name.replace('.dgrl', '_' + str(k) + '.jpg'))
            cv.imwrite(bitmap_file, bitmap)

if __name__ == '__main__':
    dgrl_path = '../../HWDB2.2/'
    for file_name in tqdm(os.listdir(dgrl_path)):
        if file_name.endswith('.dgrl'):
            file_path = os.path.join(dgrl_path, file_name)
            read_from_dgrl(file_path)