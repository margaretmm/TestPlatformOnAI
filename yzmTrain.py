#!/usr/bin/env python
# -*- coding: utf-8 -*-


#----------------------------------------------------
# Purpose:    train for captcha recognition
#
# Author:      puxinhe
# Created:     09-27-2018
# Copyright:   (c) Hikvision.com 2018

#---------------------------------------------------


import os
import random
import time

import tensorflow as tf
import numpy as np
from PIL import Image


# 验证码图片的宽度
CAPTCHA_IMAGE_WIDHT = 100
# 验证码图片的高度
CAPTCHA_IMAGE_HEIGHT = 45
# 字符集合长度 26char+10 num
#CHAR_SET_LEN = 36
CHAR_SET_LEN = 52
# 验证码字符长度
CAPTCHA_LEN = 4

# 60%的验证码图片放入训练集中
TRAIN_IMAGE_PERCENT = 0.6
# 训练集，用于训练的验证码图片的文件名
TRAINING_IMAGE_NAME = []
# 验证集，用于模型验证的验证码图片的文件名
VALIDATION_IMAGE_NAME = []

# 验证码图片的存放路径
CAPTCHA_IMAGE_PATH = './image/'
# 存放训练好的模型的路径
MODEL_SAVE_PATH = './models/'


def _get_image_file_name(img_path=CAPTCHA_IMAGE_PATH):
    '''获取验证码图片名称和数量'''
    file_name = []
    total = 0
    for file_path in os.listdir(img_path):
        captcha_name = file_path.split('/')[-1]
        file_name.append(captcha_name)
        total += 1
    return file_name, total


def _name2label(name):
    '''将验证码转换为训练时用的标签向量，维数是CAPTCHA_LEN * CHAR_SET_LEN '''
    label = np.zeros(CAPTCHA_LEN * CHAR_SET_LEN)
    for i, c in enumerate(name):
    #    print("!!!!!!!!!!!!",i,c)
        idx = i*CHAR_SET_LEN + _char2index2(c)
        label[idx] = 1
    return label


def _char2index(c):
    '''字符转换为指针'''
    k = ord(c)
    index = -1
    if k >= 48 and k <= 57:  # 数字索引
        index = k - 48
    if k >= 65 and k <= 90:  # 大写字母索引
        index = k - 55
    if k >= 97 and k <= 122:  # 小写字母索引
        index = k - 61
    if index == -1:
        raise ValueError('No Map')
    return index

def _char2index2(c):
    '''字符转换为指针'''
    k = ord(c)
    index = -1
    if k >= 65 and k <= 90:  # 大写字母索引
        index = k - 65
    if k >= 97 and k <= 122:  # 小写字母索引
        index = k - 71 #-97+26
    if index == -1:
        raise ValueError('No Map')
    return index


def _get_next_batch(batchsize=32, train_or_test='train', step=0):
    '''生成一个训练batch数据'''
    batch_data = np.zeros([batchsize, CAPTCHA_IMAGE_WIDHT * CAPTCHA_IMAGE_HEIGHT])
    batch_label = np.zeros([batchsize, CAPTCHA_LEN * CHAR_SET_LEN])
    file_name_list = TRAINING_IMAGE_NAME
    if train_or_test == 'validate':
        file_name_list = VALIDATION_IMAGE_NAME
    total_number = len(file_name_list)
    index_start = step * batchsize
    for i in range(batchsize):
        index = (i + index_start) % total_number
        name = file_name_list[index]
        img_data, img_label = _get_data_and_label(name)
        batch_data[i, :] = img_data
        batch_label[i, :] = img_label
    return batch_data, batch_label


def _get_data_and_label(file_name, file_path=CAPTCHA_IMAGE_PATH):
    '''取得验证码图片的数据以及它的标签'''
    path_name = os.path.join(file_path, file_name)
    img = Image.open(path_name)
    #转为灰度图
    img = img.convert("L")
    image_array = np.array(img)
    image_data = image_array.flatten()/255
    image_label = _name2label(file_name[0:CAPTCHA_LEN])
    #image_label = file_name[0:CAPTCHA_LEN]
    return image_data, image_label


