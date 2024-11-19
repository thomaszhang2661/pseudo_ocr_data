from PIL import Image
import numpy as np
filepath= "test.png"
image = Image.open(filepath).convert('L')
image = np.array(image)# 转为灰度图
print(image)