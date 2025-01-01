import os
from tqdm import tqdm
problem_font=["立体铁山硬笔行楷简",
              "王正良硬笔楷书立体简",
              "Cabin-Regular",
              "PublicSans-Regular-14",
              "蔡云汉硬笔行书繁书法字体",
              "陈代明硬笔体",
              "李洤迷宫草书",
              "傲世九重天(1)",
              "把侧妃呵呵(1)",
              "段宁硬笔行书---【大湾区数据】.ttf---【大湾区数据】",
              "段宁硬笔行书1.0",
              "德彪钢笔行书字体",
              "李洤迷宫草书",
              "钟齐李洤标准草书符号",
              "钟齐陈伟勋硬笔行楷繁",
              "衡山毛筆草書",
              "腾祥铁山硬隶繁",
              "方正字迹-朱涛钢笔行书繁体",
              "方正字迹-王伟钢笔行书繁体",
              "方正字迹-佩安硬笔繁体",
              "方正字迹-刘郢硬笔繁体",
              "方正硬笔楷书繁体",
              "方正硬笔行书繁体",
              "刘佳尚5500行楷",
              "汉仪家书繁",
              "汉仪瘦金书繁",
              "司马彦行书",
              "汉仪春然手书繁",
              "郑庆科黄油体",
              "华康金文体",
              "傲世九重天",
              "腾祥伯当行书---【大湾区数据】",
              "李豪手迹",
              "腾祥铚谦钢笔繁",
              "腾祥铁山硬隶繁",
              "钟齐陈伟勋硬笔行楷繁",
              "呵呵呵呵呵鸡体",
              "草草草草草草书(1)",
              "方正瘦金书繁体",
              "阿美手写体",
              "方正瘦金书繁体",
              "钟齐流江硬笔草体",
              "变更大夏(1)",
              "陈氏家族体(1)"]

# path_font = "C:/Users/ThomasZhang/PycharmProjects/pseudo_chinese_images_1231"
#
# for root,dirs,files in tqdm(os.walk(path_font),total=len(os.listdir(path_font))):
#     for file_name in files:
#         if file_name.split("_")[0] in problem_font:
#             os.remove(root+"/"+file_name)
#             #print(f"Deleted {file_name}")

path_font = "C:/Users/ThomasZhang/Desktop/selected_hw_1"
for root,dirs,files in tqdm(os.walk(path_font),total=len(os.listdir(path_font))):
    for file_name in files:
        if file_name.split(".")[0] in problem_font:
            os.remove(root+"/"+file_name)
            print(f"Deleted {file_name}")


