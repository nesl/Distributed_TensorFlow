from numpy import *
import os
import numpy as np
import time
from scipy.misc import imread
from scipy.misc import imresize

prog_begin = time.time()

import tensorflow as tf

from caffe_classes import class_names

train_x = zeros((1, 227,227,3)).astype(float32)
train_y = zeros((1, 1000))
xdim = train_x.shape[1:]
ydim = train_y.shape[1]


################################################################################
#Read Image, and change to BGR BGR BGR!!!

im1 = imread('laska.png', mode='RGB')
im1 = imresize(im1, (227, 227))
im1 = im1 - mean(im1)
im1[:, :, 0], im1[:, :, 2] = im1[:, :, 2], im1[:, :, 0]

#im2 = imread('bird.jpeg', mode='RGB')
#im2 = imresize(im2, (227, 227))
#im2 = im2 - mean(im2)
#im2[:, :, 0], im2[:, :, 2] = im2[:, :, 2], im2[:, :, 0]

################################################################################
#loading network parameters
net_data = load(open("bvlc_alexnet.npy", "rb"), encoding="latin1").item()

def conv(input, kernel, biases, k_h, k_w, c_o, s_h, s_w,  padding="VALID", group=1):
    '''From https://github.com/ethereon/caffe-tensorflow
    '''
    c_i = input.get_shape()[-1]
    assert c_i%group==0
    assert c_o%group==0
    convolve = lambda i, k: tf.nn.conv2d(i, k, [1, s_h, s_w, 1], padding=padding)
    
    
    if group==1:
        conv = convolve(input, kernel)
    else:
        input_groups =  tf.split(input, group, 3)   #tf.split(3, group, input)
        kernel_groups = tf.split(kernel, group, 3)  #tf.split(3, group, kernel) 
        output_groups = [convolve(i, k) for i,k in zip(input_groups, kernel_groups)]
        conv = tf.concat(output_groups, 3)          #tf.concat(3, output_groups)
    return  tf.reshape(tf.nn.bias_add(conv, biases), [-1]+conv.get_shape().as_list()[1:])




################################################################################
#Run network in distributed settings:
#cluster = tf.train.ClusterSpec({"local": ["localhost:2222", "localhost:2223", "localhost:2224"]})
cluster = tf.train.ClusterSpec({"DSGraph":["172.17.5.168:2223","172.17.100.219:2223"]})



x = tf.placeholder(tf.float32, (None,) + xdim)

with tf.device("/job:DSGraph/task:0"):
  #conv1
  #conv(11, 11, 96, 4, 4, padding='VALID', name='conv1')
  k_h = 11; k_w = 11; c_o = 96; s_h = 4; s_w = 4
  conv1W = tf.Variable(net_data["conv1"][0])
  conv1b = tf.Variable(net_data["conv1"][1])
  conv1_in = conv(x, conv1W, conv1b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=1)
  conv1 = tf.nn.relu(conv1_in)

with tf.device("/job:DSGraph/task:0"):
  #lrn1
  #lrn(2, 2e-05, 0.75, name='norm1')
  radius = 2; alpha = 2e-05; beta = 0.75; bias = 1.0
  lrn1 = tf.nn.local_response_normalization(conv1,
                                                    depth_radius=radius,
                                                    alpha=alpha,
                                                    beta=beta,
                                                    bias=bias)

with tf.device("/job:DSGraph/task:0"):
  #maxpool1
  #max_pool(3, 3, 2, 2, padding='VALID', name='pool1')
  k_h = 3; k_w = 3; s_h = 2; s_w = 2; padding = 'VALID'
  maxpool1 = tf.nn.max_pool(lrn1, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)


