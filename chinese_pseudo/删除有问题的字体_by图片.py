# # '''使用MD5 查找字体图片中有问题的图片'''
# # import os
# # import hashlib
# # from tqdm import tqdm
# #
# # def load_predefined_images(predefined_image_dir):
# #     """
# #     预先读取一组图片并保存图片路径，返回去重后的图片列表。
# #     :param predefined_image_dir: 包含预定义图片的文件夹路径
# #     :return: 去重后的预定义图片的路径列表
# #     """
# #     predefined_images = set()  # 使用集合去重路径
# #
# #     # 遍历预定义的图片目录
# #     for filename in os.listdir(predefined_image_dir):
# #         if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
# #             image_path = os.path.join(predefined_image_dir, filename).replace("\\", "/")
# #             predefined_images.add(image_path)  # 使用集合自动去重
# #
# #     return list(predefined_images)  # 返回去重后的图片路径列表
# #
# #
# # def calculate_file_md5(file_path):
# #     """
# #     计算文件的 MD5 值
# #     :param file_path: 文件路径
# #     :return: 文件的 MD5 值（32字符的十六进制字符串）
# #     """
# #     md5 = hashlib.md5()
# #
# #     with open(file_path, 'rb') as file:
# #         while chunk := file.read(8192):  # 逐块读取文件内容
# #             md5.update(chunk)
# #
# #     return md5.hexdigest()
# #
# #
# # def find_and_remove_duplicates(image_dir, predefined_images):
# #     """
# #     遍历目标目录，删除与预定义图片相同的图片（通过文件哈希比较）
# #     :param image_dir: 目标图片目录
# #     :param predefined_images: 预定义图片的路径列表
# #     """
# #     predefined_hashes = set()  # 用于存储预定义图片的哈希值
# #
# #     # 计算预定义图片的哈希值，并将它们存储在集合中
# #     for predefined_image in predefined_images:
# #         hash_value = calculate_file_md5(predefined_image)
# #         predefined_hashes.add(hash_value)  # 将哈希值添加到集合中
# #
# #     # 遍历目标目录中的文件，并计算它们的哈希值
# #     for root, dirs, files in tqdm(os.walk(image_dir), total=len(os.listdir(image_dir))):
# #         for filename in files:
# #             if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
# #                 image_path = os.path.join(root, filename).replace("\\", "/")
# #
# #                 # 计算目标图片的哈希值
# #                 image_hash = calculate_file_md5(image_path)
# #
# #                 # 检查目标图片的哈希值是否在预定义哈希值集合中
# #                 if image_hash in predefined_hashes:
# #                     print(f"重复图片: {os.path.basename(image_path)}，删除该文件")
# #                     os.remove(image_path)  # 删除重复的图片
# #
# #
# # # 使用示例
# # predefined_image_dir = "C:/Users/ThomasZhang/Desktop/删除的图片"  # 预定义图片所在文件夹
# # image_dir = "C:/Users/ThomasZhang/PycharmProjects/single_font_250102"  # 目标图片文件夹
# #
# # # 先加载预定义图片的路径
# # predefined_images = load_predefined_images(predefined_image_dir)
# #
# # # 遍历目标文件夹并删除重复图片
# # find_and_remove_duplicates(image_dir, predefined_images)
#
#
# #================================================================================================
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


def calculate_file_md5(file_path, cache={}):
    """
    计算文件的 MD5 值并缓存，避免重复计算
    :param file_path: 文件路径
    :param cache: 用于存储已经计算的文件哈希值
    :return: 文件的 MD5 值（32字符的十六进制字符串）
    """
    if file_path in cache:
        return cache[file_path]

    md5 = hashlib.md5()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):  # 逐块读取文件内容
            md5.update(chunk)

    hash_value = md5.hexdigest()
    cache[file_path] = hash_value  # 将计算结果缓存起来
    return hash_value


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

    # 获取目标目录中的所有图片路径
    image_paths = []
    for root, dirs, files in os.walk(image_dir):
        for filename in files:
            if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                image_path = os.path.join(root, filename).replace("\\", "/")
                image_paths.append(image_path)

    # 遍历目标目录中的每个文件并检查是否与预定义图片重复
    for image_path in tqdm(image_paths, total=len(image_paths)):
        # 计算目标图片的哈希值
        image_hash = calculate_file_md5(image_path)

        # 检查目标图片的哈希值是否在预定义哈希值集合中
        if image_hash in predefined_hashes:
            print(f"重复图片: {os.path.basename(image_path)}，删除该文件")
            os.remove(image_path)  # 删除重复的图片


