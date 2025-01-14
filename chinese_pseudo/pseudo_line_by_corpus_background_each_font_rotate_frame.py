

"""
作者：张健
时间：2024.10.20
这个模块制造伪的行数据，基于单个中文字，随机添加删除符号
"""

from PIL import Image, ImageFilter
import random
import time
import os
from tqdm import tqdm
from gen_scratch import apply_scratches
from image_operation import *
from mapping_punct import chinesepun2englishpun
import json
from itertools import cycle, islice
import math

#PREVIOUS_FONT_INDEX = 720
PREVIOUS_FONT_INDEX = 830

# 上部标点
upper_punct = [
    '"', "'", "‘", "’", '“', '”', '`', '^']

# 下部标点
lower_punct = [
    '.', ',', '。', '、', '…'
]

middle_punct = ["-", "~", "<", ">", "[", "]", "(", ")", "{", "}"]

letter_A = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
letter_baseline = ['a', 'c', 'e', 'i', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'z']  # 基线字母
letter_ascender = ['b', 'd', 'h', 'k', 'l', 't', 'f']  # 上升部件字母
letter_descender = ['g', 'p', 'q', 'y', 'j']  # 下降部件字母

# 获取当前工作目录
current_working_directory = os.getcwd()

print("当前工作路径是:", current_working_directory)






def load_background_images(background_directory):
    """加载所有底图图像并转换为灰度图像"""
    background_images = []
    files = os.listdir(background_directory)
    for filename in files:
        if filename.endswith('.jpg') or filename.endswith('.png'):
            filepath = os.path.join(background_directory, filename)
            try:
                # 打开图像并转换为灰度图像
                gray_image = Image.open(filepath).convert('L')
                background_images.append(gray_image)
            except Exception as e:
                print(f"Error loading background image {filepath}: {e}")
    return background_images




def add_background_to_image(gray_image, background_image, threshold=100):
    # 将灰度图像转换为 numpy 数组
    image_array = np.array(gray_image)

    # 获取前景图像的尺寸
    image_width, image_height = gray_image.size
    background_width, background_height = background_image.size

    # 如果背景图像的尺寸小于前景图像的尺寸，则调整背景图像的尺寸
    if background_width < image_width or background_height < image_height:
        # Resize the background image to at least match the size of the gray image
        background_image = background_image.resize((image_width, image_height), Image.Resampling.LANCZOS)
        background_array = np.array(background_image)
    elif background_height != image_height:
        background_image = background_image.resize((background_width, image_height), Image.Resampling.LANCZOS)
        background_array = np.array(background_image)
    else:
        # 如果背景图像比前景图像大，保持背景图像尺寸，前景图像粘贴在背景的左上角
        background_array = np.array(background_image)

    # 创建一个背景图像副本
    final_image_array = np.copy(background_array)

    # 将前景图像的灰度值小于阈值的部分覆盖到背景图像上
    final_image_array[:image_height, :image_width][image_array < threshold] = image_array[image_array < threshold]

    # 将合成后的图像数组转换回 PIL 图像
    final_image = Image.fromarray(final_image_array)

    return final_image




punct_dict = {}
with open('./标点符号.txt', 'r', encoding='utf-8') as f:
    for line in f:
        char, code = line.strip().split(' : ')  # 按制表符分割
        punct_dict[char] = int(code)  # 将编码转换为整数