with tf.device("/job:DSGraph/task:0"):
  #conv2
  #conv(5, 5, 256, 1, 1, group=2, name='conv2')
  k_h = 5; k_w = 5; c_o = 256; s_h = 1; s_w = 1; group = 2
  conv2W = tf.Variable(net_data["conv2"][0])
  conv2b = tf.Variable(net_data["conv2"][1])
  conv2_in = conv(maxpool1, conv2W, conv2b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
  conv2 = tf.nn.relu(conv2_in)


with tf.device("/job:DSGraph/task:0"):
  #lrn2
  #lrn(2, 2e-05, 0.75, name='norm2')
  radius = 2; alpha = 2e-05; beta = 0.75; bias = 1.0
  lrn2 = tf.nn.local_response_normalization(conv2,
                                                    depth_radius=radius,
                                                    alpha=alpha,
                                                    beta=beta,
                                                    bias=bias)
with tf.device("/job:DSGraph/task:0"):
  #maxpool2
  #max_pool(3, 3, 2, 2, padding='VALID', name='pool2')                                                  
  k_h = 3; k_w = 3; s_h = 2; s_w = 2; padding = 'VALID'
  maxpool2 = tf.nn.max_pool(lrn2, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)

with tf.device("/job:DSGraph/task:0"):
  #conv3
  #conv(3, 3, 384, 1, 1, name='conv3')
  k_h = 3; k_w = 3; c_o = 384; s_h = 1; s_w = 1; group = 1
  conv3W = tf.Variable(net_data["conv3"][0])
  conv3b = tf.Variable(net_data["conv3"][1])
  conv3_in = conv(maxpool2, conv3W, conv3b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
  conv3 = tf.nn.relu(conv3_in)

with tf.device("/job:DSGraph/task:0"):
  #conv4
  #conv(3, 3, 384, 1, 1, group=2, name='conv4')
  k_h = 3; k_w = 3; c_o = 384; s_h = 1; s_w = 1; group = 2
  conv4W = tf.Variable(net_data["conv4"][0])
  conv4b = tf.Variable(net_data["conv4"][1])
  conv4_in = conv(conv3, conv4W, conv4b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
  conv4 = tf.nn.relu(conv4_in)


with tf.device("/job:DSGraph/task:0"):
  #conv5
  #conv(3, 3, 256, 1, 1, group=2, name='conv5')
  k_h = 3; k_w = 3; c_o = 256; s_h = 1; s_w = 1; group = 2
  conv5W = tf.Variable(net_data["conv5"][0])
  conv5b = tf.Variable(net_data["conv5"][1])
  conv5_in = conv(conv4, conv5W, conv5b, k_h, k_w, c_o, s_h, s_w, padding="SAME", group=group)
  conv5 = tf.nn.relu(conv5_in)

with tf.device("/job:DSGraph/task:0"):
  #maxpool5
  #max_pool(3, 3, 2, 2, padding='VALID', name='pool5')
  k_h = 3; k_w = 3; s_h = 2; s_w = 2; padding = 'VALID'
  maxpool5 = tf.nn.max_pool(conv5, ksize=[1, k_h, k_w, 1], strides=[1, s_h, s_w, 1], padding=padding)

with tf.device("/job:DSGraph/task:0"):
  #fc6
  #fc(4096, name='fc6')
  fc6W = tf.Variable(net_data["fc6"][0])
  fc6b = tf.Variable(net_data["fc6"][1])
  fc6 = tf.nn.relu_layer(tf.reshape(maxpool5, [-1, int(prod(maxpool5.get_shape()[1:]))]), fc6W, fc6b)

with tf.device("/job:DSGraph/task:0"):
  #fc7
  #fc(4096, name='fc7')
  fc7W = tf.Variable(net_data["fc7"][0])
  fc7b = tf.Variable(net_data["fc7"][1])
  fc7 = tf.nn.relu_layer(fc6, fc7W, fc7b)

with tf.device("/job:DSGraph/task:0"):
  #fc8
  #fc(1000, relu=False, name='fc8')
  fc8W = tf.Variable(net_data["fc8"][0])
  fc8b = tf.Variable(net_data["fc8"][1])
  fc8 = tf.nn.xw_plus_b(fc7, fc8W, fc8b)

with tf.device("/job:DSGraph/task:0"):
  #prob
  #softmax(name='prob'))
  prob = tf.nn.softmax(fc8)


print('\n Network Constructed!\n')

init = tf.global_variables_initializer()

sess = tf.Session("grpc://localhost:2223")
# sess = tf.Session()
sess.run(init)

print('\n Session Initialization Complete!\n')

for i in range(1000):
 t = time.time()
 #output = sess.run(prob, feed_dict = {x:[im1,im2]})
 output = sess.run(prob, feed_dict = {x:[im1]})
 print('\n1st Time Session running time: '+str(time.time()-t)+ ' seconds\n')

 t2 = time.time()
 #output = sess.run(prob, feed_dict = {x:[im1,im2]})
 output = sess.run(prob, feed_dict = {x:[im1]})
 print('\n2nd Time Session running time: '+str(time.time()-t2)+ ' seconds\n')
################################################################################

# print(x)
# print(conv1)
# print(maxpool1)
# print(conv2)
# print(maxpool2)
# print(conv3)
# print(conv4)
# print(conv5)
# print(maxpool5)
# print(fc6)
# print(fc7)
# print(fc8)
# print(prob)

#Output:

for input_im_ind in range(output.shape[0]):
    inds = argsort(output)[input_im_ind,:]
    print("\nInput Image: "+ str(input_im_ind))
    for i in range(5):
        print(class_names[inds[-1-i]], output[input_im_ind, inds[-1-i]])

print(time.time()-t)


print('===========================================================================')
print('Program running time: '+str(time.time()-prog_begin)+ ' seconds\n')
# about 999? s for total
# about  1.875 1.034   for single execution
