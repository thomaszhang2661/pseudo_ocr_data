# -*- coding: utf-8 -*-

import os
import json
import re


def rename_files(mapping_file, target_directory):
    # 读取映射文件
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    group_name = re.sub(r"(gnt[\d\.]+)/", r"char_dict_\1.txt", target_directory)

    # 遍历映射，重命名文件
    for file, items in mapping.items():
        if file != group_name:
           continue
        for item in reversed(items):
            for key, value in item.items():
                # 获取对应的文件
                current_name = os.path.join(target_directory, str(value[0]).zfill(5))
                new_name = os.path.join(target_directory, str(value[1]).zfill(5))
                new_name = new_name + "_new"
                # 检查文件是否存在，然后重命名
                if os.path.isdir(current_name):
                    os.rename(current_name, new_name)
                    print(f"重命名：{current_name} -> {new_name}")
                else:
                    print(f"文件 {current_name} 不存在，跳过...")

# 调用函数
target_directory = "../../pic_chinese_char/gnt1.1/"
mapping_file = "mapping.txt"  # 假设映射文件为 mapping.txt
rename_files(mapping_file, target_directory)