# 使用示例
predefined_image_dir = "C:/Users/ThomasZhang/Desktop/删除的图片"  # 预定义图片所在文件夹
image_dir = "C:/Users/ThomasZhang/PycharmProjects/single_font_250102"  # 目标图片文件夹

# 先加载预定义图片的路径
predefined_images = load_predefined_images(predefined_image_dir)

# 遍历目标文件夹并删除重复图片
find_and_remove_duplicates(image_dir, predefined_images)
#================================================================================================

# import os
# import hashlib
# from tqdm.contrib.concurrent import process_map
# from multiprocessing import Manager
#
# def load_predefined_images(predefined_image_dir):
#     """
#     预先读取一组图片并保存图片路径，返回去重后的图片列表。
#     :param predefined_image_dir: 包含预定义图片的文件夹路径
#     :return: 去重后的预定义图片的路径列表
#     """
#     predefined_images = set()  # 使用集合去重路径
#
#     # 遍历预定义的图片目录
#     for filename in os.listdir(predefined_image_dir):
#         if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
#             image_path = os.path.join(predefined_image_dir, filename).replace("\\", "/")
#             predefined_images.add(image_path)  # 使用集合自动去重
#
#     return list(predefined_images)  # 返回去重后的图片路径列表
#
#
# def calculate_file_md5(file_path, cache={}):
#     """
#     计算文件的 MD5 值并缓存，避免重复计算
#     :param file_path: 文件路径
#     :param cache: 用于存储已经计算的文件哈希值
#     :return: 文件的 MD5 值（32字符的十六进制字符串）
#     """
#     if file_path in cache:
#         return cache[file_path]
#
#     md5 = hashlib.md5()
#     with open(file_path, 'rb') as file:
#         while chunk := file.read(8192):  # 逐块读取文件内容
#             md5.update(chunk)
#
#     hash_value = md5.hexdigest()
#     cache[file_path] = hash_value  # 将计算结果缓存起来
#     return hash_value
#
#
# def process_image(image_path, predefined_hashes, cache):
#     """
#     处理每个目标图片文件：计算其MD5并与预定义图片对比，如果相同则删除。
#     :param image_path: 目标图片路径
#     :param predefined_hashes: 预定义图片哈希值集合
#     :param cache: 哈希缓存
#     :return: 被删除的图片路径
#     """
#     image_hash = calculate_file_md5(image_path, cache)
#
#     # 检查目标图片的哈希值是否在预定义哈希值集合中
#     if image_hash in predefined_hashes:
#         os.remove(image_path)  # 删除重复的图片
#         return image_path  # 返回删除的文件路径
#
#
# def find_and_remove_duplicates(image_dir, predefined_images):
#     """
#     遍历目标目录，删除与预定义图片相同的图片（通过文件哈希比较）
#     :param image_dir: 目标图片目录
#     :param predefined_images: 预定义图片的路径列表
#     """
#     predefined_hashes = set()  # 用于存储预定义图片的哈希值
#
#     # 计算预定义图片的哈希值，并将它们存储在集合中
#     for predefined_image in predefined_images:
#         hash_value = calculate_file_md5(predefined_image)
#         predefined_hashes.add(hash_value)  # 将哈希值添加到集合中
#
#     # 获取目标目录中的所有图片路径
#     image_paths = []
#     for root, dirs, files in os.walk(image_dir):
#         for filename in files:
#             if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
#                 image_path = os.path.join(root, filename).replace("\\", "/")
#                 image_paths.append(image_path)
#
#     # 使用process_map代替Pool来自动显示进度条
#     results = process_map(
#         process_image,
#         image_paths,
#         args=(predefined_hashes, {}),  # 传递额外的参数
#         max_workers=8,  # 设置最多并发进程数
#         chunk_size=50,  # 设置每个进程处理的任务数量
#         desc="正在删除重复图片"  # 设置进度条描述
#     )
#     # 打印删除的文件路径
#     deleted_files = [result for result in results if result]  # 过滤非空结果
#     if deleted_files:
#         print(f"已删除 {len(deleted_files)} 个重复文件：")
#         for deleted_file in deleted_files:
#             print(f"删除图片: {deleted_file}")
#     else:
#         print("没有找到重复文件。")
#
#
# if __name__ == '__main__':
#     # 使用示例
#     predefined_image_dir = "C:/Users/ThomasZhang/Desktop/删除的图片"  # 预定义图片所在文件夹
#     image_dir = "C:/Users/ThomasZhang/PycharmProjects/single_font_250102"  # 目标图片文件夹
#
#     # 先加载预定义图片的路径
#     predefined_images = load_predefined_images(predefined_image_dir)
#
#     # 遍历目标文件夹并删除重复图片
#     find_and_remove_duplicates(image_dir, predefined_images)
