import os
import random

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager

# 定义用于保存生成图片的输出目录
output_dir = "generated_images"
os.makedirs(output_dir, exist_ok=True)
file_path="gen_content.xlsx"
#file_path="gen_content_sent.xlsx"


texts= [r' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@$%=¥~<>[]|{}°£€']
texts1=[]
#df=pd.read_excel(file_path)
df =pd.read_excel(file_path, engine='openpyxl')

for i in df["Content"]:
    err=False
    for j in i:
        if j not in texts[0]:
            err=True
            break
    if not err:
        texts1.append(i)
print(texts1)

# 定义要生成的文本列表

#alphabet_encoding_next =  r' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@$%=¥~<>[]|{}《》°£€'

# 定义要使用的字体列表 手写体

select_list = ['Baby Doll','Chalkboard','Comic Sans MS','Craftsy','Feltful',
               'Info Story','KG Primary Italics','Marker Felt','Noteworthy',
               'Skia','Courier New','Andale Mono','Chalkboard SE','Comic Sans MS','Bradley Hand']



special_and = ['Craftsy','Marker Felt','Bradley Hand']
special_dollar =['Skia']
special_temperature =['Info Story']

trans_list = ["Autography",'Lemon Tuesday','Zapfino']
# select_list = ['Keyboard', 'New York', 'SF Compact Rounded', 'SF NS Mono', 'American Typewriter', 'Andale Mono',
#                'Arial Narrow', 'Autography', 'Avenir', 'Baby Doll',
#                'Baskerville', 'Bodoni 72', 'Bradley Hand',
#                 'Chalkboard SE', 'Chalkboard', 'Chalkduster', 'Charter', 'Comic Sans MS', 'Cochin',
#                'Courier New', 'Craftsy', 'DIN Condensed', 'Feltful', 'Futura', 'Georgia',
#                 'Info Story', 'KG Midnight Memories',
#                'KG Primary Italics', 'KG Primary Penmanship Alt', 'KG Primary Penmanship',
#                'KG Primary Penmanship 2', 'Lemon Tuesday', 'Marker Felt',
#                'Microsoft YaHe', 'Noteworthy', 'Palatino', 'Papyrus',
#                 'PT Mono', 'Spot Mono', 'Andale Mono', 'PT Serif', 'PT Serif Caption',
#                 'Rockwell', 'Skia', 'Snell Roundhand',
#                 'Sugar Cream', 'Zapfino',
#                 'Distant_Stroke','Times','Times New Roman',
#                'Broetown Signature','Segoe-Script','KristenITC','Snell Roundhand']

print(len(select_list))

# 设置图片尺寸和字体大小
image_width = 50
image_height = 32
font_size = 40

# 获取系统中已安装的字体列表
installed_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

# 创建空列表存储有效的字体文件
valid_fonts = []

# 遍历已安装的字体列表，筛选出支持所需字符的字体
for font_path in installed_fonts:
    try:
        # print('Loading font', font_path)
        font = ImageFont.truetype(font_path, font_size)
        # print(font.getname())
        # print([char for char in texts[0]])
        # print([font.getsize(char)[0] != 0 for char in texts[0]])
        if all(font.getsize(char)[0] != 0 for char in texts[0]):
            valid_fonts.append(font)
    except Exception as e:
        print(f"Error loading font file: {font_path}")
        print(e)

#打印有效的字体文件列表
#print("Valid fonts:")
# sum=0
# li=[]
# for font_path in installed_fonts:
#
#     # print(font.getname()[0])
#     # print(ImageFont.truetype(font_path, font_size))
#     li.append(ImageFont.truetype(font_path, font_size).getname()[0])

# # for i in li:
# #     print(i)
# li1=[]
# for i in select_list:
#     if i   in li:
#         # sum += 1
#         li1.append(i)
#         print(i)
# # print(li1)
# print(len(set(li1)))
#
# # # 遍历文本列表，为每个文本使用不同的字体生成图片并保存
vfonts1={}
vfonts=[]
for font in valid_fonts:
    if font.getname()[0] in select_list:
            # print(font.getname()[0])
         # print(font.getname()[1],font.getname()[1]=="Regular")
         if font.getname()[0] in vfonts1.keys():
             if font.getname()[1]=="Regular":
                 vfonts1[font.getname()[0]] = font
                # print(font)
                # print(font.getname())

         else:
                vfonts1[font.getname()[0]] = font
