# coding: UTF-8
import platform

MODEL_FILE_new='trained.pb'
GraphDef_new='GraphDef.txt'
MODEL_FILE_new2='trained2.pb'
GraphDef_new2='GraphDef2.txt'
MODEL_FILE_ori='classify_image_graph_def.pb'
MODEL_FILE_ori2='tensorflow_inception_graph.pb'
IMG_EXTENSIONS = ['png','PNG','jpg', 'jepg', 'JPG', 'JPEG']

if platform.system() in ['Linux']:
    # 下载的谷歌训练好的Inception-v3模型文件目录
    MODEL_DIR = 'model/'
    MODEL_DIR2 = 'model2/'
    TRAINED_MODEL_DIR='modelTrained/'
    # 因为一个训练数据会被使用多次，所以可以将原始图像通过Inception-v3模型计算得到的特征向量保存在文件中，免去重复的计算。
    # 下载的谷歌训练好的Inception-v3模型文件目录
    CACHE_DIR = 'bottleneck/'
    # 在这个文件夹中每一个子文件夹代表一个需要区分的类别，每个子文件夹中存放了对应类别的图片。
    INPUT_DATA='data/train/'
    TEST_IMG='data/test/'
    GRAPHDIR = './'
else:
    MODEL_DIR = 'D:\\05_PycharmProjects\\test\\inceptionV3\\model\\'
    MODEL_DIR2 = 'D:\\05_PycharmProjects\\test\\inceptionV3\\model2\\'
    TRAINED_MODEL_DIR='D:\\05_PycharmProjects\\test\\inceptionV3\\modelTrained\\'
    # 下面的变量定义了这些文件的存放地址。
    CACHE_DIR = 'D:\\05_PycharmProjects\\test\\inceptionV3\\bottleneck\\'
    INPUT_DATA = 'D:\\05_PycharmProjects\\test\\inceptionV3\\data\\train\\'
    TEST_IMG = 'D:\\05_PycharmProjects\\test\\inceptionV3\\data\\test\\'
    GRAPHDIR='D:\\05_PycharmProjects\\test\\inceptionV3\\'
