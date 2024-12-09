# 打开并读取文件


import re
import json
pattern = r'([a-zA-ZüÜǖǘǚǜāáǎàīíǐìēéěèōóǒòūúǔùüɡɡāáǎàōóǒòēéěèīíǐìūúǔùüǖǘǚǜêê̄ếê̌ềm̄ḿm̀ńňǹẑĉŝŋĀÁǍÀŌÓǑÒĒÉĚÈĪÍǏÌŪÚǓÙÜǕǗǙǛÊÊ̄ẾÊ̌ỀM̄ḾM̀ŃŇǸẐĈŜŊ❶❷❸❹❺❻❼❽❾❿⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴])'

def parse_text_to_dict(file_path):
    result_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    for index_line, line in enumerate(content):

        line = re.sub(pattern, '', line.strip())
        line_list = line.split(" ")

        key = line_list[0]
        if key == "":
            continue

        # 找到解释部分（以：分割后取后半部分）
        if len(line_list) > 1:
            explanation = line_list[1:]
        else:
            continue

        # 去除圆圈数字部分：通过正则表达式移除 '票已经卖完，一个～也没有了。❷（～儿）指椅子、凳子等可以坐的东西：搬个～儿来。‖也作坐位。'
        #explanation = re.sub(r'[\u2460-\u2473]', '', explanation)
        #explanation = re.sub(r'[❶❷❸].*', '', explanation)
        explanation = [re.sub(r'[\u2776-\u2793](.*)', '', x) for x in explanation]

        explanation = [re.sub(r'另见.*', '', x) for x in explanation]
        explanation = [re.sub(r'‖.*', '', x) for x in explanation]

        # 提取所有包含“～”的片段并替换
        values = []
        for item in explanation:
            if item == "":
                continue
            #for frag in re.split(r'[｜。(例：)]', item):
            for frag in re.split(r'[｜。\(\)\（\）\（\）❶❷❸❹❺❻❼❽❾❿⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴'
                                 r'①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
                                 r'㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿|例：|例 ：|例 ：|［例］|\[例\]'
                                 r'㊀㊁㊂㊃㊄㊅㊆㊇㊈㊉]', item):
                if key not in frag:
                    continue
                if '～' in frag:
                    if "…" in key:
                        temp_key = key.split("…")
                        #key_parts = re.findall(r'temp_key[0](.*?)temp_key[1](.*)', key)  # 提取 "连" 和 "带" 后的部分

                        part1, part2 = temp_key[0],temp_key[1]  # 获取提取的部分

                        # 替换value中的～为key部分
                        result = frag.replace('～', part1, 1).replace('～', part2, 1)
                        values.append(result.strip())
                    else:
                        values.append(frag.replace('～', key).strip())
                else:
                    values.append(frag.strip())

        # 将结果加入字典，并去重
        if len(key) > 1 or len(values) > 0:
            result_dict[key] = list(set(values))

    return result_dict
# 使用示例
file_path = '100年汉语新词新语大辞典.txt'  # 替换为实际文件路径
output_path = "100年汉语新词新语大辞典_dictionary.json"
dictionary = parse_text_to_dict(file_path)
print(dictionary)
print(len(dictionary))
# 定义文件路径


# 将字典写入到JSON文件
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=4)