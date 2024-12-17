import json

merged_dict = {}
with open('merged_dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        key, value = line.strip().split(' : ')
        merged_dict[key] = int(value)

new_list = []
with open('需要添加的汉字', 'r', encoding='utf-8') as f:
    for line in f:
        new_list.append(line.strip())

count = len(merged_dict)

for c in new_list:
    if c not in merged_dict:
        count += 1
        merged_dict[c] = count

# 保存新的字典
with open('merged_dict_new.txt', 'w', encoding='utf-8') as f:
    for key, value in merged_dict.items():
        f.write(f'{key} : {value}\n')

with open('merged_dict.json', 'r', encoding='utf-8') as f:
    json.dump(merged_dict, f, ensure_ascii=False, indent=4)