1. generate_printed_number_sample.py 是生成数字码图片的文件,这些生成的图片作为输入可训练ocr模型
2. xuehao_add_frame.py 是手写学号识别对原有图片数据加框扩展的代码 输出保存在 ../pseudo_ocr_data_xuehao/framed_xuehao
   ../pseudo_ocr_data_xuehao/data_train 是手写学号识别之前的标注文件，已经检查过一遍可以进行加框扩展
3. pseudo_hwr_xuehao.py 是根据MINIST数据集生成手写学号的伪数据。
    ../pseudo_ocr_data_xuehao/mnist_images_checked 是人工检查后的MINIST数据集
    .。/pseudo_ocr_data_xuehao/gen_mnist_data 是生成的手写伪数据
4. check_MNIST_data.py 是数据格式转换，将原有格式转换成方便人观察的图片。
