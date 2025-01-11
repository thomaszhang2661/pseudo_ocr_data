import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from tqdm import tqdm
# 设置输出根文件夹
output_root_folder = "../../AI_output_images"
if not os.path.exists(output_root_folder):
    os.makedirs(output_root_folder)

# 读取常用汉字列表
def load_common_chinese_characters(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

# 定义字体文件路径
font_paths = "./AI生成汉字/AI_font/"
print("字体文件夹路径:", font_paths)
print("当前工作目录:", os.getcwd())
# 字体文件所在目录
font_list = os.listdir(font_paths)
font_path_list = []
for font in font_list:
    font_path_list.append(os.path.join(font_paths, font))

# 字体大小
font_size = 50
image_size = (200, 200)  # 图片的尺寸

def crop_off_whitespace(image, margin=2,threshold=200):
    # 转换为NumPy数组
    # 将图像转换为灰度
    h,w = image.shape
    #random.randint(0,4)
    image_array = np.array(image)

    # 计算每一行和每一列的灰度值之和
    horizontal_sum = np.sum(image_array < threshold, axis=1)
    vertical_sum = np.sum(image_array < threshold, axis=0)

    # 找到上边界和下边界
    top = np.argmax(horizontal_sum > 0)
    bottom = len(horizontal_sum) - np.argmax(horizontal_sum[::-1] > 0)

    # 找到左边界和右边界
    left = np.argmax(vertical_sum > 0)
    right = len(vertical_sum) - np.argmax(vertical_sum[::-1] > 0)

    # 裁剪图像
    #cropped_image = image.crop((left, top, right, bottom))
    #cropped_image = image[top:bottom, left:right]
    cropped_image = image[max(0, top - margin): min(bottom + margin, h),
                          max(0, left - margin): min(right + margin, w)]

    return cropped_image

# 为每个汉字生成灰度图片
def generate_images_for_char(character, output_folder, font_paths):
    for font_path in font_paths:
        #try:
            # 加载字体
            font = ImageFont.truetype(font_path, font_size)

            # 创建一张白色背景的灰度图片（模式 'L' 表示灰度图）
            img = Image.new("L", image_size, color=255)  # 使用灰度模式
            draw = ImageDraw.Draw(img)

            # 计算文字的宽高，确保文字居中
            text_width, text_height = draw.textsize(character, font=font)
            text_x = (img.width - text_width) / 2
            text_y = (img.height - text_height) / 2

            # 在图片上绘制汉字（填充颜色为黑色）
            draw.text((text_x, text_y), character, font=font, fill=0)  # 0表示黑色，255表示白色
            img = np.array(img)
            img = crop_off_whitespace(img)
            img = Image.fromarray(img)
            # 构建字体对应的文件名
            font_name = os.path.basename(font_path).split('.')[0]  # 获取字体文件名（去除扩展名）
            output_image_path = os.path.join(output_folder, f"{font_name}_{character}.png")

            # 保存图片
            img.save(output_image_path)
            print(f"已保存：{output_image_path}")
        # except Exception as e:
        #     print(f"处理字体 {font_path} 时出错：{e}")

# 主函数，加载汉字并为每个字生成图片
def main():
    # 从文本文件中加载常用汉字列表
    characters = load_common_chinese_characters("./AI生成汉字/3500常用汉字.txt")

    for char in tqdm(characters,total=3500):
        # 创建每个汉字的文件夹
        char_folder = os.path.join(output_root_folder, char)
        if not os.path.exists(char_folder):
            os.makedirs(char_folder)

        # 为每个汉字生成图片
        generate_images_for_char(char, char_folder, font_path_list)

if __name__ == "__main__":
    main()
