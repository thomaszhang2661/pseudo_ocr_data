import json
from tqdm import tqdm
# 读取中学词典统计数据
file_count = "../char_count_result_词典.txt"
#file_count = "result_dict1.json"
xdhycd = "XDHYCD_dictionary.json"
#previous_result = 'xdhy_corpus1.txt'

dict_list = {}
THRETHOLD = 20
result_corpus = []
result_corpus_dict = {}
def get_frequency(str_input):
    result = 0
    for x in str_input:
        if x in dict_list and dict_list[x] < THRETHOLD:
            result += 1


    return result
def add_new_value(str_input):
    str_input = str_input.strip().replace("。", "")
    if str_input in result_corpus_dict:
        return
    #result_corpus.append(str_input)
    #result_corpus_dict[str_input] = None
    if len(str_input) <= 20:
        result_corpus.append(str_input)
        result_corpus_dict[str_input] = None
    else:
        for i in range(0, len(str_input), 20):
            result_corpus.append(str_input[i:i + 20])
            result_corpus_dict[str_input[i:i + 20]] = None
    for x in str_input:
        if x in dict_list:
            dict_list[x] += 1


with open(file_count, 'r', encoding='utf-8') as file:
    content = file.readlines()
    for line in content:
        key, value = line.split(" : ")
        #dict_list.append([key,int(value)])
        dict_list[key] = int(value)
    #dict_list = json.load(file)

# with open(previous_result, 'r', encoding='utf-8') as file:
#     content = file.readlines()
#     for line in content:
#         result_corpus.append(line.strip())
#         result_corpus_dict[line.strip()] = None

# 根据dict_list 选取其中出现次数少的字在XDHYCD7th.txt中查找
with open(xdhycd, 'r', encoding='utf-8') as file:
    dictionary_xdhy = json.load(file)
    #print(dictionary_xdhy)
    #print(len(dictionary_xdhy)


# 选取次数少的字
#result = []
for key, value in tqdm(dict_list.items()):
    if value < THRETHOLD:
        temp_list = []
        for xdhy_key, xdhy_value in dictionary_xdhy.items():
            if key in xdhy_key:
                if key == "…":
                    add_new_value(xdhy_key)
                    temp_list = []
                    continue
                if xdhy_key not in result_corpus_dict and len(xdhy_key) > 1:
                    temp_list.append(xdhy_key)
                for x in xdhy_value:
                    if x not in result_corpus_dict:
                        temp_list.append(x)
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
with open("xdhy_corpus2.txt", 'w', encoding='utf-8') as file:
    for x in result_corpus:
        file.write(x + "\n")
with open("result_dict2.json", 'w', encoding='utf-8') as file:
    json.dump(dict_list, file, ensure_ascii=False)