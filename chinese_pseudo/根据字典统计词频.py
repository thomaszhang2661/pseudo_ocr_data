
import os
import re

import chardet
from mapping_punct import chinesepun2englishpun



def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        print("encoding",result)
        return result['encoding']

# 假设字典文件路径
dict_file_path = 'merged_dict.txt'
# 假设文本文件路径
text_file_path = 'corpus/古龙全集/'

# 创建一个空字典来存放字典内容
char_dict = {}

# 读取字典文件并将其内容放入字典中
with open(dict_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # 读取字典中的每一行，按': '分割，存入字典
        key, value = line.split(' : ')
        char_dict[key] = int(value)

# 创建一个空字典来存放文本中字符出现的次数
#char_count = {key: 0 for key in char_dict}  # 初始化字典，所有字符的出现次数为0


#
char_count = {}
# with open(f'char_count_result.txt', 'r', encoding='utf-8') as f:
#     # 读取char_count
#     for line in f:
#         line = line.strip()
#         if not line:
#             continue
#         # 读取char_count中的每一行，按': '分割，存入字典
#         key, value = line.split(' : ')
#         char_count[key] = int(value)


# for file_name in os.listdir(text_file_path):
#     # 读取文本文件并统计字符出现的次数
#     file_path = os.path.join(text_file_path, file_name)
# file_path = './all_chinese_dicts_all.txt'
# file_name = 'all_chinese_dicts_all.txt'

file_path = './corpus/金庸小说/天龙八部.txt'
file_name = './corpus/金庸小说/天龙八部.txt'
    # 检查文件是否是文本文件
if os.path.isfile(file_path) and file_name.endswith('.txt'):
    print(f"Processing file: {file_name}")
    # 读取文本文件并统计字符出现的次数
    encoding = detect_encoding(file_path)
    print(encoding)
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        text = f.read()
        text = chinesepun2englishpun(text)
        for char in text:
            # 如果字符在字典中，增加计数
            #print(char)
            if char in char_dict:
                #char_count[char] += 1
                char_count[char] = char_count.get(char, 0) + 1
            else:
                # 假设你要打印的字符是 `char`
                print("not in",char)
                #pass
                #print(f"Character '{char.encode('utf-8', errors='replace').decode('utf-8')}' not in dictionary")

# 输出统计结果
# for key, count in char_count.items():
#     #if count > 0:  # 只输出出现次数大于0的字符
#     print(f'{key} : {count}')

# 将统计结果保存为输出文件
total = 0
with open(f'char_count_result_天龙.txt', 'w', encoding='utf-8') as output_file:
    #for key, count in char_count.items():
        #output_file.write(f'{key} : {count}\n')
    for key, value in char_dict.items():
        #if count > 0:  # 只写入出现次数大于0的字符
        output_file.write(f'{key} : {char_count.get(key, 0)}\n')
        total += char_count.get(key, 0)
    output_file.write(f'Total : {total}\n')

