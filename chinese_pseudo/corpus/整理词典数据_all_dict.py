# import os
# path_input = 'all_english_dicts.txt'
# path_output = 'all_english_dicts_standard.txt'
#
# result = []
# with open(path_input, 'r', encoding='utf-8') as file:
#     content = file.readlines()
#     for line in content:
#         line = line.strip()
#         line_list = line.split()
#         if len(line_list) < 8 and len(line) < 50:
#             result.append(line)
#         else:
#             for i in range(0, len(line_list), 5):
#                 result.append(" ".join(line_list[i:i + 5]))
#
# with open(path_output, 'w', encoding='utf-8') as file:
#     for line in result:
#         file.write(line + "\n")

# import os
# import re
# path_input = 'all_chinese_dicts_all.txt'
# path_output = 'all_chinese_dicts_standard.txt'
#
# result = []
# with open(path_input, 'r', encoding='utf-8') as file:
#     content = file.readlines()
#     for line in content:
#         line = line.strip()
#         line = line.replace('word group',"")
#         line_list = re.split('[，；（）()]',line)
#         line_list = [x for x in line_list if x]
#         if len(line) < 20:
#             result.append(line)
#         else:
#             if len(line_list) > 1 and len(line)/len(line_list) < 20:
#                 num_chunks = (15 * len(line_list)) // len(line)
#                 if num_chunks == 0:
#                     num_chunks = 1
#                 for i in range(0, len(line_list), num_chunks):
#                     result.append(" ".join(line_list[i:i + num_chunks]))
#             else:
#                 for i in range(0, len(line), 15):
#                     result.append(line[i:i + 15])
#
# with open(path_output, 'w', encoding='utf-8') as file:
#     for line in result:
#         file.write(line + "\n")


import os
import re
path_input = 'xdhy_corpus2.txt'
path_output = 'xdhy_corpus2_standard.txt'
pattern = r'([a-zA-ZüÜāáǎàīíǐìēéěèōóǒòūúǔùüɡɡ])'

result = []
with open(path_input, 'r', encoding='utf-8') as file:
    content = file.readlines()
    for line in content:
        line = line.strip()
        # 删除拼音
        line = re.sub(pattern, '', line)
        line = line.replace("()", "")
        line = line.replace("（）", "")


        line_list = re.split('[，；（）()]',line)
        line_list = [x for x in line_list if x]
        if len(line) < 20:
            result.append(line)
        else:
            if len(line_list) > 1 and len(line)/len(line_list) < 20:
                num_chunks = (15 * len(line_list)) // len(line)
                if num_chunks == 0:
                    num_chunks = 1
                for i in range(0, len(line_list), num_chunks):
                    result.append(" ".join(line_list[i:i + num_chunks]))
            else:
                for i in range(0, len(line), 15):
                    result.append(line[i:i + 15])

with open(path_output, 'w', encoding='utf-8') as file:
    for line in result:
        file.write(line + "\n")

