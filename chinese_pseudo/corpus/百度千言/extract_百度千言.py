# import json
#
#
# def process_large_json(file_path):
#     # 打开大文件并按行逐个加载
#     with open(file_path, 'r', encoding='utf-8') as file:
#         # 使用 JSONDecoder 逐条解析
#         decoder = json.JSONDecoder()
#         buffer = ''
#
#         for line in file:
#             buffer += line.strip()
#             # 尝试解析 JSON
#             try:
#                 while buffer:
#                     # 尝试解码一个完整的 JSON 对象
#                     obj, index = decoder.raw_decode(buffer)
#                     print(obj)  # 可以替换为你需要的处理逻辑
#                     # 更新 buffer，去除已解析部分
#                     buffer = buffer[index:].strip()
#             except json.JSONDecodeError:
#                 # 如果遇到不完整的 JSON，继续读入更多数据
#                 continue
#
#
# # 传入你的大 JSON 文件路径
# file_path = ('tencent/dev.txt')
# process_large_json(file_path)

import json
import os

def extract_values(data):
    """递归提取 JSON 数据中的所有值，并过滤掉空值"""
    if isinstance(data, dict):
        for key, value in data.items():
            yield from extract_values(value)  # 递归提取字典中的值
    elif isinstance(data, list):
        for item in data:
            yield from extract_values(item)  # 递归提取列表中的值
    else:
        if data:  # 只返回非空的值
            yield str(data).replace(" ", "")  # 去掉空格


def process_large_json(file_path, output_file):
    """处理大 JSON 文件并将提取的值写入输出文件"""
    # 打开大文件并按行逐个加载
    with open(file_path, 'r', encoding='utf-8') as file:
        # 使用 JSONDecoder 逐条解析
        decoder = json.JSONDecoder()
        buffer = ''

        for line in file:
            buffer += line.strip()
            # 尝试解析 JSON
            try:
                while buffer:
                    # 尝试解码一个完整的 JSON 对象
                    obj, index = decoder.raw_decode(buffer)
                    # 提取并写入所有非空的值
                    for value in extract_values(obj):
                        output_file.write(value + '\n')  # 将值写入文件，每个值占一行
                    # 更新 buffer，去除已解析部分
                    buffer = buffer[index:].strip()
            except json.JSONDecodeError:
                # 如果遇到不完整的 JSON，继续读入更多数据
                continue


# 设置输入文件目录和输出文件路径
input_file_path = './'  # 输入文件所在目录
output_file_path = 'output.txt'

# 打开输出文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # 遍历目录中的文件
    for file_name in os.listdir(input_file_path):
        file_path = os.path.join(input_file_path, file_name)  # 构建完整路径

        if os.path.isdir(file_path):  # 如果是目录
            for subfile_name in os.listdir(file_path):
                subfile_path = os.path.join(file_path, subfile_name)  # 子文件的完整路径
                if subfile_name.endswith('.json') or subfile_name.endswith('.txt'):  # 只处理 .json 和 .txt 文件
                    process_large_json(subfile_path, output_file)
        elif file_name.endswith('.json') or file_name.endswith('.txt'):  # 处理当前目录中的文件
            process_large_json(file_path, output_file)
