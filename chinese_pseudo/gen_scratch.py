# # 作者：张健 Thomas Zhang
# # 时间：2024/8/5,14:58
# from PIL import Image, ImageDraw
# import numpy as np
# import random
# import os
#
# def apply_scratches(image_path, output_path, num_scratches=10, max_scratch_length=50):
#     # 打开图像
#     image = Image.open(image_path).convert('RGB')
#     draw = ImageDraw.Draw(image)
#     width, height = image.size
#
#     for _ in range(num_scratches):
#         # 随机生成起始和结束点
#         x1 = random.randint(0, width)
#         y1 = random.randint(0, height)
#         x2 = random.randint(0, width)
#         y2 = random.randint(0, height)
#
#         # 随机生成线条宽度
#         line_width = random.randint(1, 5)
#
#         # 随机生成线条颜色
#         line_color = (0, 0, 0)  # 黑色线条
#
#         # 绘制直线
#         draw.line([(x1, y1), (x2, y2)], fill=line_color, width=line_width)
#
#     # 模拟涂抹效果
#     num_smears = 5
#     for _ in range(num_smears):
#         # 随机选择涂抹区域
#         smear_width = random.randint(20, 50)
#         smear_height = random.randint(20, 50)
#         smear_x = random.randint(0, width - smear_width)
#         smear_y = random.randint(0, height - smear_height)
#
#         # 生成随机的涂抹颜色
#         smear_color = (0, 0, 0)  # 黑色涂抹
#
#         # 在图像上涂抹
#         draw.rectangle([smear_x, smear_y, smear_x + smear_width, smear_y + smear_height], fill=smear_color)
#
#     # 保存处理后的图像
#     image.save(output_path)
#
# def main():
#     input_image_path = './1722839715_61272769.png'  # 替换为你的图像路径
#     output_image_path = 'output_image.png'  # 替换为你想要保存的路径
#     apply_scratches(input_image_path, output_image_path)
#
# if __name__ == "__main__":
#     main()


from PIL import Image, ImageDraw
import numpy as np
import random
import math


def draw_curve(draw, points, color, width):
    """绘制曲线，通过多段直线模拟连续曲线"""
    if len(points) < 2:
        return

    # 插值点数，越大曲线越平滑
    num_intervals = 100

    def interpolate(p1, p2, t):
        """线性插值"""
        return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)

    def bezier(t, p0, p1, p2, p3):
        """计算贝塞尔曲线点"""
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        return (x, y)

    # 生成贝塞尔曲线上的点
    curve_points = []
    for i in range(len(points) - 3):
        p0 = points[i]
        p1 = points[i + 1]
        p2 = points[i + 2]
        p3 = points[i + 3] if i + 3 < len(points) else points[-1]

        for t in np.linspace(0, 1, num_intervals):
            curve_points.append(bezier(t, p0, p1, p2, p3))

    # 绘制曲线
    for i in range(1, len(curve_points)):
        draw.line([curve_points[i - 1], curve_points[i]], fill=color, width=width)


# def draw_horizontal_scratch(image, num_scratch_lines_max=8, line_width_range=(3, 6), color=None):
#     """
#     在图像上绘制横向划痕。
#
#     :param image: 输入的图像对象（PIL.Image）。
#     :param num_scratch_lines: 划痕的数量。
#     :param line_width_range: 划痕的宽度范围（最小宽度，最大宽度）。
#     :param color: 划痕的颜色。如果为 None，将随机选择灰度值。
#     """
#     draw = ImageDraw.Draw(image)
#     width, height = image.size
#     num_scratch_lines = random.randint(3,num_scratch_lines_max)
#     bound = int(height / 4)
#     # 计算均匀间隔
#     if num_scratch_lines > 1:
#         y_positions = [bound + (int((i + 0.5) * height - 2 * bound) / num_scratch_lines) for i in range(num_scratch_lines)]
#     else:
#         y_positions = [height // 2]  # 如果只有一条划痕，放在中间
#
#     # 设置边界以防划痕超出图像边界
#
#     y_positions = [max(bound, min(y, height - bound - 1)) for y in y_positions]
#
#     for y in y_positions:
#         # 随机选择划痕宽度
#         line_width = random.randint(*line_width_range)
#         # if color is None:
#         #     color = random.randint(0, 255)  # 随机灰度值
#         color = 0
#         # 绘制横线
#         draw.line([(0, y), (width, y)], fill=color, width=line_width)