zidonghua_dict = {}
zidonghua_dict_reverse = {}
with open('merged_dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        char, code = line.strip().split(' : ')  # 按制表符分割
        zidonghua_dict[char] = int(code)  # 将编码转换为整数
        zidonghua_dict_reverse[int(code)] = char
zidonghua_list = list(zidonghua_dict.keys())


lenth_original = len(zidonghua_dict)


# print("corpus exam finished")

# 定义伽马校正函数
def adjust_gamma(image, gamma=1.0):
    # 构建查找表来加快伽马校正的速度

    image = Image.fromarray(image)

    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype("uint8")

    # 将图像转换为灰度模式（如果图像为 RGB 模式）
    if image.mode != 'L':
        image = image.convert('L')

    # 应用查找表进行伽马校正
    image = image.point(table)

    return np.array(image)



def adjust_text_brightness(image, lower=30):
    """调整图像的亮度，使字体颜色变淡"""
    # 转为 numpy 数组
    image_array = np.array(image)
    # 调整亮度
    image_array = np.clip(image_array, lower, 255)
    return Image.fromarray(image_array)

def crop_off_whitespace(image,direction="all"):
    # 转换为NumPy数组
    # 将图像转换为灰度
    gray_image = image.convert('L')
    w,h = gray_image.size
    image_array = np.array(gray_image)
    threshold = 100
    # 计算每一行和每一列的灰度值之和
    horizontal_sum = np.sum(image_array < threshold, axis=1)
    vertical_sum = np.sum(image_array < threshold, axis=0)

    if direction == "all":
        # 找到上边界和下边界
        top = np.argmax(horizontal_sum > 0)  - random.randint(0, 5)
        bottom = len(horizontal_sum) - np.argmax(horizontal_sum[::-1] > 0) + random.randint(0, 5)

        # 找到左边界和右边界
        left = np.argmax(vertical_sum > 0)  - random.randint(0, 5)
        right = len(vertical_sum) - np.argmax(vertical_sum[::-1] > 0) + random.randint(0, 5)
    elif direction == "x":
        # 找到左边界和右边界
        left = np.argmax(vertical_sum > 0) - random.randint(0, 5)
        right = len(vertical_sum) - np.argmax(vertical_sum[::-1] > 0) + random.randint(0, 5)
        top = 0
        bottom = h
    elif direction == "y":
        # 找到上边界和下边界
        top = np.argmax(horizontal_sum > 0) - random.randint(0, 5)
        bottom = len(horizontal_sum) - np.argmax(horizontal_sum[::-1] > 0) + random.randint(0, 5)
        left = 0
        right = w


    # # 找到上边界和下边界
    # top = np.argmax(horizontal_sum > 0)
    # bottom = len(horizontal_sum) - np.argmax(horizontal_sum[::-1] > 0)
    #
    # # 找到左边界和右边界
    # left = np.argmax(vertical_sum > 0)
    # right = len(vertical_sum) - np.argmax(vertical_sum[::-1] > 0)

    # 裁剪图像
    cropped_image = image.crop((max(left,0), max(0,top), min(right,w), min(bottom,h)))
    return cropped_image

def load_local_images(image_directory):
    """这个函数根据单子数据添加到一个字典结构中"""
    mnist_data = {}
    font_style = []
    #files = sorted(os.listdir(image_directory))
    files = os.listdir(image_directory)
    filenames = [f for f in files if f.endswith('.jpg')]
    for filename in tqdm(filenames, desc="加载图像"):
        font_name, label = filename.split('_', 1)
        label = label.split('.')[0]
        if font_name not in font_style:
            font_style.append(font_name)
        filepath = os.path.join(image_directory, filename)
        image = Image.open(filepath).convert('L')  # 转为灰度图
        # if label not in mnist_data:
        #     mnist_data[label] = []
        # mnist_data[label].append(np.array(image))
        # 初始化字典结构
        if label not in mnist_data:
            mnist_data[label] = {}

        # 将图像数据存入相应的标签和字体名下
        mnist_data[label][font_name] = np.array(image)
        #font_style = list(set(font_style))
    return font_style, mnist_data




def load_local_images_pub(image_directory,num_font,num_font_off_set,font_list):
    '''加载自动化所的单个手写字体'''
    zidonghua_data = {}

    # 获取所有子文件夹的列表
    # sub_files_list = [sub_files for sub_files in os.listdir(image_directory)
    #                   if len(sub_files) == 5 and sub_files.isdigit()]

    if os.path.exists(image_directory):
        sub_files_list = [sub_files for sub_files in os.listdir(image_directory)]
    else:
        print(f"Directory {image_directory} not found.")
    # 遍历所有有效子文件夹
    for sub_files in tqdm(sub_files_list, desc="加载图像"):
        # 获取对应的字符
        word = zidonghua_dict_reverse.get(int(sub_files[:-4]), None)
        if word is None:  # 如果字典中没有对应的字符，跳过
            continue

        folder_path = os.path.join(image_directory, sub_files)

        # 获取该文件夹中所有文件名
        files = os.listdir(folder_path)
        #files = [entry.name for entry in os.scandir(folder_path) if entry.is_file()]
        
        
        # sorted_files = sorted(files, key=lambda x: x.split('.')[0])
        # if len(sorted_files) < num_font_off_set + num_font:
        #     sorted_files = list(islice(cycle(sorted_files), num_font_off_set + num_font))
                
        # files = sorted_files[num_font_off_set:num_font_off_set+num_font]
        
        
        #print(len(files),'len_sorted_files')
        # 初始化当前字符的图像数据列表
        zidonghua_data[word] = []

        font_list_wanted = font_list[num_font_off_set:num_font_off_set+num_font]
        # 直接打开图像并转换为灰度图像，批量加载
        # for filename in files:
            
        #     if filename.split('_')[0] not in font_list_wanted:
        #         continue
        
        # 按照 font_list 顺序加载图像
        for font in font_list_wanted:
            for filename in files:
                if font in filename:
                    filepath = os.path.join(folder_path, filename)
                    try:
                        # 加载图像并转换为灰度模式
                        image_data = Image.open(filepath).convert('L')
                        zidonghua_data[word].append(np.array(image_data))  # 存储图像数据
                    except Exception as e:
                        print(f"Error loading image {filepath}: {e}")
                    break
            else:
                zidonghua_data[word].append(None)

    zidonghua_data[" "] = [np.ones((70, 70)) * 255]  # 空格
    return zidonghua_data

def add_border(image, border_width=3, border_color=0, width_goal=70):
    """
    为图片添加边框

    :param image: 输入的PIL.Image图像
    :param border_width: 边框的宽度
    :param border_color: 边框的颜色 (默认为黑色: 0)
    :return: 带有边框的图像
    """
    width, height = image.size
    leave_blank = random.randint(1, 5)
    new_image = Image.new("L", (width + 2 * (border_width + leave_blank) , height + 2 * (border_width + leave_blank)), 255)
    new_image.paste(image, (border_width, border_width))

    draw = ImageDraw.Draw(new_image)
    draw.rectangle(
        [(border_width, border_width), (width + border_width - 1, height + border_width - 1)],
        outline=border_color,
        width=border_width,
    )
    # 添加竖线
    range_x = math.ceil(width/width_goal)
    for x in range(1, range_x):
        draw.line([(x*width_goal + border_width, border_width), (x*width_goal + border_width, height + border_width)],
                  fill=border_color, width=border_width)
    
    return new_image

def create_handwritten_number_image_pub_by_corpus(index_font, index_line, line_chars, output_path, zidonghua_data,
                                                  background_images=[],mnist_data=[]):
    '''根据自动化所的手写图像生成伪数据'''

    list_of_text = list(line_chars)

    width_goal = 70
    height_goal = 70
    off_set_max = 10

    # 整幅图片
    image = Image.new('L', (int((width_goal + off_set_max)*len(line_chars) * 1.5), int(height_goal * 1.5)), 255)
    


    #gamma_value = 0.4  # 可以调整此值，0.5效果通常较为明显
    # 随机选择一次所有字符的图像
    selected_images = []
    for i_c, char in enumerate(line_chars):
        # if char not in zidonghua_data:
        #     list_of_text[i_c] = " "
        #     # 添加空白图片
        #     selected_images.append(zidonghua_data[" "][0])
        #     #print("warning not in dict", char, line_chars)
        #     continue
        if char in zidonghua_data:
            char_images = zidonghua_data[char]
            #random_indices = random.randint(0, len(char_images) - 1)
            # index_font = index_font % len(char_images)
            try:
                if char == " ":
                    selected_image = char_images[0]
                elif char_images[index_font] is None or len(char_images[index_font]) == 0:
                    list_of_text[i_c] = " "
                    selected_image = np.ones((height_goal, width_goal)) * 255
                else:
                    selected_image = char_images[index_font]
            except IndexError as e:
                print(f"Error: {e}. Length of char_images: {len(char_images)}, index_font: {index_font}")

            # 调整伽马值，尝试低于1.0的值来增加黑色区域的深度
            #selected_image = adjust_gamma(selected_image, gamma=gamma_value)
            selected_images.append(selected_image)
        # elif char in mnist_data:
        #     char_images = mnist_data[char]
        #     selected_image = char_images.get(random.choice(font_style),
        #                                          char_images.get(random.choice(list(char_images.keys()))))
        #
        #     selected_images.append(selected_image)

        else:
            #raise
            #selected_images.append(np.zeros((height, width)))  # 如果找不到，填充空白图像
            #selected_images.append(np.ones((height_goal, int(width_goal/2))) * 255)  # 如果找不到，填充白色图
            
            #========================
            # if char != " ":
            #     print("未找到字符", char)
            list_of_text[i_c] = " "
            selected_images.append(zidonghua_data[" "][0])
    # 粘贴图像
    # 粘贴图像
    off_set_position = 0
    # 加入多样性？
    random_flag = True
    if random.choice(range(1)) == 0:
        random_flag = True
    for i, single_image in enumerate(selected_images):
        single_image = Image.fromarray(single_image)

        # 归一化文字部分的大小
        single_image = crop_off_whitespace(single_image)
        cur_width, cur_height = single_image.size
        # 如果图片不存在，则用空白图片代替
        if cur_width <=0 or cur_height <=0:
            list_of_text[i] = " "
            single_image = Image.fromarray(np.ones((height_goal,
                                                    random.randint(int(width_goal * 0.3),int(width_goal)))) * 255)
            
            
        ratio = min(width_goal / cur_width, height_goal / cur_height)

        if list_of_text[i] not in punct_dict:
            if random.choice(range(2)) == 0:
            #single_image = single_image.resize((int(cur_width*ratio), int(cur_height*ratio)), Image.ANTIALIAS)
                single_image = single_image.resize((int(cur_width*ratio), int(cur_height*ratio)), Image.Resampling.LANCZOS)

        elif ratio < 1:
            single_image = single_image.resize((int(cur_width*ratio * 0.9), int(cur_height*ratio * 0.9)), Image.Resampling.LANCZOS)



        # 透视变换
        if random_flag :#and random.choice(range(2)) == 0:
            single_image = apply_perspective_transform(single_image)
        # 应用旋转变换
        #  # 旋转角度，可以调整
        if random_flag :#and random.choice(range(2)) == 0:
            angle_ratio = random.uniform(-1.0, 1.0)
            angle = 10 * angle_ratio
            single_image = rotate_text_image(single_image, angle)

        single_image = crop_off_whitespace(single_image)
        # 归一化大小
        if list_of_text[i] not in punct_dict:
            cur_width, cur_height = single_image.size
            #if cur_height > height_goal or cur_width > width_goal:
            # single_image = cv2.resize(single_image, (width_goal, height_goal), interpolation=cv2.INTER_LINEAR)
            ratio = min(width_goal / cur_width, height_goal / cur_height)
            #single_image = single_image.resize((int(cur_width * ratio), int(cur_height * ratio)), Image.ANTIALIAS)
            single_image = single_image.resize((int(cur_width * ratio), int(cur_height * ratio)),
            Image.Resampling.LANCZOS)
        # 如果是英文字母或者数字，需要调整大小
        else:
            cur_width, cur_height = single_image.size
            ratio = min(width_goal / cur_width, height_goal / cur_height)
            ratio = min(ratio,2)
            ratio = random.uniform(1, ratio)
            single_image = single_image.resize((int(cur_width * ratio), int(cur_height * ratio)),
            Image.Resampling.LANCZOS)
            
        if list_of_text[i] == " ":
            single_image = Image.fromarray(np.ones((height_goal,
                                                    random.randint(int(width_goal * 0.3),int(width_goal)))) * 255)


        # 调整大小
        single_width, single_height = single_image.size
        scale_ratio = random.uniform(0.9, 1.0)
        scaled_w = max(int(single_width * scale_ratio), 1)
        scaled_h = max(int(single_height * scale_ratio), 1)
        
        #single_image = single_image.resize((scaled_w, scaled_h), Image.ANTIALIAS)
        single_image = single_image.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)

        # 加入划痕
        if list_of_text[i] not in punct_dict and list_of_text[i] != " " and random.choice(range(100)) == 0:
            single_image = crop_off_whitespace(single_image)
            single_image = apply_scratches(single_image)
            list_of_text[i] = '\\'

        # 切边
        single_image = crop_off_whitespace(single_image)

        # 此处可加入随机性
        single_width, single_height = single_image.size
        #offset_x = random.randint(0, min(off_set_max, int(single_width)))
        offset_x = 0
        #
        ##else:
        #    offset_x = single_width - cell_width

        #offset_y = random.randint(0, height_goal - single_height)
        # 适当调整位置
        if list_of_text[i] not in punct_dict:
            offset_y = random.randint(max(int(0.5 * height_goal - single_height), 0),
                                      min(int(0.5 * height_goal), height_goal - single_height))
        elif list_of_text[i] in upper_punct:
            offset_y = random.randint(0, int(0.1 * height_goal))
        elif list_of_text[i] in lower_punct:
            offset_y = random.randint(min(int(0.7 * height_goal), height_goal - single_height),
                                      height_goal - single_height)
        elif list_of_text[i] in middle_punct:
            offset_y = random.randint(int(0.5 * height_goal - single_height * 0.5 - 0.1 * single_height),
                                      int(0.5 * height_goal - single_height * 0.5 + 0.1 * single_height))

        elif list_of_text[i] in letter_A:
            offset_y = random.randint(height_goal - single_height - int(0.1 * single_height),
                                      height_goal - single_height)

        elif list_of_text[i] in letter_baseline:
            offset_y = random.randint(height_goal - single_height - int(0.1 * single_height),
                                      height_goal - single_height)
        elif list_of_text[i] in letter_ascender:
            offset_y = random.randint(height_goal - single_height - int(0.1 * single_height),
                                      height_goal - single_height)

        elif list_of_text[i] in letter_descender:
            # offset_y = random.randint(int(height_goal - single_height * 0.5 - 0.05 * single_height),
            #                           int(height_goal - single_height * 0.5))
            offset_y = random.randint(height_goal - single_height - int(0.1 * single_height),
                                      int(height_goal - single_height * 0.5))

        elif list_of_text[i] in punct_dict:
            # offset_y = random.randint(height_goal - single_height - int(0.1 * height_goal),
            #                           height_goal - single_height)
            offset_y = random.randint(int(0.5 * height_goal - single_height * 0.5 - 0.1 * single_height),
                                      int(0.5 * height_goal - single_height * 0.5 + 0.1 * single_height))
        else:
            offset_y = random.randint(int(height_goal * 0.5 - single_height * 0.5 - 0.1 * single_height),
                                      int(height_goal * 0.5 - single_height * 0.5 + 0.1 * single_height))


        # 这个地方需要对标点符号特殊处理。


        # paste_position = (i * cell_width + offset_x, offset_y)
        paste_position = (off_set_position + offset_x, offset_y)
        #off_set_position += offset_x + single_width
        off_set_position += offset_x + width_goal
        
        image.paste(single_image, paste_position)

    # 切左右
    image = crop_off_whitespace(image, direction='x')
    width, height = image.size
    # draw = ImageDraw.Draw(image)
    # if random.choice(range(3)) != 0:
    #     underline_y1 = height_goal - random.randint(0, 10)  # 下划线的位置
    #     underline_y2 = height_goal - random.randint(0, 10)  # 下划线的位置

    #     draw.line([(0, underline_y1), (width, underline_y2)], fill=0, width=random.randint(3,5))

    # # 切边
    # image = crop_off_whitespace(image)
    # width, height = image.size



    #random_lower = random.randint(0, 60)
    #larger_image = adjust_text_brightness(larger_image, lower=random_lower)
    image = crop_off_whitespace(image)
    
    #===================
    #添加frame or 下划线
    width, height = image.size
    draw = ImageDraw.Draw(image)
        
    # 找到 final_image 颜色 25%的位置
    # 将图像转换为灰度图像（如果需要，可以选择其他颜色空间）
    image_gray = image.convert("L")  # 转换为灰度图像
    # 将灰度图像转为 numpy 数组
    image_array = np.array(image_gray)
    # 计算图像的 25% 像素值
    #color_10 = final_image_array.min() #int(np.percentile(final_image_array, 1))
    color_under_line = int(max(0, min(255, image_array.min() + random.randint(-10, 10))))  # 加上一个随机偏移
    
    frame_choice = 1#random.choice(range(3))

    if frame_choice == 0:
        underline_y1 = height - random.randint(0, 10)  # 下划线的位置        
        draw.line([(0, underline_y1), (width, underline_y1)]
                  , fill=color_under_line, width=random.randint(1,4))
        
    elif frame_choice == 1:
        # 加入边框
        image = add_border(image, border_width=random.randint(2, 4), border_color=color_under_line, 
                           width_goal=width_goal)
    

    w_l, h_l = image.size
    if h_l > 64:
        ratio = 64 / h_l
        image = image.resize((int(w_l*ratio), int(h_l*ratio)), Image.Resampling.LANCZOS)
    larger_image = image
    # 对图片随机旋转角度
    angle = random.randint(-2, 2)
    larger_image = larger_image.rotate(angle, expand=True, fillcolor=255)
    background = random.choice(background_images)
    

    #将背景图resize到目标大小
    # 处理宽度 这里面考虑填空题右侧留空的情况统一向右扩展 像素200-550宽度
    width_blank = random.randint(200, 550)
    final_width = int(max(width_blank, larger_image.size[0] + random.randint(50,200)))
    # # print('final_width',final_width)
    # # print(' background.size[0]',background.size[1])
    # if background.size[0] < final_width:
    #     background = background.resize((final_width, background.size[1]),  Image.Resampling.LANCZOS)
    # # 处理高度
    # elif background.size[1] < larger_image.size[1]:
    #     background = background.resize((background.size[0], larger_image.size[1]), Image.Resampling.LANCZOS)
    # else:
    #     # 截取需要的部分背景图片 随机截取
    #     #background = background.crop((0, 0, larger_image.size[0], larger_image.size[1]))
    #     x_start = random.randint(0, background.size[0] - final_width)
    #     y_start = random.randint(0, background.size[1] - larger_image.size[1])
    #     background = background.crop((x_start,
    #                                   y_start,
    #                                   x_start + final_width,
    #                                   y_start + larger_image.size[1]))
    
    def resize_background(background, final_width, final_height):
        if background.size[0] < final_width:
            background = background.resize((final_width, background.size[1]), Image.Resampling.LANCZOS)
        if background.size[1] < final_height:
            background = background.resize((background.size[0], final_height), Image.Resampling.LANCZOS)
        return background

    def crop_background(background, final_width, final_height):
        x_start = random.randint(0, max(0, background.size[0] - final_width))
        y_start = random.randint(0, max(0, background.size[1] - final_height))
        return background.crop((x_start, y_start, x_start + final_width, y_start + final_height))

    # 使用封装后的函数
    background = resize_background(background, final_width, larger_image.size[1])
    background = crop_background(background, final_width, larger_image.size[1])

    final_image = add_background_to_image(larger_image, background)
    final_image = crop_off_whitespace(final_image,direction="y")

    if debug:
        #保存图片debug
        output_sub = os.path.join(output_path,str(i_font+num_font_off_set+PREVIOUS_FONT_INDEX))
        os.makedirs(output_sub, exist_ok=True)
        #print(output_sub)
        output_file = os.path.join(output_sub, f'0000_{i_font+num_font_off_set+PREVIOUS_FONT_INDEX}_{index_line}_background.jpg')
        #output_file = os.path.join(output_sub, f'0000_background.jpg')

        #print(output_file)
        final_image.save(output_file)
    



    # 切边
    #final_image = crop_off_whitespace(final_image)
    width, height = final_image.size
    #===================
    random_lower = random.randint(0, 60)
    final_image = adjust_text_brightness(final_image, lower=random_lower)
    # 这里可以调整radius来控制模糊程度
    final_image = final_image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0, 0.8))) 

    
    # 添加边距
    # min_margin = int(0.04 * height)
    # max_margin = int(0.08 * height)
    # left_margin = random.randint(min_margin, max_margin)
    # right_margin = random.randint(min_margin, max_margin)
    # top_margin = random.randint(min_margin, max_margin)
    # bottom_margin = random.randint(min_margin, max_margin)
    # larger_width = width + left_margin + right_margin
    # larger_height = height + top_margin + bottom_margin
    # larger_image = Image.new('L', (larger_width, larger_height), 255)
    # larger_image.paste(final_image, (left_margin, top_margin))
    
    larger_image = final_image
    # 保存图像

    timestamp = int(time.time())
    text_new = "".join(list_of_text)

    output_sub = os.path.join(output_path,str(i_font+num_font_off_set+PREVIOUS_FONT_INDEX))
    os.makedirs(output_sub, exist_ok=True)
    #print(output_sub)
    output_file = os.path.join(output_sub, f'{timestamp}_{i_font+num_font_off_set+PREVIOUS_FONT_INDEX}_{index_line}.jpg')

    try:
        # 如果标注内容为空，不保存
        if text_new.strip() == "":
            return
        larger_image.save(output_file)
        label_content[f'{timestamp}_{i_font+num_font_off_set+PREVIOUS_FONT_INDEX}_{index_line}'] = text_new

    except Exception as e:
        print(f"Error saving image {output_file}: {e}")
    
    # label_path = os.path.join(output_sub, 'labels')
    # os.makedirs(label_path, exist_ok=True)
    # label_file_name = os.path.join(label_path, f"{timestamp}_{i_font+num_font_off_set}_{index_line}.txt")

    # with open(label_file_name,'w',encoding='utf-8') as f:
    #     f.write(text_new)



