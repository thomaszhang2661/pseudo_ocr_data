# # # 作者：张健 Thomas Zhang
# # # 时间：2024/7/2,22:03
# # from PIL import Image, ImageDraw
# # import numpy as np
# # from tensorflow.keras.datasets import mnist
# #
# # def create_handwritten_number_image(numbers, output_path):
# #     # Load MNIST dataset
# #     (x_train, y_train), (x_test, y_test) = mnist.load_data()
# #
# #     # Image settings
# #     width = 280
# #     height = 28
# #     cell_width = width // len(numbers)
# #
# #     # Create a new image with white background
# #     image = Image.new('L', (width, height), 255)
# #     draw = ImageDraw.Draw(image)
# #
# #     # Draw the numbers and the grid
# #     for i, number in enumerate(numbers):
# #         # Get a random sample of the target number from MNIST
# #         idx = np.where(y_train == int(number))[0]
# #         digit_image = x_train[np.random.choice(idx)]
# #
# #         # Resize digit image to fit cell
# #         digit_image = Image.fromarray(digit_image).resize((cell_width, height), Image.ANTIALIAS)
# #
# #         # Paste the digit image in the correct location
# #         image.paste(digit_image, (i * cell_width, 0))
# #
# #         # Draw vertical dashed line
# #         if i > 0:
# #             for y_dash in range(0, height, 4):
# #                 draw.line([(i * cell_width, y_dash), (i * cell_width, y_dash + 2)], fill=0)
# #
# #     # Draw border
# #     draw.rectangle([0, 0, width - 1, height - 1], outline=0)
# #
# #     # Save the image
# #     image.save(output_path)
# #
# # # Example usage
# # numbers = '180029'
# # output_path = 'output_image.png'
# # create_handwritten_number_image(numbers, output_path)
#
# # ===========
# # version 2
# #
# # from PIL import Image, ImageDraw
# # import numpy as np
# # import random
# # import string
# # import tensorflow as tf
# # import time
# # import math
# #
# # def generate_random_number_string(length):
# #     return ''.join(random.choices(string.digits, k=length))
# #
# # def create_handwritten_number_image(numbers, output_path):
# #     # Load MNIST dataset
# #     (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
# #
# #     # Image settings
# #     width = 52 * len(numbers) #28 52
# #     height = 82  #28
# #     cell_width = width // len(numbers)
# #
# #     # Create a new image with white background
# #     image = Image.new('L', (width, height), 255)
# #     draw = ImageDraw.Draw(image)
# #
# #     rand_dash_all = random.randint(6, 9)
# #     rand_dash_inter = random.randint(1, 3)
# #
# #     #rand_dash_select = random.randint(0,2)
# #     rand_dash_select = 1
# #     # Draw the numbers and the grid
# #     for i, number in enumerate(numbers):
# #         # Get a random sample of the target number from MNIST
# #         idx = np.where(y_train == int(number))[0]
# #         digit_image = x_train[np.random.choice(idx)]
# #
# #         # Invert the colors of the digit image to make it white background and black digit
# #         digit_image = 255 - digit_image
# #
# #         # 假设你需要的缩放比例范围是 0.5 到 1.0
# #         scale_factor_x = random.uniform(0.7, 1.0)
# #         scale_factor_y = random.uniform(0.7, 1.0)
# #         # Convert the array to an image and resize to fit cell
# #         scaled_w = int(width/len(numbers) * scale_factor_x)
# #         scaled_h = int(height * scale_factor_y)
# #         digit_image = Image.fromarray(digit_image).resize((scaled_w, scaled_h), Image.ANTIALIAS)
# #
# #         # # 计算缩放后的数字图像大小
# #         # scaled_width = int(digit_image.width * scale_factor)
# #         # scaled_height = int(digit_image.height * scale_factor)
# #         #
# #         # # 缩放数字图像
# #         # scaled_digit_image = digit_image.resize((scaled_width, scaled_height), Image.ANTIALIAS)
# #
# #         offset_x = random.randint(0, width/len(numbers) - scaled_w)
# #         offset_y = random.randint(0, height - scaled_h)
# #         # 计算新的粘贴位置
# #         paste_position = (i * cell_width + offset_x, offset_y)
# #         # Paste the digit image in the correct location
# #         image.paste(digit_image, paste_position)
# #
# #         if rand_dash_select == 0:
# #             pass
# #         elif rand_dash_select == 1:
# #         # Draw vertical dashed line
# #             if i > 0:
# #                 for y_dash in range(0, height, rand_dash_all):
# #                     draw.line([(i * cell_width, y_dash), (i * cell_width, y_dash + rand_dash_inter)], fill=0)
# #         elif rand_dash_select == 2:
# #             # Draw vertical dashed line
# #             if i > 0:
# #                 draw.line(((i * cell_width, 0),(i * cell_width, height)), fill=0)
# #
# #     # Draw border
# #     draw.rectangle([0, 0, width - 1, height - 1], outline=0, width=3)
# #
# #     margin = random.randint(5, 20)
# #     # Create a larger image with margins
# #     larger_width = width + 2 * margin
# #     larger_height = height + 2 * margin
# #     larger_image = Image.new('L', (larger_width, larger_height), 255)
# #     larger_image.paste(image, (margin, margin))
# #
# #
# #     mean = 0  # 均值
# #     stddev = 5  # 标准差
# #     random_angle = np.random.normal(mean, stddev)
# #
# #     # 限制角度在 [-10, 10] 范围内
# #     random_angle = np.clip(random_angle, -3, 3)
# #     # 对图片进行旋转
# #     rotated_img = larger_image.rotate(random_angle, fillcolor=(255))
# #     # Save the image
# #     rotated_img.save(output_path)
# # # Example usage
# # random.seed(42)  # For reproducibility
# # output_paths = []
# #
# # for i in range(10000):  # Generate 3 example images
# #     length = random.randint(6, 14)
# #     text = generate_random_number_string(length)
# #     timestamp = int(time.time())
# #     output_path = f'./data/{timestamp}_{text}.jpg'
# #     create_handwritten_number_image(text, output_path)
# #     output_paths.append(output_path)
# #
# # output_paths
#
# # ========= version 2 ended
# from PIL import Image, ImageDraw
# import numpy as np
# import random
# import string
# import tensorflow as tf
# import time
# import multiprocessing
# import os
# from tqdm import tqdm
#
#
# def generate_random_number_string(length):
#     return ''.join(random.choices(string.digits, k=length))
#
#
# def load_mnist_data():
#     (x_train, y_train), _ = tf.keras.datasets.mnist.load_data()
#     mnist_data = {}
#     for i in range(10):
#         mnist_data[i] = x_train[y_train == i]
#     return mnist_data
#
#
# def load_local_images(image_directory):
#     mnist_data = {}
#     for filename in os.listdir(image_directory):
#         if filename.endswith('.png'):
#             label, _ = filename.split('_', 1)
#             label = int(label)
#             filepath = os.path.join(image_directory, filename)
#             if label not in mnist_data:
#                 mnist_data[label] = []
#             image = Image.open(filepath).convert('L')  # Convert to grayscale
#             mnist_data[label].append(np.array(image))
#     return mnist_data
#
#
# def create_handwritten_number_image(numbers, output_path, mnist_data):
#     width = 52 * len(numbers)
#     height = 82
#     cell_width = width // len(numbers)
#
#     image = Image.new('L', (width, height), 255)
#     draw = ImageDraw.Draw(image)
#
#     rand_dash_all = random.randint(6, 9)
#     rand_dash_inter = random.randint(1, 3)
#     rand_dash_select = 1
#
#     for i, number in enumerate(numbers):
#         digit_images = mnist_data[int(number)]
#         digit_image = digit_images[np.random.choice(digit_images.shape[0])]
#         #digit_image = 255 - digit_image
#
#         scale_factor_x = random.uniform(0.7, 1.0)
#         scale_factor_y = random.uniform(0.7, 1.0)
#         scaled_w = int(width / len(numbers) * scale_factor_x)
#         scaled_h = int(height * scale_factor_y)
#         digit_image = Image.fromarray(digit_image).resize((scaled_w, scaled_h), Image.ANTIALIAS)
#
#         offset_x = random.randint(0, width // len(numbers) - scaled_w)
#         offset_y = random.randint(0, height - scaled_h)
#         paste_position = (i * cell_width + offset_x, offset_y)
#         image.paste(digit_image, paste_position)
#
#         if rand_dash_select == 1 and i > 0:
#             for y_dash in range(0, height, rand_dash_all):
#                 draw.line([(i * cell_width, y_dash), (i * cell_width, y_dash + rand_dash_inter)], fill=0)
#         elif rand_dash_select == 2 and i > 0:
#             draw.line([(i * cell_width, 0), (i * cell_width, height)], fill=0)
#
#     draw.rectangle([0, 0, width - 1, height - 1], outline=0, width=3)
#
#     left_margin = random.randint(0, 20)
#     right_margin = random.randint(0, 20)
#     top_margin = random.randint(0, 20)
#     bottom_margin = random.randint(0, 20)
#     larger_width = width + left_margin + right_margin
#     larger_height = height + top_margin + bottom_margin
#     larger_image = Image.new('L', (larger_width, larger_height), 255)
#     larger_image.paste(image, (left_margin, top_margin))
#     mean = 0
#     stddev = 5
#     random_angle = np.random.normal(mean, stddev)
#     random_angle = np.clip(random_angle, -3, 3)
#     rotated_img = larger_image.rotate(random_angle, fillcolor=(255))
#     rotated_img.save(output_path)
#     #larger_image.save(output_path)
#
#
#
# def process_image_wrapper(args):
#     output_path, text, mnist_data = args
#     create_handwritten_number_image(text, output_path, mnist_data)
#     return output_path
#
# if __name__ == '__main__':
#     random.seed(42)
#     #mnist_data = load_mnist_data()
#     image_directory = '../pseudo_ocr_data_xuehao/mnist_images_checked/'  # Update this to the directory containing your image files
#     mnist_data = load_local_images(image_directory)
#     output_paths_and_texts = []
#     for i in range(100):
#         length = random.randint(6, 14)
#         text = generate_random_number_string(length)
#         timestamp = int(time.time()) + i  # To ensure unique timestamps
#         output_path = f'../pseudo_ocr_data_xuehao/gen_mnist_data/{timestamp}_{text}.jpg'
#         output_paths_and_texts.append((output_path, text))
#
#     num_processes = multiprocessing.cpu_count()
#
#     with multiprocessing.Pool(processes=num_processes) as pool:
#         results = list(tqdm(pool.imap_unordered(process_image_wrapper, [(path, text, mnist_data) for path, text in output_paths_and_texts]), total=len(output_paths_and_texts)))


