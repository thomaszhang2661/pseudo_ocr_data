
import os

import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

# 假设字典文件路径
dict_file_path = 'merged_dict.txt'
# 假设文本文件路径
text_file_path = 'corpus/金庸小说/'

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
char_count = {key: 0 for key in char_dict}  # 初始化字典，所有字符的出现次数为0


for file_name in os.listdir(text_file_path):
    # 读取文本文件并统计字符出现的次数
    file_path = os.path.join(text_file_path, file_name)

    # 检查文件是否是文本文件
    if os.path.isfile(file_path) and file_name.endswith('.txt'):
        print(f"Processing file: {file_name}")
        # 读取文本文件并统计字符出现的次数
        encoding = detect_encoding(file_path)
        print(encoding)
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            text = f.read()
            for char in text:
                # 如果字符在字典中，增加计数
                #print(char)
                if char in char_dict:
                    char_count[char] += 1
                else:
                    # 假设你要打印的字符是 `char`
                    pass
                    #print(f"Character '{char.encode('utf-8', errors='replace').decode('utf-8')}' not in dictionary")

# 输出统计结果
for key, count in char_count.items():
    #if count > 0:  # 只输出出现次数大于0的字符
    print(f'{key} : {count}')

# 将统计结果保存为输出文件
with open(f'char_count_result_金庸.txt', 'w', encoding='utf-8') as output_file:
    for key, count in char_count.items():
        #if count > 0:  # 只写入出现次数大于0的字符
        output_file.write(f'{key} : {count}\n')