vfonts=list(vfonts1.values())
print("brackets",vfonts)
# print(len(vfonts))
# for j in select_list:
#     if j not in [i.getname()[0] for i in vfonts]:
#         print(j)
#
# # print( [i.getname()[0] for i in vfonts])
for idx, text in enumerate(texts):
    # # 遍历有效的字体列表
    # for i in range(3):
    #     #print(i)
    #     font=random.choice(vfonts)
    #print(text)
    for font in vfonts:
        print(font.getname()[0],text)
        if font.getname()[0] in special_and and "&" in text:
            print("warning continue",font.getname()[0],text)
            continue
        if font.getname()[0] in special_dollar and "$" in text:
            print("warning continue",font.getname()[0],text)
            continue
        if font.getname()[0] in special_temperature and "°" in text:
            print("warning continue",font.getname()[0],text)
            continue


            # # 创建一张空白图片
        image = Image.new("RGB", (image_width, image_height), color="white")
        draw = ImageDraw.Draw(image)
            #
            # # 计算文本的大小和位置
        text_width, text_height = draw.textsize(text, font=font)
        text_width0, text_height_0 = draw.textsize(texts[0], font=font)
            # x = (image_width - text_width) / 2
            # y = (image_height - text_height) / 2

            # 如果文本大小超出图片尺寸，则调整图片尺寸
        #if text_width > image_width or text_height > image_height:

        #四周留白增加随机性
        random_x = 0# random.randint(10, 20)
        random_y = 0# random.randint(10, 20)
        image_width = text_width + random_x# max(text_width, image_width)
        if image_width <= 13000:
            image_height = max(text_height_0, image_height) + random_y
            image = Image.new("RGB", (image_width, image_height), color="white")
            draw = ImageDraw.Draw(image)
            x = (image_width - text_width) / 2
            y = (image_height - text_height_0) / 2

            # Draw the text
            draw.text((x, y), text, fill="black", font=font)

            # Add underline
            under_line_hight = max(2, int(image_height / 32))
            underline_y = int(y + 0.83 * text_height_0) # Adjust 2 according to your preference
            draw.line([(x, underline_y), (x + text_width, underline_y)], fill="black", width=under_line_hight)  # Adjust width as needed

            # Save the image
            image_filename = os.path.join(output_dir, f"tiankong_{idx}_{font.getname()[0]}.jpg")
            image.save(image_filename)

            # Print the generated image filename and corresponding text
            print(f"Generated image {image_filename} with text: {text} and font: {font.getname()[0]}")
# import os
# from PIL import Image, ImageDraw, ImageFont
# import matplotlib.font_manager
#
# # 定义用于保存生成图片的输出目录
# output_dir = "generated_images"
# os.makedirs(output_dir, exist_ok=True)
#
# # 定义要生成的文本列表
# texts = [r' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@$%=¥~<>[]|{}°£€']
# #alphabet_encoding_next =  r' !"#&\'()*+,-./0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@$%=¥~<>[]|{}《》°£€'
#
# # 定义要使用的字体列表
select_list = ['Keyboard', 'New York', 'SF Compact Rounded', 'SF NS Mono', 'American Typewriter', 'Andale Mono',
               'Arial Narrow', 'Autography', 'Avenir', 'Baby Doll',
               'Baskerville', 'Bodoni 72', 'Bradley Hand',
               'Celebration', 'Chalkboard SE', 'Chalkboard', 'Chalkduster', 'Charter', 'Comic Sans MS', 'Cochin',
               'Courier New', 'Craftsy', 'DIN Condensed', 'Feltful', 'Futura', 'Georgia',
                'Info Story', 'KG Midnight Memories',
               'KG Primary Italics', 'KG Primary Penmanship Alt', 'KG Primary Penmanship',
               'KG Primary Penmanship 2', 'Le Domaine Auriane', 'Lemon Tuesday', 'Marker Felt',
               'Microsoft YaHe', 'Noteworthy', 'Palatino', 'Papyrus',
                'PT Mono', 'Spot Mono', 'Andale Mono', 'PT Serif', 'PT Serif Caption',
               'Roadly Hezarttest', 'Rockwell', 'Skia', 'Snell Roundhand',
               'Something in the Cloud', 'Sugar Cream', 'Zapfino',
                'Distant_Stroke', 'Miama','Times','Times New Roman',
               'Broetown Signature','Segoe-Script','KristenITC','Snell Roundhand']
