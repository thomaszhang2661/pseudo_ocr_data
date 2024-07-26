# 作者：张健 Thomas Zhang
# 时间：2024/7/3,13:07
import os
import numpy as np
from PIL import Image
import tensorflow as tf

def save_mnist_images(x_data, y_data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i in range(len(x_data)):
        inverted_image = 255 - x_data[i]
        image = Image.fromarray(inverted_image.astype(np.uint8), mode='L')
        label = y_data[i]
        image.save(os.path.join(output_dir, f'{label}_{i}.png'))

# 示例：保存前100张训练集图片到本地文件夹
output_directory = './mnist_images'
(x_train, y_train), _ = tf.keras.datasets.mnist.load_data()
print(len(x_train[:]),len(y_train[:]))
save_mnist_images(x_train[:], y_train[:], output_directory)