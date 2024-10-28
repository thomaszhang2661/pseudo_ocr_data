# 作者：张健 Thomas Zhang
# 时间：2024/10/26,22:13
##########################################################
# """转存字典的格式"""
# import pickle
#
# # 读取字符字典
# with open('chinese_data1018/char_dict', 'rb') as f:
#     char_dict = pickle.load(f)
#
# # 存储字典到txt文件
# with open('char_dict.txt', 'w', encoding='utf-8') as f:
#     for char, code in char_dict.items():
#         f.write(f"{char}\t{code}\n")
############################################################
#
# """查找3500词中字典没有的汉字"""
# import pandas as pd
# import re
# # 读取 Excel 文件
# #file_path = 'chinese_data1018/课标词汇3500.xlsx'  # 替换为你的文件路径
# file_path = 'chinese_data1018/新课标1600词词表.xlsx'  # 替换为你的文件路径
#
# df = pd.read_excel(file_path, engine='openpyxl')
# # 提取某一列的所有内容
# column_name = '释义'  # 替换为你想要提取的列名
# column_data = df[column_name]
#
#
# # 读取自动化所字典
# char_dict = {}
#
# # 读取字典从txt文件
# with open('char_dict.txt', 'r', encoding='utf-8') as f:
#     for line in f:
#         char, code = line.strip().split('\t')  # 按制表符分割
#         char_dict[char] = int(code)  # 将编码转换为整数
#
#
# result = []
# # 遍历列数据
# for index, value in column_data.iteritems():
#     # 使用正则表达式提取汉字
#     #chinese_characters = re.findall(r'[\u4e00-\u9fa5]', value)
#     # if type(value) != "str":
#     #     print(value,"continue")
#     #     continue
#     value = str(value)
#     chinese_characters = re.findall(r'[^a-zA-Z]', value)
#
#     # 将提取的汉字合并成一个字符串
#     print(chinese_characters)
#     for char in chinese_characters:
#         if char not in char_dict:
#             result += char
#     #result += chinese_characters
# # 使用 set 去重，并保持顺序
# result = list(dict.fromkeys(result))
# # 合并成一个字符串
# final_result = "".join(result)
# print(len(final_result), final_result)


##################################################################
# """这部分功能为转格式，转为字典格式方便直接复制"""
# # 定义包含汉字的字符串
# #characters = "126 . （，…）；湎 /;、407瘾=夙轶踝&魅尴尬闩羁蝙蝠沐()褔[]黏咧“√”哽雳咔嚓嗒饪姊肴黝<>潢惚沓-皙,
# # 锉朦胧褶浏檐嗨嗥诙飓淇髦25熨颌颚怦嗦匮跛睑槭啬煦169箴髭嘈迥踱蹚媲摞莅搡裨橄榄笃虔岖鲨愕狩烊鳐瞌霾蜿啜馊啐疱玷莓咂3：缜嘀阱遛砣祉嗯孀跤"
# characters = "30 . （，）、；…&(,)崽/哒;嬉[]踹=筝盹橘妃薇腼"
# # 只提取汉字
# import re
#
# # 提取汉字
# chinese_characters = re.findall(r'[\u4e00-\u9fa5]', characters)
#
# # 初始化字典和编号
# char_dict = {}
# start_number = 3847
#
# # 将汉字与编号关联
# for char in chinese_characters:
#     char_dict[char] = start_number
#     start_number += 1  # 编号递增
#
# # 打印结果
# for char, code in char_dict.items():
#     print(f"{char}\t{code}")