#
# print(len(select_list))
#
# # 设置图片尺寸和字体大小
# image_width = 100
# image_height = 64
# font_size = 40
#
# # 获取系统中已安装的字体列表
# installed_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
#
# # 创建空列表存储有效的字体文件
# valid_fonts = []
#
# # 遍历已安装的字体列表，筛选出支持所需字符的字体
# for font_path in installed_fonts:
#     try:
#         font = ImageFont.truetype(font_path, font_size)
#         if all(font.getsize(char)[0] != 0 for char in texts[0]):
#             valid_fonts.append(font)
#     except Exception as e:
#         print(f"Error loading font file: {font_path}")
#         print(e)
#
# # 打印有效的字体文件列表
# print("Valid fonts:")
# for font in valid_fonts:
#     print(font.getname()[0])
#
# # 遍历文本列表，为每个文本使用不同的字体生成图片并保存
# for idx, text in enumerate(texts):
#     # 遍历有效的字体列表
#     for font in valid_fonts:
#         if font.getname()[0] in select_list:
#             # # 创建一张空白图片
#             image = Image.new("RGB", (image_width, image_height), color="white")
#             draw = ImageDraw.Draw(image)
#             #
#             # # 计算文本的大小和位置
#             text_width, text_height = draw.textsize(text, font=font)
#             # x = (image_width - text_width) / 2
#             # y = (image_height - text_height) / 2
#
#             # 如果文本大小超出图片尺寸，则调整图片尺寸
#             #if text_width > image_width or text_height > image_height:
#             image_width = text_width + 20 # max(text_width, image_width)
#             image_height = text_height + 10 #max(text_height, image_height)
#             image = Image.new("RGB", (image_width, image_height), color="white")
#             draw = ImageDraw.Draw(image)
#             x = (image_width - text_width) / 2
#             y = (image_height - text_height) / 2
#
#             # 在图片上绘制文本
#             draw.text((x, y), text, fill="black", font=font)
#
#             # 保存图片为JPEG格式
#             image_filename = os.path.join(output_dir, f"image_{idx}_{font.getname()[0]}.jpg")
#             image.save(image_filename)
#
#             # 打印生成的图片文件名和对应的文本
#             print(f"Generated image {image_filename} with text: {text} and font: {font.getname()[0]}")
# import os
# from PIL import Image, ImageDraw, ImageFont
# import matplotlib.font_manager
#
# exclude_list = ['Arabic','Apple Braille','LastResort',"Bayan","Bodoni Ornaments",'Smallcaps','Hebrew','Damascus',\
#                 'DecoType Naskh','Devanagari MT','Kohinoor','Diwan','Mishafi','Farisi','Geeza',\
#                 'Gujarati','Gurmukhi MT','Herculanum','MT','Devanagari','Kailasa','Kohinoor',\
#                 'Kokonor','KufiStandardGK','Mishafi','Mshtakan','Mukta','Muna','Myanmar','Noto',\
#                 'Tarikh','Nile','Baghdad','Beirut','Farah','Nadeem','Phosphate','Raanana','Sana',\
#                 'STIX','Symbol','Waseem','Webdings','Wingdings','Zapf Dingbats','Copperplate',\
#                 'Billion Dreams','Breathing Personal Use','Romeria Notes PERSONAL USE', "Party LET"]
# exclude1_list = ['Ornaments','Caps']
#
# select_list = ['Keyboard','New York','SF Compact Rounded', 'SF NS Mono','American Typewriter','Andale Mono',\
#                'Apple Chancery','AppleMyungjo','Arial Narrow','Athelas','Audrey Tatum','Autography',\
#                'Automali','Avenir','Baby Doll','Baskerville','Big Caslon','Bodoni 72 Oldstyle','Bodoni 72',\
#                'Bradley Hand','Brittany Signature','Celebration','Chalkboard SE','Chalkboard','Chalkduster',\
#                'Charter','Comic Sans MS','Cochin','Courier New','Craftsy','DIN Alternate','DIN Condensed',\
#                'Feltful','Futura','Georgia','Hello Valentica','Hiragino Sans','Holidays Homework','Info Story',\
#                'KG Midnight Memories','KG Primary Italics','KG Primary Penmanship Alt','KG Primary Penmanship',\
#                'KG Primary Penmanship 2','Le Domaine Auriane','Lemon Tuesday','Luminari','Marker Felt','Microsoft YaHe',\
#                'My Ugly Handwriting','Nickainley','Noteworthy','Palatino','Papyrus','Please write me a song',\
#                'PT Mono','Spot Mono','Andale Mono','PT Serif','PT Serif Caption','Roadly Hezarttest','Rockwell',\
#                'Savoye LET','SignPainter','Skia','Snell Roundhand','Something in the Cloud','Sugar Cream',\
#                'The Students Teacher','Thesignature','Zapfino','alphabetized cassette tapes','James Fajardo',\
#                'Distant_Stroke','Miama','Rolling Beat_Personal Use','Broetown Signature']
# # 创建一个目录用于保存生成的图片
# output_dir = "generated_images"
# os.makedirs(output_dir, exist_ok=True)
#
# # 定义要生成的文本列表
# texts = ["25th, 3,500, 1st, 2nd, xyz, 777"]  # "1st", "2nd", "25", "50s"
#
#
# # 设置图片尺寸和字体大小
# image_width = 1600
# image_height = 128
# font_size = 30
#
# # 获取系统中已安装的字体列表
# installed_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
#
# # 创建空列表存储有效的字体文件
# valid_fonts = []
#
# # 遍历已安装的字体列表，筛选出支持所需字符的字体
# for font_path in installed_fonts:
#     try:
#         font = ImageFont.truetype(font_path, font_size)
#         if all(font.getsize(char)[0] != 0 for char in "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
#             valid_fonts.append(font)
#     except Exception as e:
#         print(f"Error loading font file: {font_path}")
#         print(e)
#
# # 打印有效的字体文件列表
# print("Valid fonts:")
# for font in valid_fonts:
#     print(font.getname()[0])
#
# # 遍历文本列表，为每个文本使用不同的字体生成图片并保存
# for idx, text in enumerate(texts):
#     # 遍历有效的字体列表
#     for int_f, font in enumerate(valid_fonts):
#         # 检查文本是否可以使用当前字体渲染
#         # if all(font.getsize(char) != (0, 0) for char in text) and not any(\
#         #         name in font.getname()[0] for name in exclude_list) and not any(\
#         #         name in font.getname()[1] for name in exclude1_list):
#         if all(font.getsize(char) != (0, 0) for char in text) and \
#                 font.getname()[0] in select_list:
#             # 创建一张空白图片
#             image = Image.new("RGB", (image_width, image_height), color="white")
#             draw = ImageDraw.Draw(image)
#
#             # 计算文本的大小和位置
#             text_width, text_height = draw.textsize(text, font=font)
#             x = (image_width - text_width) / 2
#             y = (image_height - text_height) / 2
#
#             # 在图片上绘制文本
#             draw.text((x, y), text, fill="black", font=font)
#
#             # 保存图片
#             image_filename = os.path.join(output_dir, f"image_{idx}_{font.getname()}.png")
#             image.save(image_filename)
#
#             # 打印生成的图片文件名和对应的文本
#             print(f"Generated image {image_filename} with text: {text} and font: {font.getname()[0]}")
#         #else:
#         #    print(f"Text '{text}' cannot be rendered with any available font.")



