# 作者：张健 Thomas Zhang
# 时间：2024/11/15,22:44
import cv2
import os

# def resize_image(image, desired_size):
#     ''' Helper function to resize an image while keeping the aspect ratio.
#     Parameter
#     ---------
#
#     image: np.array
#         The image to be resized.
#
#     desired_size: (int, int)
#         The (height, width) of the resized image
#
#     Return
#     ------
#
#     image: np.array
#         The image of size = desired_size
#
#     bounding box: (int, int, int, int)
#         (x, y, w, h) in percentages of the resized image of the original
#     '''
#     size = image.shape[:2]
#     #print('size:', size)
#     #print(desired_size)
#     #if size[0] == 0  or size[1] == 0:
#     #    print("warning size",size)
#     if size[0] > desired_size[0] or size[1] > desired_size[1]:
#         #print("size??",size[0],size[1])
#         ratio_w = float(desired_size[0]) / size[0]
#         ratio_h = float(desired_size[1]) / size[1]
#         ratio = min(ratio_w, ratio_h)
#         new_size = tuple([int(x * ratio) for x in size])
#         image = cv2.resize(image, (new_size[1], new_size[0]))
#         size = image.shape
#
#     delta_w = max(0, desired_size[1] - size[1])
#     delta_h = max(0, desired_size[0] - size[0])
#     # top, bottom = delta_h // 2, delta_h - (delta_h // 2)
#     # left, right = delta_w // 2, delta_w - (delta_w // 2)
#     # top, bottom = 0, delta_h
#     # left, right = 0, delta_w
#     top, bottom = delta_h // 2, delta_h - (delta_h // 2)
#     left, right = 0, delta_w
#
#     color = 255
#     # try:
#     #     color = image[0][0]
#     # except Exception as e:
#     #     print(e)
#
#     # if color < 230:
#     #     color = 230
#     image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=float(color))
#     crop_bb = (left / image.shape[1], top / image.shape[0], (image.shape[1] - right - left) / image.shape[1],
#                (image.shape[0] - bottom - top) / image.shape[0])
#     #image[image > 230] = 255
#     return image, crop_bb
def resize_image_gray(image, desired_size):
    size = image.shape[:2]
    # print('size:', size)
    if size[0] > desired_size[0] or size[1] > desired_size[1]:
        ratio_w = float(desired_size[0]) / size[0]
        ratio_h = float(desired_size[1]) / size[1]
        ratio = min(ratio_w, ratio_h)
        new_size = tuple([int(x * ratio) for x in size])
        image = cv2.resize(image, (new_size[1], new_size[0]))
        size = image.shape

    delta_w = max(0, desired_size[1] - size[1])
    delta_h = max(0, desired_size[0] - size[0])
    # top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    # left, right = delta_w // 2, delta_w - (delta_w // 2)
    # top, bottom = 0, delta_h
    # left, right = 0, delta_w
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = 0, delta_w

    color = 255
    image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=float(color))
    crop_bb = (left / image.shape[1], top / image.shape[0], (image.shape[1] - right - left) / image.shape[1],
               (image.shape[0] - bottom - top) / image.shape[0])
    return image, crop_bb

if __name__ == "__main__":
    # path = "qie_chinese"
    # files = os.listdir(path)
    # for pic in files:
    #     filename = os.path.join(path, pic)
    #     image = cv2.imread(filename, flags=cv2.IMREAD_GRAYSCALE)
    #     image,_ = resize_image_gray(image,(64,800))
    #     cv2.imwrite("./output/" + pic, image)
    filename = "qie_chinese/1731666112.492108_2.jpg"
    #filename = "qie_chinese/test3_9.jpg"
    image = cv2.imread(filename, flags=cv2.IMREAD_GRAYSCALE)
    image, _ = resize_image_gray(image, (64, 800))
    cv2.imwrite("./output/" + pic, image)