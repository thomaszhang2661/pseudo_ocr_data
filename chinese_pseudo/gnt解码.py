# 作者：张健 Thomas Zhang
# 时间：2024/11/27,23:07
#
# https://blog.csdn.net/shiwanghualuo/article/details/119648829
# https://blog.csdn.net/sinat_28442665/article/details/109477806
# https://blog.csdn.net/DaGongJiGuoMaLu09/article/details/107050519
import os
import numpy as np
import struct
from PIL import Image
from tqdm import tqdm

# data文件夹存放转换后的.png文件
data_dir = '../../pic_chinese_char/gnt1.1_new/'
# 路径为存放数据集解压后的.gnt文件
train_data_dir = '../../all_chinese_char1.1/'
# test_data_dir = os.path.join(data_dir, 'F:/Datasets/HWDB1.0/gnttest')
if not os.path.exists(train_data_dir):
    os.makedirs(train_data_dir)

def read_from_gnt_dir(gnt_dir=train_data_dir):
    def one_file(f):
        header_size = 10
        while True:
            header = np.fromfile(f, dtype='uint8', count=header_size)
            if not header.size: break
            header = [int(x) for x in header]
            sample_size = header[0] + (header[1] << 8) + (header[2] << 16) + (header[3] << 24)
            tagcode = header[5] + (header[4] << 8)
            width = header[6] + (header[7] << 8)
            height = header[8] + (header[9] << 8)
            if header_size + width * height != sample_size:
                break
            image = np.fromfile(f, dtype='uint8', count=width * height).reshape((height, width))
            yield image, tagcode
    total = len(os.listdir(gnt_dir))
    for file_name in tqdm(os.listdir(gnt_dir),total=total):
        if file_name.endswith('.gnt'):
            file_path = os.path.join(gnt_dir, file_name)
            with open(file_path, 'rb') as f:
                for image, tagcode in one_file(f):
                    yield image, tagcode

char_set = set()
for _, tagcode in read_from_gnt_dir(gnt_dir=train_data_dir):
    tagcode_unicode = struct.pack('>H', tagcode).decode('gbk')
    char_set.add(tagcode_unicode)
char_list = list(char_set)
char_dict1 = dict(zip(sorted(char_list), range(len(char_list))))
char_dict = {}
for k in char_dict1.keys():
    # if char_dict1[k] <= 168 or char_dict1[k] in [3924, 3925]:
    #     continue
    # else:
    char_dict[k] = char_dict1[k]

print(len(char_dict))
print("char_dict=", char_dict)

# import pickle
#
# f = open('char_dict', 'wb')
# pickle.dump(char_dict, f)
# f.close()

# 保存字符字典为 txt 文件
with open('char_dict_tmp.txt', 'w', encoding='utf-8') as f:
    for key, value in char_dict.items():
        # 每行存储一个键值对，格式为 "key: value"
        f.write(f"{key}: {value}\n")

train_counter = 0
test_counter = 0
for image, tagcode in read_from_gnt_dir(gnt_dir=train_data_dir):
    tagcode_unicode = struct.pack('>H', tagcode).decode('gbk')
    if tagcode_unicode not in char_dict.keys():
        continue
    im = Image.fromarray(image)
# 路径为data文件夹下的子文件夹，train为存放训练集.png的文件夹
    dir_name = f'{data_dir}' + '%0.5d' % char_dict[tagcode_unicode]
    # if not os.path.exists(dir_name):
    #     #     os.mkdir(dir_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)  # 使用 makedirs 来确保父目录也被创建
    try:
        im.convert('L').save(dir_name + '/' + str(train_counter) + '.png')
    except Exception as e:
        print(e)
        print("tagcode_unicode=", tagcode_unicode)
    #print("train_counter=", train_counter)
    train_counter += 1


# for image, tagcode in read_from_gnt_dir(gnt_dir=test_data_dir):
#     tagcode_unicode = struct.pack('>H', tagcode).decode('gb2312')
#     im = Image.fromarray(image)
# # 路径为data文件夹下的子文件夹，test为存放测试集.png的文件夹
#     dir_name = 'F:/Datasets/HWDB1.0/pngtest/' + '%0.5d' % char_dict[tagcode_unicode]
#     if not os.path.exists(dir_name):
#         os.mkdir(dir_name)
#     im.convert('RGB').save(dir_name + '/' + str(test_counter) + '.png')
#     print("test_counter=", test_counter)
#     test_counter += 1
