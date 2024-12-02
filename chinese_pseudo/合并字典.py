# -*- coding: utf-8 -*-

import os

import os
print("当前工作目录:", os.getcwd())
# 假设我们有三个 txt 文件，包含字典内容
files = ['../../pic_chinese_char/char_dict_gnt1.0.txt', '../../pic_chinese_char/char_dict_gnt1.1.txt', '../../pic_chinese_char/char_dict_gnt1.2.txt']

# 创建一个空字典来存放合并后的结果
merged_dict = []

# 逐个读取文件并合并字典内容
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        # 逐行读取文件
        for line in f:
            # 删除行两端的空白字符
            line = line.strip()
            line = line.replace('\x00', '')  # 移除 '\x00' 字符

            # 跳过空行
            if not line:
                continue
            print(line)
            # 分割键和值
            key, value = line.split(': ')

            # 更新字典，自动去除重复的键
            merged_dict.append(key)

# 将合并后的字典保存为新文件
with open('merged_dict.txt', 'w', encoding='utf-8') as output_file:
    for i_word, word in enumerate(merged_dict):
        output_file.write(f'{word} : {i_word + 1}\n')

# # 打印合并后的字典
# for key, value in merged_dict.items():
#     print(f'{key} : {value}')
