# 作者：张健 Thomas Zhang
# 时间：2024/12/1,20:34
from collections import Counter


def count_characters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 统计每个字符出现的次数
    char_count = Counter(text)

    # 计算总字符数（包括各种符号）
    total_chars = sum(char_count.values())

    # 打印每个字符及其出现的次数
    print("字符出现次数统计：")
    for char, count in char_count.items():
        print(f"'{char}': {count}")

    print("\n总字符数（包括符号）：", total_chars)

    # 返回统计结果
    return char_count, total_chars


# 输入文件路径
file_path = 'output_chinese.txt'  # 替换为您的文件路径

# 调用函数统计字符
char_count, total_chars = count_characters(file_path)