# import unicodedata
# import string
# import os
# from PIL import Image, ImageDraw, ImageFont
# import matplotlib.font_manager
#
# # exclude_list = ['Arabic','Apple Braille','LastResort',"Bayan","Bodoni Ornaments",'Smallcaps','Hebrew','Damascus',\
# #                 'DecoType Naskh','Devanagari MT','Kohinoor','Diwan','Mishafi','Fafrah','Farisi','Geeza',\
# #                 'Gujarati','Gurmukhi MT','Herculanum','MT','Devanagari','Kailasa','Kohinoor',\
# #                 'Kokonor','KufiStandardGK','Mishafi','Mshtakan','Mukta','Muna','Myanmar','Noto',\
# #                 ]
# # exclude1_list = ['Ornaments']
# # 创建一个目录用于保存生成的图片
# output_dir = "generated_images"
# os.makedirs(output_dir, exist_ok=True)
#
# # 定义要生成的文本列表
# texts = ["25th"]  # "1st", "2nd", "25", "50s"
#
#
# # 设置图片尺寸和字体大小
# image_width = 200
# image_height = 64
# font_size = 30
#
# # 获取系统中已安装的字体列表
# installed_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
#
# # 创建空列表存储有效的字体文件
# valid_fonts = []
#
# # 遍历已安装的字体列表，筛选出支持所需字符的字体
# for font_path in installed_fonts:
#     try:
#         font = ImageFont.truetype(font_path, font_size)
#         if all(font.getsize(char)[0] != 0 for char in "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
#             valid_fonts.append(font)
#     except Exception as e:
#         print(f"Error loading font file: {font_path}")
#         print(e)
#
# # 打印有效的字体文件列表
# print("Valid fonts:")
# for font in valid_fonts:
#     print(font.getname()[0])
#
# # 存储包含英文字体的字体列表
# english_fonts = []
#
# # 检查每个字体是否包含英文字体
# for font_name in installed_fonts:
#     try:
#         font = ImageFont.truetype(font_name, size=12)
#         # 检查字体是否包含英文字符
#         has_english_chars = all(unicodedata.category(char)[0] == "L" for char in string.ascii_letters)
#
#         if has_english_chars:
#             english_fonts.append(font_name)
#     except Exception as e:
#         print(f"Error loading font: {font_name}")
#         print(e)
#
# # 遍历文本列表，为每个文本使用不同的字体生成图片并保存
# for idx, text in enumerate(texts):
#     # 遍历有效的字体列表
#     for int_f, font in enumerate(english_fonts):
#         # 检查文本是否可以使用当前字体渲染
#         # if all(font.getsize(char) != (0, 0) for char in text) and not any(\
#         #         name in font.getname()[0] for name in exclude_list) and not any(\
#         #         name in font.getname()[1] for name in exclude1_list):
#         if all(font.getsize(char) != (0, 0) for char in text):
#             # 创建一张空白图片
#             image = Image.new("RGB", (image_width, image_height), color="white")
#             draw = ImageDraw.Draw(image)
#
#             # 计算文本的大小和位置
#             text_width, text_height = draw.textsize(text, font=font)
#             x = (image_width - text_width) / 2
#             y = (image_height - text_height) / 2
#
#             # 在图片上绘制文本
#             draw.text((x, y), text, fill="black", font=font)
#
#             # 保存图片
#             image_filename = os.path.join(output_dir, f"image_{idx}_{font.getname()}.png")
#             image.save(image_filename)
#
#             # 打印生成的图片文件名和对应的文本
#             print(f"Generated image {image_filename} with text: {text} and font: {font.getname()[0]}")
#         else:
#             print(f"Text '{text}' cannot be rendered with any available font.")


