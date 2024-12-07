import os
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm
import random

# 设置路径
INPUT_DIR = "../../pic_chinese_char/test/"  # 原始数据路径
OUTPUT_DIR = "../../pic_chinese_char/test/output/"  # 增强后数据存储路径
NUM_AUGMENTATIONS = 10  # 每张图片生成增强版本数量

os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def extract_stroke_area(image):
    image_np = np.array(image)
    _, binary = cv2.threshold(image_np, 250, 255, cv2.THRESH_BINARY_INV)
    x, y, w, h = cv2.boundingRect(binary)
    cropped = image_np[y:y + h, x:x + w]
    if len(cropped.shape) > 2:
        cropped = cropped[:, :, 0]
    return cropped, (x, y, w, h, image_np.shape)


# def apply_perspective_transform(image, jitter=10, min_expand_ratio=0.9, max_expand_ratio=1.1):
#     """
#     对整个图像应用随机透视变换，防止缩小或扩张过度。
#     :param image: 输入灰度图像 (numpy array)
#     :param jitter: 角点随机偏移范围（像素）
#     :param min_expand_ratio: 最小的缩放比例，避免内容缩小过多
#     :param max_expand_ratio: 最大的扩张比例，避免内容放大过多
#     :return: 透视变换后的图像
#     """
#     h, w = image.shape
#     #jitter_h = int(jitter_ratio * h)
#     #jitter_w = int(jitter_ratio * w)
#     # 定义源点：图像的四个角
#     src_points = np.float32([
#         [0, 0],         # 左上角
#         [w - 1, 0],     # 右上角
#         [w - 1, h - 1],  # 右下角
#         [0, h - 1]      # 左下角
#     ])
#
#     # 目标点的随机偏移
#     dst_points = np.float32([
#         [random.randint(-jitter, jitter), random.randint(-jitter,
#                                                          jitter)],                          # 左上角
#         # 右上角
#         [w - 1 + random.randint(-jitter, jitter),
#          random.randint(-jitter, jitter)],
#         [w - 1 + random.randint(-jitter, jitter), h - 1 + \
#          random.randint(-jitter, jitter)],        # 右下角
#         [random.randint(-jitter, jitter), h - 1 + \
#          random.randint(-jitter, jitter)]                 # 左下角
#     ])
#
#     # 调整目标点使变换的缩放比限制在合理范围
#     dst_points[:, 0] = np.clip(
#         dst_points[:, 0], w * (1 - max_expand_ratio), w * max_expand_ratio)  # 限制宽度方向
#     dst_points[:, 1] = np.clip(
#         dst_points[:, 1], h * (1 - max_expand_ratio), h * max_expand_ratio)  # 限制高度方向
#
#     # 计算透视变换矩阵
#     matrix = cv2.getPerspectiveTransform(src_points, dst_points)
#
#     # 应用透视变换
#     transformed_image = cv2.warpPerspective(
#         image, matrix, (w, h), borderValue=255)
#
#     return transformed_image

