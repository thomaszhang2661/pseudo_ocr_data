from tqdm import tqdm
import os

path_font = "C:/Users/ThomasZhang/PycharmProjects/pseudo_chinese_images_1231"
#for root,dirs,files in tqdm(os.walk(path_font),total=len(os.listdir(path_font))):
for dir in os.listdir(path_font):
    #new_dir = str(int(dir) - 2000)
    # 改成4位数字
    new_dir = dir.zfill(4)
    #修改文件名
    os.rename(path_font+"/"+dir,path_font+"/"+new_dir)
