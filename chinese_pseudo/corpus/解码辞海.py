from pyglossary.glossary import Glossary

# 创建 Glossary 对象
glossary = Glossary()

# 加载 MDX 文件
file_path = "汉语辞海.mdx"  # 替换为实际文件路径
output_path = "output.txt"  # 提取内容保存的文件路径

# 加载 MDX 文件
glossary.read(file_path)

# 将内容导出为 TXT 格式
with open(output_path, "w", encoding="utf-8") as f:
    for key, value in glossary:
        f.write(f"{key}: {value}\n")

print(f"MDX 内容已提取到 {output_path}")
