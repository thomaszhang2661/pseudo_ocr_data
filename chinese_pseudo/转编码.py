# -*- coding: utf-8 -*-
import os


# 定义转换文件编码的函数
def convert_gbk_to_utf8(input_file, output_file):
    # 以 GBK 编码读取文件内容
    with open(input_file, 'r', encoding='ISO-8859-1') as f:
        content = f.read()

    # 将内容写入为 UTF-8 编码的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)


# 遍历文件夹下所有的 .txt 文件
def batch_convert_files(input_folder, output_folder):
    # 确保输出文件夹存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, filename)

        # 如果是文本文件
        if filename.endswith('.txt') and os.path.isfile(input_file_path):
            # 输出文件的路径
            output_file_path = os.path.join(output_folder, filename)

            # 调用转换函数
            try:
                convert_gbk_to_utf8(input_file_path, output_file_path)
                print(f"已将 {input_file_path} 转换为 UTF-8 并保存为 {output_file_path}")
            except Exception as e:
                print(f"转换文件 {input_file_path} 时出错: {e}")


# 输入文件夹路径和输出文件夹路径
input_folder = './corpus/金庸小说'  # 原始 GBK 编码文件所在的文件夹
output_folder = './corpus/金庸小说_utf8'  # 转换后 UTF-8 编码的文件存放的文件夹

# 批量处理文件夹中的文件
batch_convert_files(input_folder, output_folder)
