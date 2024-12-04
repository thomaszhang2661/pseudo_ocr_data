# 作者：张健 Thomas Zhang
# 时间：2024/12/1,20:31
# 提取包含中文的列
def extract_chinese(input_file, output_file):
    chinese_sentences = []

    with open(input_file, 'r', encoding='utf-8') as file:
        # 读取第一行作为表头
        headers = file.readline().strip().split('\t')

        # 找到中文(zh)列的索引
        zh_index = headers.index('zh') if 'zh' in headers else None
        if zh_index is None:
            print("没有找到中文列 (zh)!")
            return

        # 逐行读取中文内容
        for line in file:
            columns = line.strip().split('\t')
            if len(columns) > zh_index:
                chinese_sentences.append(columns[zh_index])

    # 将提取到的中文内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as output:
        for sentence in chinese_sentences:
            output.write(sentence + '\n')

    print(f"中文内容已提取并保存到 {output_file}")


# 输入和输出文件路径
input_path = 'xnli.15way.orig.tsv'  # 替换为实际输入文件路径
output_path = 'output_chinese.txt'  # 替换为实际输出文件路径

# 调用函数提取中文
extract_chinese(input_path, output_path)
