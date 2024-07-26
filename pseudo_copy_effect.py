# 作者：张健 Thomas Zhang
# 时间：2024/7/1,15:07
import numpy as np
import cv2


def simulate_copy_effect(image, contrast_factor=1, brightness_delta=-100):
    # Adjust contrast and brightness
    djusted_image = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=brightness_delta)

    # Apply Gaussian blur to smooth the edges
    # blurred_image = cv2.GaussianBlur(adjusted_image, blur_kernel_size, 0)

    # Clip values to ensure they stay within [0, 255] range
    #final_image = np.clip(image, 0, 255).astype(np.uint8)

    return djusted_image


image = cv2.imread("./output/1719674426_1669970.png", cv2.IMREAD_GRAYSCALE)
if image is None:
    print("Error loading image")
    exit()
image = simulate_copy_effect(image, contrast_factor=1, brightness_delta=-100)
cv2.imwrite("./test.jpg", image)
