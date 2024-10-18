# 作者：张健 Thomas Zhang
# 时间：2024/8/16,01:09
import gzip
import numpy as np
import os
from PIL import Image
from datetime import datetime

def extract_images_labels(image_file, label_file):
    with gzip.open(image_file, 'rb') as img_f, gzip.open(label_file, 'rb') as lbl_f:
        # Skip headers
        img_f.read(16)
        lbl_f.read(8)

        # Read data
        images = np.frombuffer(img_f.read(), dtype=np.uint8).reshape(-1, 28, 28)
        labels = np.frombuffer(lbl_f.read(), dtype=np.uint8)
    return images, labels

def load_class_mapping(mapping_file):
    class_mapping = {}
    with open(mapping_file, 'r') as f:
        for line in f:
            label, ascii_code = line.split()
            class_mapping[int(label)] = chr(int(ascii_code))
    return class_mapping

def save_emnist_images(x_data, y_data, output_dir, class_mapping):
    os.makedirs(output_dir, exist_ok=True)
    for i in range(len(x_data)):
        label = y_data[i]
        char_label = class_mapping.get(label, None)
        #if char_label is not None and char_label.isalpha():
        # Only save images of alphabetic characters (a-z, A-Z)
        inverted_image = 255 - x_data[i]  # 图像反色
        image = Image.fromarray(inverted_image.astype(np.uint8), mode='L')
        image = image.rotate(-90, expand=True)  # 旋转图像90度
        image = image.transpose(Image.FLIP_LEFT_RIGHT)  # 镜像翻转
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        image.save(os.path.join(output_dir, f'{timestamp}_{char_label}.png'))

# 加载EMNIST数据
image_file_path = '/Users/zhangjian/Downloads/gzip/emnist-bymerge-train-images-idx3-ubyte.gz'
label_file_path = '/Users/zhangjian/Downloads/gzip/emnist-bymerge-train-labels-idx1-ubyte.gz'
mapping_file_path = '/Users/zhangjian/Downloads/gzip/emnist-bymerge-mapping.txt'  # 使用合适的映射文件

images, labels = extract_images_labels(image_file_path, label_file_path)
class_mapping = load_class_mapping(mapping_file_path)

# 保存前100张图像
output_directory = './emnist_images'
save_emnist_images(images[:100], labels[:100], output_directory, class_mapping)
