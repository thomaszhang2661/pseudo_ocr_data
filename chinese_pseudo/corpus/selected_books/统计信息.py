import json

with open('result_dict_book.json', 'r', encoding='utf-8') as file:
    pre_dict = json.load(file)

count = 0
for key,value in pre_dict.items():
    if value < 10:
        print(key,value)
        count += 1
print(count)