# import os
# from PIL import Image, ImageDraw, ImageFont
# import string
# import unicodedata
# import matplotlib.font_manager
#
# # 创建一个目录用于保存生成的图片
# output_dir = "generated_images"
# os.makedirs(output_dir, exist_ok=True)
#
# # 定义要生成的文本列表
# texts = ["25th"]  # "1st", "2nd", "25", "50s"
#
# # 设置图片尺寸和字体大小
# image_width = 200
# image_height = 64
# font_size = 30
#
# # 获取系统中已安装的字体列表
# installed_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
#
# # 创建空列表存储有效的字体文件
# valid_fonts = []
#
# # 存储包含英文字体的字体列表
# english_fonts = []
#
# # 遍历已安装的字体列表，筛选出支持所需字符的字体，并存储有效的字体文件和包含英文字体的字体
# for font_path in installed_fonts:
#     try:
#         font = ImageFont.truetype(font_path, font_size)
#         # 检查字体是否包含英文字符
#         has_english_chars = all(unicodedata.category(char)[0] == "L" for char in string.ascii_letters)
#         if has_english_chars:
#             english_fonts.append(font)
#         if all(font.getsize(char)[0] != 0 for char in "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
#             valid_fonts.append(font)
#     except Exception as e:
#         print(f"Error loading font file: {font_path}")
#         print(e)
#
# # 打印有效的字体文件列表
# print("Valid fonts:")
# for font in valid_fonts:
#     print(font.getname()[0])
#
# # 打印包含英文字体的字体列表
# print("English fonts:")
# for font in english_fonts:
#     print(font.getname()[0])
#
# # 遍历文本列表，为每个文本使用不同的字体生成图片并保存
# for idx, text in enumerate(texts):
#     # 遍历有效的字体列表
#     for int_f, font in enumerate(english_fonts):
#         # 检查文本是否可以使用当前字体渲染
#         if all(font.getsize(char) != (0, 0) for char in text):
#             # 创建一张空白图片
#             image = Image.new("RGB", (image_width, image_height), color="white")
#             draw = ImageDraw.Draw(image)
#
#             # 计算文本的大小和位置
#             text_width, text_height = draw.textsize(text, font=font)
#             x = (image_width - text_width) / 2
#             y = (image_height - text_height) / 2
#
#             # 在图片上绘制文本
#             draw.text((x, y), text, fill="black", font=font)
#
#             # 保存图片
#             image_filename = os.path.join(output_dir, f"image_{idx}_{font.getname()}.png")
#             image.save(image_filename)
#
#             # 打印生成的图片文件名和对应的文本
#             print(f"Generated image {image_filename} with text: {text} and font: {font.getname()[0]}")
#         else:
#             print(f"Text '{text}' cannot be rendered with any available font.")
