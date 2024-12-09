import json
from tqdm import tqdm
import os
from mapping_punct import *
import chardet
import random
# 读取现有corpus的词频统计
file_count = "../special_dict/result_dict_100年新词.json"
books_path = '汉语大词典(简体精排,339937条).txt'
previous_result = '../special_dict/all_corpus_standard.txt'
pattern = r'([a-zA-ZüÜǖǘǚǜāáǎàīíǐìēéěèōóǒòūúǔùüɡɡāáǎàōóǒòēéěèīíǐìūúǔùüǖǘǚǜêê̄ếê̌ềm̄ḿm̀ńňǹẑĉŝŋĀÁǍÀŌÓǑÒĒÉĚÈĪÍǏÌŪÚǓÙÜǕǗǙǛÊÊ̄ẾÊ̌ỀM̄ḾM̀ŃŇǸẐĈŜŊ❶❷❸❹❺❻❼❽❾❿⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴])'

dict_list = {}
THRETHOLD = 20
result_corpus = []
result_corpus_dict = {}
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        print("encoding",result)
        return result['encoding']

def get_frequency(str_input):
    result = 0
    for x in str_input:
        if x in dict_list and dict_list[x] < THRETHOLD:
            result += 1
    return result
def add_new_value(str_input):
    if str_input in result_corpus_dict:
        return
    result_corpus.append(str_input)
    result_corpus_dict[str_input] = None
    for x in str_input:
        if x in dict_list:
            dict_list[x] += 1


with open(file_count, 'r', encoding='utf-8') as file:
    # content = file.readlines()
    # for line in content:
    #     key, value = line.split(" : ")
    #     #dict_list.append([key,int(value)])
    #     dict_list[key] = int(value)
    dict_list = json.load(file)


with open(previous_result, 'r', encoding='utf-8') as file:
    content = file.readlines()
    for line in content:
        #result_corpus.append(line.strip())
        result_corpus_dict[line.strip()] = None


# # 根据dict_list 选取其中出现次数少的字在XDHYCD7th.txt中查找
# with open(xdhycd, 'r', encoding='utf-8') as file:
#     dictionary_xdhy = json.load(file)
#     #print(dictionary_xdhy)
#     #print(len(dictionary_xdhy)

book_dict = {}

def get_book_dict(lines):
    for line in lines:
        #line = chinesepun2englishpun(line)
        line = line.strip()
        line = re.sub(pattern, '', line.strip())

        line_list = line.split("[,。]")
        for x in line_list:
            if len(x) <= 30:
                book_dict[x] = None
            else:
                chunk = random.randint(5,30)
                for i in range(0, len(x), chunk):
                    book_dict[x[i:i+chunk]] = None


# 读取文件夹内的所有文件
# for file in os.listdir(books_path):
#     #print(file)
#     if file.endswith(".txt"):
#         encoding = detect_encoding(os.path.join(books_path, file))
#         if encoding == 'GB2312' or encoding == 'GBK':
#             encoding = 'GB18030'
#         #print(encoding)
#         with open(os.path.join(books_path, file), 'r', encoding=encoding, errors='ignore') as f:
#             content = f.readlines()
#             get_book_dict(content)

    #print(file)
# encoding = detect_encoding(books_path)
# if encoding == 'GB2312' or encoding == 'GBK':
#     encoding = 'GB18030'
#print(encoding)
with open(books_path, 'r', encoding="utf-8", errors='ignore') as f:
    content = f.readlines()
    get_book_dict(content)



# 选取次数少的字
#result = []
for idx, (key, value) in tqdm(enumerate(dict_list.items()),total=len(dict_list)):
    if idx > 170 and value < THRETHOLD:
        temp_list = []
        for xdhy_key, xdhy_value in book_dict.items():

            if key in xdhy_key:
                # if key == "…":
                #     add_new_value(xdhy_key)
                #     temp_list = []
                #     continue
                if xdhy_key not in result_corpus_dict and len(xdhy_key) > 1:
                    temp_list.append(xdhy_key)
                # for x in xdhy_value:
                #     if x not in result_corpus_dict:
                #         temp_list.append(x)

        else:
            if len(temp_list) > 0:
            # 如果加入temp_list后不超过THRETHOLD，全部加入
                if len(temp_list) + dict_list[key] <= THRETHOLD:
                    for x in temp_list:
                        add_new_value(x)
                else:
                    # 如果超过THRETHOLD，选取生僻字多的
                    num_need = THRETHOLD - dict_list[key]
                    freq = []
                    for x in temp_list:
                        freq.append(get_frequency(x))
                    sorted_temp_list = [val for _, val in sorted(zip(freq, temp_list), key=lambda x: x[0],reverse=True)]
                    for x in sorted_temp_list[:num_need]:
                        add_new_value(x)

                    #min_index, min_value = max(enumerate(freq), key=lambda x: x[1])
                    #temp_value = temp_list[min_index]


                # min_index, min_value = max(enumerate(freq), key=lambda x: x[1])
                # temp_value = temp_list[min_index]
                # add_new_value(temp_value)

            # elif len(xdhy_key) > 1:
            #     add_new_value(xdhy_key)

# 输出结果
print(result_corpus)
print(dict_list)

# 输出到文件
with open("汉语大词典_corpus.txt", 'w', encoding='utf-8') as file:
    for x in result_corpus:
        file.write(x + "\n")
with open("result_dict_汉语大词典.json", 'w', encoding='utf-8') as file:
    json.dump(dict_list, file, ensure_ascii=False)