def draw_horizontal_scratch(image, num_scratch_lines_max=5, line_width_range=(3, 6), color=None, angle_range=(-30, 30)):
    """
    在图像上绘制划痕。

    :param image: 输入的图像对象（PIL.Image）。
    :param num_scratch_lines_max: 划痕的数量。
    :param line_width_range: 划痕的宽度范围（最小宽度，最大宽度）。
    :param color: 划痕的颜色。如果为 None，将随机选择灰度值。
    :param angle_range: 划痕的角度范围（最小角度，最大角度，单位为度）。
    """
    draw = ImageDraw.Draw(image)
    width, height = image.size
    num_scratch_lines = random.randint(2, num_scratch_lines_max)
    bound = int(height / 4)

    # 计算均匀间隔
    if num_scratch_lines > 1:
        y_positions = [bound + (int((i + 0.5) * height - 2 * bound) / num_scratch_lines) for i in
                       range(num_scratch_lines)]
    else:
        y_positions = [height // 2]  # 如果只有一条划痕，放在中间

    # 设置边界以防划痕超出图像边界
    y_positions = [max(bound, min(y, height - bound - 1)) for y in y_positions]

    # if color is None:
    #     color = random.randint(0, 255)  # 随机灰度值
    color = 0
    angle = random.uniform(*angle_range)

    for y in y_positions:
        # 随机选择划痕宽度
        line_width = random.randint(*line_width_range)

        # 随机选择划痕角度
        angle_rad = math.radians(angle)  # 将角度转换为弧度

        # 计算线条的起始和结束点
        x_start = 0
        y_start = y - (width / 2) * math.tan(angle_rad)
        x_end = width
        y_end = y + (width / 2) * math.tan(angle_rad)

        # 限制线条在图像边界内
        if y_start < 0:
            y_start = 0
            x_start = -y_start / math.tan(angle_rad)
        if y_end > height:
            y_end = height
            x_end = width - (y_end - height) / math.tan(angle_rad)

        # 绘制划痕
        draw.line([(x_start, y_start), (x_end, y_end)], fill=color, width=line_width)


def apply_scratches(image, num_curves_in=9, max_curve_width=3):
    # 打开图像
    draw = ImageDraw.Draw(image)
    width, height = image.size
    # draw_horizontal_scratch(image, num_scratch_lines_max=8, line_width_range=(2, 3))

    if random.choice((0,1)) == 0:
        draw_horizontal_scratch(image, num_scratch_lines_max=5, line_width_range=(3, 4))
    else:
        # 应用曲线涂抹
        num_curves = random.randint(5, num_curves_in)
        for _ in range(num_curves):
            num_points = random.randint(4, 6)
            points = [(random.randint(0, width), random.randint(0, height)) for _ in range(num_points)]
            curve_width = random.randint(2, max_curve_width)
            #curve_color = random.randint(0, 255)  # 随机灰度值
            curve_color = 0

            draw_curve(draw, points, curve_color, curve_width)

    #保存处理后的图像
    #image.save(output_path)
    return image


def main():
    input_image_path = './1722839715_61272769.png'  # 替换为你的图像路径
    output_image_path = 'output_image.png'  # 替换为你想要保存的路径
    image = Image.open(input_image_path).convert('L')  # 转换为灰度图像
    image_out = apply_scratches(image)
    image_out.save(output_image_path)

if __name__ == "__main__":
    main()
