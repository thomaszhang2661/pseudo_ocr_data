import os
output_dir = "C:/Users/ThomasZhang/PycharmProjects/pseudo_chinese_images_1216/"  #"/Volumes/Samsung SSD/字体/1213_font/"

delete_list=["微软简粗黑---【大湾区数据】.TTF---【大湾区数据】","白舟白雨書体---【大湾区数据】","白舟白雨書体---【大湾区数据】1","微软简粗黑---【大湾区数据】.TTF---【大湾区数据】",
             "新罗马斜体---【大湾区数据】","新罗马斜粗体---【大湾区数据】","新罗马粗体---【大湾区数据】","新罗马常规---【大湾区数据】","方正仿宋"]

for root,dirs,files in os.walk(output_dir):

    #print(root,dirs,files)
    for file_name in files:
        if file_name.split("_")[0] in delete_list:
            os.remove(root+"/"+file_name)
            print(f"Deleted {file_name}")
    # for
    # if file_name in delete_list:
    #     os.remove(output_dir+file_name)
    #     print(f"Deleted {file_name}")