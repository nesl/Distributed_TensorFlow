from tensorflow.examples.tutorials.mnist import input_data

import time
import tensorflow as tf
from scipy.misc import imread
from scipy.misc import imresize
from scipy.misc import imsave
import numpy as np
start=time.time()

from picamera import PiCamera
from time import sleep

import threading

camera = PiCamera()
camera.resolution=(50,50)
camera.framerate=15
camera.start_preview()
#camera.image_effect='negative'
#sleep(3)
for i in range(5):
  camera.capture('image'+str(i)+'.jpg')
  #sleep(2)
camera.stop_preview()

macc1="192.168.2.4:2222"
macc2="172.17.5.168:2222"
cluster = tf.train.ClusterSpec({"DSGraph":[macc1,macc2]})


mac1="grpc://192.168.2.4:2222"
mac2="grpc://172.17.5.168:2222"
inputsess=[mac1,mac2,mac1,mac2,mac1]

#for i in range(5):
def worker(i):
 #print threading.currentThread().getName, 'starting'
 im1 = imread('image'+str(i)+'.jpg', mode='L')
 im1 = imresize(im1, (28, 28))
 im1 = im1.reshape((1, 784))
 im1[0] = (im1[0]*1.0 )/max(im1[0]*1.0)* 255.0
 im1 = (255.0-im1)/255.0
 im2 = im1.reshape((28, 28))
 imsave('processed'+str(i)+'.jpg',im2)
 imy1 = [0, 0, 0, 0, 0 ,0, 0, 0, 1, 0]
 imy1 = np.transpose(imy1)
 imy1 = imy1.reshape((1, 10))
 x = tf.placeholder(tf.float32, [None, 784], name="input")
 W = tf.Variable(tf.zeros([784, 10]), name = "w1")
 b = tf.Variable(tf.zeros([10]), name = "b1")

 prob=tf.matmul(x, W) + b
 
 y = tf.nn.softmax(prob)

 # swd--save the Checkpoint file
 saver = tf.train.Saver()

#with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
 with tf.Session(inputsess[i%5]) as sess:
    # swd save ckpt
    saver.restore(sess, "saved_model/model.ckpt")
    print("Model restored.")
    
 with tf.Session(inputsess[i]) as sess:    
    np.set_printoptions(precision = 2)
    result=sess.run(y,feed_dict={x: im1})
    print(result)
    print('The number is: '+str(np.argmax(result)))
  #print threading.currentThread().getName, 'exiting'
 return

thread=[]
for i in range(5):
 t=threading.Thread(target=worker,args=(i,))
 thread.append(t)
 t.start()