if __name__ == '__main__':
    random.seed(40)
    # 总共235 字体
    # 总共104 字体
    num_font = 5 #字体数量
    num_font_off_set = 0
    debug = False
    user_font_dir = "/database/selected_hw_1"
    #获取字体名称列表
    font_style_list = []
    for root, dirs, files in os.walk(user_font_dir):
        for file in files:
            font_style_list.append(file.split(".")[0])
    print(font_style_list)
    print(len(font_style_list))
    #image_directory = './single_font/pseudo_chinese_images_1111_checked'
    #image_font_directory = '../../pseudo_chinese_images_1111_checked/'
    #image_font_directory = '../../pseudo_chinese_images_1111_checked/'
    #image_pub_directory = './chinese_data1018/pic_chinese_char'
    #image_pub_directory = '../../gnt_all/'.replace('/', os.sep)
    
    image_pub_directory = '/database/single_font_250102_new/'.replace('/', os.sep)
    #image_pub_directory = '/database/single_font_1222/'.replace('/', os.sep)

    #image_pub_directory = r"C:\Users\ThomasZhang\PycharmProjects\pseudo_chinese_images_250101".replace("\\","/")
    
    #output_path = './Chinese-app-digital/data/data_train/'
    #output_path = f'./psudo_chinese_data/gen_line_print_data_1110/'
    #output_path = '../../psudo_chinese_data/gen_line_data_1210_delta/'.replace('/', os.sep)
    output_path = '/database/gen_line_data_250112_font_frame/'.replace('/', os.sep)
    #output_path = '/database/gen_line_data_250112_font_old/'.replace('/', os.sep)

    #output_path = r"C:\Users\ThomasZhang\PycharmProjects\gen_line_data_250101_font_new".replace("\\", "/")

    # 加载底图
    #background_directory = r"C:\Users\ThomasZhang\PycharmProjects\background".replace("\\", "/")  # 底图文件夹路径
    background_directory ="./background/"
    background_images = load_background_images(background_directory)

    #label_path = f'{output_path}labels/'.replace('/', os.sep)
    if not os.path.exists(output_path):
        os.makedirs(output_path,exist_ok=True)
    #if not os.path.exists(label_path):
    #    os.makedirs(label_path),,exist_ok=True
    random_font = True
    random_seq = True

    # 加载单个汉字图片
    zidonghua_data = load_local_images_pub(image_pub_directory,num_font,num_font_off_set,font_style_list)
    
    #读取corpus #'all_chinese_dicts_standard.txt','all_english_dicts_standard.txt','xdhy_corpus2_standard.txt','xdhy_corpus_book.txt','xdhy_corpus_book.txt'
    corpus_list = ['all_corpus_standard.txt']
    corpus_path = './corpus/'
    corpus_content = []
    
    for file in corpus_list:
        print(file)
        path_corpus = os.path.join(corpus_path, file)
        with open(path_corpus, 'r', encoding='utf-8') as f:
            for line in f:
                translation = chinesepun2englishpun(line.strip())
                corpus_content.append(translation)
    print("corpus exam finished")

    # 遍历字体，每种字体生成一套数据，后面不够的轮回前面的字体 num_font
    for i_font in tqdm(range(num_font), total=num_font):
        label_content = {}
        for index_line, line in enumerate(corpus_content):
            create_handwritten_number_image_pub_by_corpus(i_font, index_line, line,
                                                          output_path, zidonghua_data, background_images)
        # 输出labels
        output_sub = os.path.join(output_path,str(i_font+num_font_off_set+PREVIOUS_FONT_INDEX))
        os.makedirs(output_sub, exist_ok=True)
        print(output_sub)
        label_file = os.path.join(output_sub,'label.json')
        with open(label_file, 'w', encoding='utf-8') as f:
            json.dump(label_content, f, ensure_ascii=False, indent=4)
    # 保存标签