def train_data_with_CNN():
    '''构建卷积神经网络并训练'''

    def weight_variable(shape, name='weight'):
        '''初始化权值'''
        init = tf.truncated_normal(shape, stddev=0.1)
        var = tf.Variable(initial_value=init, name=name)
        return var


    def bias_variable(shape, name='bias'):
        '''初始化偏置'''
        init = tf.constant(0.1, shape=shape)
        var = tf.Variable(init, name=name)
        return var


    def conv2d(x, W, name='conv2d'):
        '''卷积'''
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME', name=name)


    def max_pool_2X2(x, name='maxpool'):
        ''' 池化 '''
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name=name)


    # 输入层,请注意 X 的 name，在测试model时会用到它
    X = tf.placeholder(tf.float32, [None, CAPTCHA_IMAGE_WIDHT * CAPTCHA_IMAGE_HEIGHT], name='data-input')
    Y = tf.placeholder(tf.float32, [None, CAPTCHA_LEN * CHAR_SET_LEN], name='label-input')
    x_input = tf.reshape(X, [-1, CAPTCHA_IMAGE_HEIGHT, CAPTCHA_IMAGE_WIDHT, 1], name='x-input')

    # dropout,防止过拟合,请注意 keep_prob 的 name，在测试model时会用到它
    keep_prob = tf.placeholder(tf.float32, name='keep-prob')

    # 第一层卷积
    W_conv1 = weight_variable([3, 3, 1, 32], 'W_conv1')
    B_conv1 = bias_variable([32], 'B_conv1')
    conv1 = tf.nn.relu(conv2d(x_input, W_conv1, 'conv1') + B_conv1)
    conv1 = max_pool_2X2(conv1, 'conv1-pool')
    conv1 = tf.nn.dropout(conv1, keep_prob)

    # 第二层卷积
    W_conv2 = weight_variable([3, 3, 32, 64], 'W_conv2')
    B_conv2 = bias_variable([64], 'B_conv2')
    conv2 = tf.nn.relu(conv2d(conv1, W_conv2, 'conv2') + B_conv2)
    conv2 = max_pool_2X2(conv2, 'conv2-pool')
    conv2 = tf.nn.dropout(conv2, keep_prob)

    # 第三层卷积
    W_conv3 = weight_variable([3, 3, 64, 64], 'W_conv3')
    B_conv3 = bias_variable([64], 'B_conv3')
    conv3 = tf.nn.relu(conv2d(conv2, W_conv3, 'conv3') + B_conv3)
    conv3 = max_pool_2X2(conv3, 'conv3-pool')
    conv3 = tf.nn.dropout(conv3, keep_prob)

    # 全链接层
    # 每次池化后，图片的宽度和高度均缩小为原来的一半，进过上面的三次池化，宽度和高度均缩小8倍
    # 如图片大小改变，W_fc前两位应该改为weight/8,hight/8向上取整
    W_fc1 = weight_variable([13 * 6   * 64, 1024], 'W_fc1')
    B_fc1 = bias_variable([1024], 'B_fc1')
    fc1 = tf.reshape(conv3, [-1, W_fc1.get_shape().as_list()[0]])
    fc1 = tf.nn.relu(tf.add(tf.matmul(fc1, W_fc1), B_fc1))
    fc1 = tf.nn.dropout(fc1, keep_prob)
    # 输出层
    W_fc2 = weight_variable([1024, CAPTCHA_LEN * CHAR_SET_LEN], 'W_fc2')
    B_fc2 = bias_variable([CAPTCHA_LEN * CHAR_SET_LEN], 'B_fc2')
    output = tf.add(tf.matmul(fc1, W_fc2), B_fc2, 'output')
    #loss,优化器
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=Y, logits=output))
    optimizer = tf.train.AdamOptimizer(0.001).minimize(loss)
    #预测与标签
    predict = tf.reshape(output, [-1, CAPTCHA_LEN, CHAR_SET_LEN], name='predict')
    labels = tf.reshape(Y, [-1, CAPTCHA_LEN, CHAR_SET_LEN], name='labels')
    # 预测结果
    # 请注意 predict_max_idx 的 name，在测试model时会用到它
    predict_max_idx = tf.argmax(predict, axis=2, name='predict_max_idx')
    labels_max_idx = tf.argmax(labels, axis=2, name='labels_max_idx')
    predict_correct_vec = tf.equal(predict_max_idx, labels_max_idx)
    accuracy = tf.reduce_mean(tf.cast(predict_correct_vec, tf.float32))
    #保存模型
    saver = tf.train.Saver()
    config = tf.ConfigProto(allow_soft_placement=True,log_device_placement=True)
    config.gpu_options.per_process_gpu_memory_fraction = 0.6
    #运行
    with tf.Session(config=config) as sess:
        sess.run(tf.global_variables_initializer())
        steps = 0
        for epoch in range(6000):
            train_data, train_label = _get_next_batch(64, 'train', steps)
            op,pre = sess.run([optimizer,labels_max_idx], feed_dict={X: train_data, Y: train_label, keep_prob: 0.75})

            if steps % 1 == 0:
                test_data, test_label = _get_next_batch(100, 'validate', steps)
                acc = sess.run(accuracy, feed_dict={X: test_data, Y: test_label, keep_prob: 1.0})
                print("steps=%d, accuracy=%f" % (steps, acc))
                if acc > 0.99:
                    saver.save(sess, MODEL_SAVE_PATH + "crack_captcha.model", global_step=steps)
                    break
            if steps > 4000:
                if steps % 500 == 0:
                    saver.save(sess, MODEL_SAVE_PATH + "crack_captcha.model", global_step=steps)
            steps += 1


if __name__ == '__main__':
    image_file_name_list, total = _get_image_file_name(CAPTCHA_IMAGE_PATH)
    random.seed(time.time())
    # 随机顺序
    random.shuffle(image_file_name_list)
    #训练集数目
    trainImageNumber = int(total * TRAIN_IMAGE_PERCENT)
    # 分成测试集
    TRAINING_IMAGE_NAME = image_file_name_list[: trainImageNumber]
    # 和验证集
    VALIDATION_IMAGE_NAME = image_file_name_list[trainImageNumber:]
    train_data_with_CNN()
    print('Training finished')