from PIL import Image, ImageDraw
import numpy as np
import random
import string
import tensorflow as tf
import time
import multiprocessing
import os
from tqdm import tqdm
import cv2  # OpenCV library for faster image processing


def generate_random_number_string(length):
    return ''.join(random.choices(string.digits, k=length))


def load_local_images(image_directory):
    mnist_data = {}
    for filename in os.listdir(image_directory):
        if filename.endswith('.png'):
            label, _ = filename.split('_', 1)
            label = int(label)
            filepath = os.path.join(image_directory, filename)
            if label not in mnist_data:
                mnist_data[label] = []
            image = Image.open(filepath).convert('L')  # Convert to grayscale
            mnist_data[label].append(np.array(image))
    return mnist_data


def create_handwritten_number_image(numbers, output_path, mnist_data):
    width = 52 * len(numbers)
    height = 82
    cell_width = width // len(numbers)

    # Create a new image with white background
    image = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(image)

    rand_dash_all = random.randint(6, 9)
    rand_dash_inter = random.randint(1, 3)
    rand_dash_select = 1

    for i, number in enumerate(numbers):
        digit_images = mnist_data[int(number)]
        digit_image = digit_images[np.random.choice(len(digit_images))]

        # Invert colors and resize with OpenCV
        #digit_image = 255 - digit_image
        scaled_w = int(width / len(numbers) * random.uniform(0.7, 1.0))
        scaled_h = int(height * random.uniform(0.7, 1.0))
        digit_image = cv2.resize(digit_image, (scaled_w, scaled_h), interpolation=cv2.INTER_LINEAR)
        digit_image = Image.fromarray(digit_image)

        offset_x = random.randint(0, width // len(numbers) - scaled_w)
        offset_y = random.randint(0, height - scaled_h)
        paste_position = (i * cell_width + offset_x, offset_y)
        image.paste(digit_image, paste_position)

        if rand_dash_select == 1 and i > 0:
            for y_dash in range(0, height, rand_dash_all):
                draw.line([(i * cell_width, y_dash), (i * cell_width, y_dash + rand_dash_inter)], fill=0)
        elif rand_dash_select == 2 and i > 0:
            draw.line([(i * cell_width, 0), (i * cell_width, height)], fill=0)

    draw.rectangle([0, 0, width - 1, height - 1], outline=0, width=3)

    # left_margin = random.randint(0, 20)
    # right_margin = random.randint(0, 20)
    # top_margin = random.randint(0, 20)
    # bottom_margin = random.randint(0, 20)
    left_margin = 15
    right_margin = 15
    top_margin = 15
    bottom_margin = 15
    larger_width = width + left_margin + right_margin
    larger_height = height + top_margin + bottom_margin
    larger_image = Image.new('L', (larger_width, larger_height), 255)
    larger_image.paste(image, (left_margin, top_margin))

    # random_angle = np.clip(np.random.normal(0, 5), -3, 3)
    # rotated_img = larger_image.rotate(random_angle, fillcolor=(255))
    larger_image.save(output_path)


def process_image_wrapper(args):
    output_path, text, mnist_data = args
    create_handwritten_number_image(text, output_path, mnist_data)
    return output_path

if __name__ == '__main__':
    random.seed(42)
    image_directory = '../pseudo_ocr_data_xuehao/mnist_images_checked_0803/'
    mnist_data = load_local_images(image_directory)
    output_paths_and_texts = []
    for i in range(100):
        length = random.randint(6, 14)
        text = generate_random_number_string(length)
        timestamp = int(time.time()) + i
        output_path = f'../pseudo_ocr_data_xuehao/gen_mnist_data/{timestamp}_{text}.jpg'
        output_paths_and_texts.append((output_path, text))

    num_processes = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = list(tqdm(pool.imap_unordered(process_image_wrapper, [(path, text, mnist_data) for path, text in output_paths_and_texts]), total=len(output_paths_and_texts)))
