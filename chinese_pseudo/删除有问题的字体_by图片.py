'''使用MD5 查找字体图片中有问题的图片'''
import os
import hashlib
from tqdm import tqdm

def load_predefined_images(predefined_image_dir):
    """
    预先读取一组图片并保存图片路径，返回去重后的图片列表。
    :param predefined_image_dir: 包含预定义图片的文件夹路径
    :return: 去重后的预定义图片的路径列表
    """
    predefined_images = set()  # 使用集合去重路径

    # 遍历预定义的图片目录
    for filename in os.listdir(predefined_image_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            image_path = os.path.join(predefined_image_dir, filename).replace("\\", "/")
            predefined_images.add(image_path)  # 使用集合自动去重

    return list(predefined_images)  # 返回去重后的图片路径列表


def calculate_file_md5(file_path):
    """
    计算文件的 MD5 值
    :param file_path: 文件路径
    :return: 文件的 MD5 值（32字符的十六进制字符串）
    """
    md5 = hashlib.md5()

    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):  # 逐块读取文件内容
            md5.update(chunk)

    return md5.hexdigest()


def find_and_remove_duplicates(image_dir, predefined_images):
    """
    遍历目标目录，删除与预定义图片相同的图片（通过文件哈希比较）
    :param image_dir: 目标图片目录
    :param predefined_images: 预定义图片的路径列表
    """
    predefined_hashes = set()  # 用于存储预定义图片的哈希值

    # 计算预定义图片的哈希值，并将它们存储在集合中
    for predefined_image in predefined_images:
        hash_value = calculate_file_md5(predefined_image)
        predefined_hashes.add(hash_value)  # 将哈希值添加到集合中

    # 遍历目标目录中的文件，并计算它们的哈希值
    for root, dirs, files in tqdm(os.walk(image_dir), total=len(os.listdir(image_dir))):
        for filename in files:
            if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                image_path = os.path.join(root, filename).replace("\\", "/")

                # 计算目标图片的哈希值
                image_hash = calculate_file_md5(image_path)

                # 检查目标图片的哈希值是否在预定义哈希值集合中
                if image_hash in predefined_hashes:
                    print(f"重复图片: {os.path.basename(image_path)}，删除该文件")
                    os.remove(image_path)  # 删除重复的图片


# 使用示例
predefined_image_dir = "C:/Users/ThomasZhang/Desktop/删除的图片"  # 预定义图片所在文件夹
image_dir = "C:/Users/ThomasZhang/PycharmProjects/pseudo_chinese_images_250101"  # 目标图片文件夹

# 先加载预定义图片的路径
predefined_images = load_predefined_images(predefined_image_dir)

# 遍历目标文件夹并删除重复图片
find_and_remove_duplicates(image_dir, predefined_images)
