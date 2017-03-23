import time
import tensorflow as tf
from scipy.misc import imread
from scipy.misc import imresize
from scipy.misc import imsave
import numpy as np

from flask import Flask
from flask import request

from picamera import PiCamera
from time import sleep

import threading

camera = PiCamera()
camera.resolution=(50,50)
camera.framerate=15


logs_path = '/home/pi/tensorflow/logs/'

macc1="192.168.2.4:2222"
macc2="172.17.5.168:2222"
macc3="172.17.100.219:2222"
macc4="172.17.100.200:2222"
macc5="172.17.100.244:2222"

cluster = tf.train.ClusterSpec({"DSGraph":[macc1,macc2,macc3,macc4,macc5]})


mac1="grpc://192.168.2.4:2222"
mac2="grpc://172.17.5.168:2222"
mac3="grpc://172.17.100.219:2222"
mac4="grpc://172.17.100.200:2222"
mac5="grpc://172.17.100.244:2222"
#inputsess=[mac2,mac2,mac2,mac2,mac2,mac2,mac2,mac2,mac2,mac2,mac2,mac2,mac2,mac2,mac2]

#inputsess=[mac1,mac2,mac3,mac1,mac2,mac3,mac1,mac2,mac3,mac1,mac2,mac3,mac1,mac2,mac3]
inputsess=[mac1] #will create the number of input sessions dynamically


Results=''

c1='0'
c2='0'
c3='0'
c4='0'
c5='0'

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return 'hello world'

@app.route('/p1',methods=['GET','POST'])
def p1():
    global inputsess
    #inputsess=[]
    global c1
    global c2
    global c3
    global c4
    global c5
    
    c1=request.args.get("mac1")
    c2=request.args.get("mac2")
    c3=request.args.get("mac3")
    c4=request.args.get("mac4")
    c5=request.args.get("mac5")
    
    print('mac1 is:'+c1)
    print('mac2 is:'+c2)
    print('mac3 is:'+c3)
    print('mac4 is:'+c4)
    print('mac5 is:'+c5)
    #adding mac1 to the inputsess
    if not c1:
        c1='0'
    if not c2:
        c2='0'
    if not c3:
        c3='0'
    if not c4:
        c4='0'
    if not c5:
        c5='0'
    
    #for k in range(int(c1)):
    #    inputsess.extend([mac1])
    #for k in range(int(c2)):
    #    inputsess.extend([mac2])
    #for k in range(int(c3)):
    #    inputsess.extend([mac3])
    #for k in range(int(c4)):
    #    inputsess.extend([mac4])
    #for k in range(int(c5)):
    #    inputsess.extend([mac5])
    
    print('input sess is:'+str(inputsess))
    result='<div align="center">'
    result=result+'<h1>Job Results on Tensorflow Cluster</h1><br><br>'
    result=result+run_p1()
    result=result+'</div>'
    return result

def run_p1():
    global inputsess
    global Results
    
    Results=''
    camera.start_preview()
    #camera.image_effect='negative'
    sleep(5)
    for i in range(1):
     camera.capture('image'+str(i)+'.jpg')
      #sleep(2)
    camera.stop_preview()

    run_pi_time=time.time()
    
    thread=[]
    for i in range(len(inputsess)):
     t=threading.Thread(target=worker,args=(i,))
     thread.append(t)
     t.start()
     t.join()

    Results = Results+'<br><br> Total Time in this Configuration: ' +"%.2f"%(time.time()-run_pi_time) 
    return Results

def worker(i):
 global inputsess
 #thread_time=time.time()
 global Results
 global c1
 global c2
 global c3
 global c4
 global c5
 
 im1 = imread('image'+str(i%5)+'.jpg', mode='L')
 im1 = imresize(im1, (28, 28))
 im1 = im1.reshape((1, 784))
 im1[0] = (im1[0]*1.0 )/max(im1[0]*1.0)* 255.0
 im1 = (255.0-im1)/255.0
 im2 = im1.reshape((28, 28))
 #imsave('processed'+str(i%5)+'.jpg',im2)
 imy1 = [0, 0, 0, 0, 0 ,0, 0, 0, 1, 0]
 imy1 = np.transpose(imy1)
 imy1 = imy1.reshape((1, 10))

 t1=time.time()
 with tf.device("/job:DSGraph/task:"+c1):
  x = tf.placeholder(tf.float32, [None, 784], name="input")
 #Results =Results+'<br>'+'Node1 on '+c1+': Time: '+"%.2f"%(time.time()-t1)
 t1=time.time()
 with tf.device("/job:DSGraph/task:"+c2):
  W = tf.Variable(tf.zeros([784, 10]), name = "w1")
 #Results =Results+'<br>'+'Node1 on '+c1+': Time: '+"%.2f"%(time.time()-t1)
 t1=time.time()
 with tf.device("/job:DSGraph/task:"+c3):
  b = tf.Variable(tf.zeros([10]), name = "b1")
 #Results =Results+'<br>'+'Node1 on '+c1+': Time: '+"%.2f"%(time.time()-t1)
 t1=time.time()
 with tf.device("/job:DSGraph/task:"+c4):
  prob=tf.matmul(x, W) + b
 #Results =Results+'<br>'+'Node1 on '+c1+': Time: '+"%.2f"%(time.time()-t1)
 t1=time.time()
 with tf.device("/job:DSGraph/task:"+c5):
  y = tf.nn.softmax(prob)
 #Results =Results+'<br>'+'Node1 on '+c1+': Time: '+"%.2f"%(time.time()-t1)


 # swd--save the Checkpoint file
 saver = tf.train.Saver()

#with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:

 with tf.Session(inputsess[i]) as sess:
    # swd save ckpt
    saver.restore(sess, "saved_model/model.ckpt")
    print("Model restored.")
    #np.set_printoptions(precision = 2)
    for k in range(10):
     thread_time=time.time()
     result=sess.run(y,feed_dict={x: im1})
     print(result)
     print(str(i+1)+' The number is: '+str(np.argmax(result)))
     Results =Results+'<br>'+str(i+1)+' Machine: '+inputsess[i]+'  Ouput Number:'+str(np.argmax(result))+'  Time: '+"%.2f"%(time.time()-thread_time)
  #print threading.currentThread().getName, 'exiting'
 return

    
if __name__=='__main__':
    app.run(host='0.0.0.0')