def apply_perspective_transform(image, jitter_ratio=0.1, min_expand_ratio=0.9, max_expand_ratio=1.1):
    """
    对整个图像应用随机透视变换，防止缩小或扩张过度。
    :param image: 输入灰度图像 (numpy array)
    :param jitter_ratio: 角点随机偏移范围（相对图像大小的比例）
    :param min_expand_ratio: 最小的缩放比例，避免内容缩小过多
    :param max_expand_ratio: 最大的扩张比例，避免内容放大过多
    :return: 透视变换后的图像
    """
    h, w = image.shape
    jitter_h = int(jitter_ratio * h)  # 高度方向最大偏移像素
    jitter_w = int(jitter_ratio * w)  # 宽度方向最大偏移像素

    # 定义源点：图像的四个角
    src_points = np.float32([
        [0, 0],         # 左上角
        [w - 1, 0],     # 右上角
        [w - 1, h - 1],  # 右下角
        [0, h - 1]      # 左下角
    ])

    # 目标点的随机偏移
    dst_points = np.float32([
        [
            random.uniform(0, jitter_w),
            random.uniform(0, jitter_h)
        ],  # 左上角
        [
            w - 1 + random.uniform(-jitter_w, 0),
            random.uniform(0, jitter_h)
        ],  # 右上角
        [
            w - 1 + random.uniform(-jitter_w, 0),
            h - 1 + random.uniform(-jitter_h, 0)
        ],  # 右下角
        [
            random.uniform(0, jitter_w),
            h - 1 + random.uniform(-jitter_h,0)
        ]  # 左下角
    ])

    # 调整目标点，限制在合理缩放范围内
    dst_points[:, 0] = np.clip(dst_points[:, 0], 0, w - 1)  # 限制宽度方向
    dst_points[:, 1] = np.clip(dst_points[:, 1], 0, h - 1)  # 限制高度方向

    # 计算透视变换矩阵
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # 应用透视变换，保持原图大小
    transformed_image = cv2.warpPerspective(
        image, matrix, (w, h), borderValue=255  # 使用白色填充边缘
    )

    return transformed_image

def adjust_stroke_thickness(image, method="dilate"):
    kernel = np.ones((2, 2), np.uint8)
    if method == "dilate":
        return cv2.dilate(image, kernel, iterations=1)
    elif method == "erode":
        return cv2.erode(image, kernel, iterations=1)
    return image


def add_random_gaps(image):
    h, w = image.shape
    num_gaps = np.random.randint(1, 4)
    for _ in range(num_gaps):
        x1, x2 = np.random.randint(0, w // 2), np.random.randint(w // 2, w)
        y = np.random.randint(0, h)
        image[y, x1:x2] = 255
    return image


def augment_dataset(input_dir, output_dir, num_augmentations):
    for char_folder in tqdm(os.listdir(input_dir), desc="Processing folders"):
        char_folder_path = os.path.join(input_dir, char_folder)
        if os.path.isdir(char_folder_path):
            output_char_folder = os.path.join(output_dir, char_folder)
            setup_output_dir(output_char_folder)

            for image_file in os.listdir(char_folder_path):
                input_image_path = os.path.join(char_folder_path, image_file)

                if image_file.endswith((".png", ".jpg", ".jpeg", ".bmp")):
                    image_file = image_file.split(".")[0]
                    image = Image.open(input_image_path).convert("L")
                    stroke_area, bbox = extract_stroke_area(image)

                    image.save(os.path.join(
                        output_char_folder, f"{image_file}_orig.png"))

                    x, y, w, h, shape = bbox
                    if w < 10 or h < 10:
                        continue

                    for i in range(num_augmentations):
                        # 使用透视变换替代 augment_stroke
                        augmented_image = apply_perspective_transform(
                            stroke_area, jitter_ratio=0.25, min_expand_ratio=0.9, max_expand_ratio=1.1)

                        # if np.random.rand() > 0.5:
                        #     augmented_image = adjust_stroke_thickness(
                        #         augmented_image, method="dilate")
                        if np.random.rand() > 0.7:
                            augmented_image = add_random_gaps(augmented_image)

                        augmented_image, _ = extract_stroke_area(augmented_image)

                        resized_augmented_image = cv2.resize(
                            augmented_image, (w,
                                              h), interpolation=cv2.INTER_AREA
                        )

                        full_image = np.full(shape, 255, dtype=np.uint8)
                        full_image[y:y + h, x:x + w] = resized_augmented_image
                        full_image = resized_augmented_image
                        output_image_path = os.path.join(
                            output_char_folder, f"{image_file}_{i}_aug.png")
                        cv2.imwrite(output_image_path, full_image)


if __name__ == "__main__":
    augment_dataset(INPUT_DIR, OUTPUT_DIR, NUM_AUGMENTATIONS)
