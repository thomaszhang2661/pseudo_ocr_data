# 作者：张健 Thomas Zhang
# 时间：2024/7/4,23:32

import os
import cv2
import numpy as np
import tqdm


border_size = 2
margin = 10


def add_frame_and_background(image_path, border_size=2, margin=10):
    # 读取灰度图像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 找到图像中的最小和最大像素值
    min_pixel_value = int(np.percentile(image, 5))
    max_pixel_value = int(np.percentile(image, 70))

    # 添加黑色边框
    bordered_image = cv2.copyMakeBorder(image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=min_pixel_value)

    # # 获取图像的高度和宽度（包括边框）
    # height, width = bordered_image.shape
    #
    # # 创建更大的背景图像，并将原始图像放置在中心位置
    # larger_width = width + 2 * border_size + 2 * margin
    # larger_height = height + 2 * border_size + 2 * margin
    # larger_image = np.ones((larger_height, larger_width), dtype=np.uint8) * max_pixel_value
    # larger_image[margin + border_size:margin + border_size + height, margin + border_size:margin + border_size + width] = bordered_image
    #
    # # 保存原始图像的中心位置作为背景颜色
    # background_color = larger_image[0, 0]
    #
    # # 生成背景图像，将背景颜色填充到外部
    # background_image = np.ones((larger_height + 2 * margin, larger_width + 2 * margin), dtype=np.uint8) * background_color
    # background_image[margin:margin + larger_height, margin:margin + larger_width] = larger_image

    # 获取图像的高度和宽度（包括边框）
    height, width = bordered_image.shape

    # 创建更大的背景图像，并将原始图像放置在中心位置
    larger_width = width + 2 * border_size + 2 * margin
    larger_height = height + 2 * border_size + 2 * margin
    larger_image = np.ones((larger_height, larger_width), dtype=np.uint8) * max_pixel_value
    # 添加高斯噪声到背景部分
    noise = np.zeros_like(larger_image, dtype=np.uint8)
    cv2.randn(noise, 0, 15)  # 生成高斯噪声，标准差为 15
    noisy_background = cv2.add(larger_image, noise, dtype=cv2.CV_8U)
    noisy_background = cv2.GaussianBlur(noisy_background, (5, 5), 0)

    noisy_background[margin + border_size:margin + border_size + height, margin + border_size:margin + border_size + width] = bordered_image



    return noisy_background
if __name__ == '__main__':
    # 定义要遍历的文件夹路径
    folder_path = './xuehao/data_train/'
    output_path = './xuehao/framed_xuehao/'
# 获取文件夹中的所有文件列表
files = os.listdir(folder_path)

# 遍历文件列表，找出所有的 JPG 文件
for file in tqdm.tqdm(files):
    # 检查文件名是否以 .jpg 结尾（忽略大小写）
    if file.lower().endswith('.jpg'):
        # 拼接完整的文件路径
        file_path = os.path.join(folder_path, file)
        # 处理文件，例如打印文件路径
        bordered_image = add_frame_and_background(file_path)
        cv2.imwrite(output_path+file,bordered_image)
