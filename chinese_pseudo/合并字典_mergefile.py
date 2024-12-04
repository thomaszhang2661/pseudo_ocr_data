# # -*- coding: utf-8 -*-
#
# import os
# import shutil
# from tqdm import tqdm
#
# def merge_folders(source_folders, target_folder):
#     """
#     将多个源文件夹中的文件合并到目标文件夹中，如果目标文件夹已有同名文件，则进行重命名。
#
#     :param source_folders: 一个包含多个源文件夹路径的列表
#     :param target_folder: 目标文件夹的路径
#     """
#     # 确保目标文件夹存在
#     if not os.path.exists(target_folder):
#         os.makedirs(target_folder)
#
#     # 遍历所有源文件夹
#     for folder in source_folders:
#         if not os.path.isdir(folder):
#             print(f"源文件夹 {folder} 不存在，跳过...")
#             continue
#         # 遍历所有源文件夹
#         for folder1 in tqdm(os.listdir(folder)):
#             if not os.path.isdir(os.path.join(folder, folder1)):
#                 print(f"源文件夹 {folder1} 不存在，跳过...")
#                 continue
#             #print(f"正在处理文件夹 {folder}...")
#
#             # 遍历当前源文件夹中的所有文件
#             for filename in os.listdir(os.path.join(folder, folder1)):
#                 #source_path = os.path.join(folder, filename)
#                 #target_path = os.path.join(target_folder, filename)
#                 #source_path = os.path.join(folder, folder1, filename)
#                 #target_path = os.path.join(target_folder,folder1, filename)
#                 source_path = folder + folder1 +r"/"+ filename
#                 target_path = target_folder + folder1 +r"/"+ filename
#                 if not os.path.exists(target_folder + folder1):
#                     os.makedirs(target_folder + folder1)
#
#                 #source_path = source_path.replace(r"/", r"\\")
#                 #target_path = target_path.replace(r"/", r"\\")
#
#                 # # 如果目标文件夹中已经存在同名文件，进行重命名
#                 # counter = 1
#                 # while os.path.exists(target_path):
#                 #     # 如果目标文件已存在，修改文件名
#                 #     name, ext = os.path.splitext(filename)
#                 #     target_path = os.path.join(target_folder, f"{name}_{counter}{ext}")
#                 #     counter += 1
#
#                 # 将文件从源文件夹复制到目标文件夹
#                 try:
#                     if os.path.isfile(source_path):
#                         shutil.copy(source_path, target_path)  # 使用 copy2 保留文件的元数据
#                         #os.system(f'copy {source_path} {target_path}')
#                         #print(f"已复制 {source_path} 到 {target_path}")
#                     else:
#                         print(f"跳过非文件项 {source_path}")
#                 except Exception as e:
#                     print(f"处理文件 {source_path} 时出错: {e}")
#
#
# # 示例使用
# source_folders = [r'../../pic_chinese_char/gnt1.0/', r'../../pic_chinese_char/gnt1.1/', r'../../pic_chinese_char/gnt1.2/']  # 替换为你的源文件夹路径
# # source_folders = [os.path.join("..","..","pic_chinese_char","gnt1.0"),
# #                   os.path.join("..","..","pic_chinese_char","gnt1.1"),
# #                   os.path.join("..","..","pic_chinese_char","gnt1.2")]  # 替换为你的源文件夹路径
# target_folder = r'../../pic_chinese_char/gnt_all/'  # 替换为目标文件夹路径 os.path.join("..","..","pic_chinese_char","gnt_all")
#
# # 合并文件夹
# merge_folders(source_folders, target_folder)

import os
import shutil
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def copy_file(source_path, target_path):
    """
    将文件从源路径复制到目标路径
    """
    try:
        if os.path.isfile(source_path):
            shutil.copy2(source_path, target_path)  # 使用 copy2 保留文件的元数据
            #print(f"已复制 {source_path} 到 {target_path}")
        else:
            print(f"跳过非文件项 {source_path}")
    except Exception as e:
        print(f"处理文件 {source_path} 时出错: {e}")


def merge_folders(source_folders, target_folder):
    """
    将多个源文件夹中的文件合并到目标文件夹中，如果目标文件夹已有同名文件，则进行重命名。

    :param source_folders: 一个包含多个源文件夹路径的列表
    :param target_folder: 目标文件夹的路径
    """
    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 使用线程池加速文件复制
    with ThreadPoolExecutor(max_workers=16) as executor:  # 增加最大线程数
        # 遍历所有源文件夹
        for folder in source_folders:
            if not os.path.isdir(folder):
                print(f"源文件夹 {folder} 不存在，跳过...")
                continue

            # 遍历源文件夹中的子文件夹
            for folder1 in tqdm(os.listdir(folder), desc=f"处理 {folder}"):
                folder1_path = os.path.join(folder, folder1)

                if not os.path.isdir(folder1_path):
                    print(f"源文件夹 {folder1} 不存在，跳过...")
                    continue

                # 遍历当前源文件夹中的所有文件
                for filename in os.listdir(folder1_path):
                    source_path = os.path.join(folder, folder1, filename)
                    target_folder1_path = os.path.join(target_folder, folder1)

                    # 确保目标子文件夹存在
                    if not os.path.exists(target_folder1_path):
                        os.makedirs(target_folder1_path)

                    target_path = os.path.join(target_folder1_path, filename)

                    # 调试输出，查看复制的文件路径
                    #print(f"准备复制 {source_path} 到 {target_path}")

                    # 使用线程池提交复制任务
                    executor.submit(copy_file, source_path, target_path)


# 示例使用
source_folders = [r'../../pic_chinese_char/gnt1.0/', r'../../pic_chinese_char/gnt1.1/', r'../../pic_chinese_char/gnt1.2/']
target_folder = r'../../pic_chinese_char/gnt_all/'

# 合并文件夹
merge_folders(source_folders, target_folder)
