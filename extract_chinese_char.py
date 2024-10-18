# 作者：张健 Thomas Zhang
# 时间：2024/8/15,20:39
# from fontTools.ttLib import TTFont
#
#
# def extract_chinese_characters_from_font(font_path):
#     font = TTFont(font_path)
#     characters = set()
#
#     # 获取字形映射表
#     cmap = font.get('cmap')
#     for table in cmap.tables:
#         if table.platformID == 3 and table.platformEncodingID == 1:  # 针对简体中文字体
#             for codepoint, name in table.cmap.items():
#                 if 0x4E00 <= codepoint <= 0x9FFF:  # 汉字 Unicode 范围
#                     characters.add(chr(codepoint))
#
#     return characters
#
#
# # 示例使用
# font_path = '/path/to/your/font.ttf'
# chinese_chars = extract_chinese_characters_from_font(font_path)
# print(chinese_chars)


# from fontTools.ttLib import TTFont
# import os
#
#
# def extract_chinese_characters_from_font(font_path):
#     font = TTFont(font_path)
#     characters = set()
#
#     # 获取字形映射表
#     cmap = font.get('cmap')
#     for table in cmap.tables:
#         if table.platformID == 3 and table.platformEncodingID == 1:  # 针对简体中文字体
#             for codepoint, name in table.cmap.items():
#                 if 0x4E00 <= codepoint <= 0x9FFF:  # 汉字 Unicode 范围
#                     characters.add(chr(codepoint))
#
#     return characters
#
#
# def extract_characters_from_fonts_in_directory(directory_path):
#     all_characters = set()
#     for root, _, files in os.walk(directory_path):
#         for file in files:
#             if file.lower().endswith(('.ttf', '.otf')):
#                 font_path = os.path.join(root, file)
#                 print(f"Processing font: {font_path}")
#                 characters = extract_chinese_characters_from_font(font_path)
#                 all_characters.update(characters)
#
#     return all_characters
#
#
# # 示例使用
# directory_path = '/System/Library/Fonts/'
# chinese_chars = extract_characters_from_fonts_in_directory(directory_path)
#
# # 打印提取到的汉字字符
# print("Extracted Chinese characters:")
# print(chinese_chars)


from fontTools.ttLib import TTFont
import os


def extract_chinese_characters_from_font(font_path):
    font = TTFont(font_path)
    characters = set()

    # 获取所有的字形映射表
    cmap = font.get('cmap')
    for table in cmap.tables:
        # 确保使用合适的 cmap 表
        try:
            for codepoint, name in table.cmap.items():
                if 0x4E00 <= codepoint <= 0x9FFF:  # 汉字 Unicode 范围
                    characters.add(chr(codepoint))
        except AttributeError:
            # 如果表没有 cmap 属性，我们就跳过它
            continue

    return characters


def extract_characters_from_fonts_in_directory(directory_path):
    all_characters = set()
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.ttf', '.otf')):
                font_path = os.path.join(root, file)
                print(f"Processing font: {font_path}")
                characters = extract_chinese_characters_from_font(font_path)
                all_characters.update(characters)

    return all_characters


# 示例使用
directory_path = '/System/Library/Fonts/'
chinese_chars = extract_characters_from_fonts_in_directory(directory_path)

# 打印提取到的汉字字符
print("Extracted Chinese characters:")
print(chinese_chars)
print(len(chinese_chars))
