import json
import random

pre_dict_path = 'selected_books/result_dict_book.json'

with open(pre_dict_path, 'r', encoding='utf-8') as file:
    pre_dict = json.load(file)

random_dict = {}
for key,value in pre_dict.items():
    if value < 10:
        print(key,value)
        random_dict[key] = 10 - value

# 从random_dict中随机生成文本，每行5-30个字
result = []
while random_dict:
    # 随机确定本次处理的元素数量
    chunk = random.randint(5, 30)

    # 随机选择指定数量的键
    keys = random.choices(list(random_dict.keys()), k=chunk)

    # 处理选中的键
    for key in keys:
        if key in random_dict:  # 确保键仍然存在
            random_dict[key] -= 1
            if random_dict[key] <= 0:
                del random_dict[key]  # 使用 del 更高效删除键

    # 将当前结果添加到结果列表
    result.append(''.join(keys))

print(result)
with open('random_补充.txt', 'w', encoding='utf-8') as file:
    for line in result:
        file.write(line+'\n')

