from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import time
import tensorflow as tf

start=time.time()

cluster = tf.train.ClusterSpec({"local": ["localhost:2222", "localhost:2223", "localhost:2224"]})


x = tf.placeholder(tf.float32, [None, 784])

with tf.device("/job:local/task:0"):
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))

time1=time.time()
print ("Time1: "+str(time1-start)+" seconds")


with tf.device("/job:local/task:1"):
    y = tf.nn.softmax(tf.matmul(x, W) + b)
    y_ = tf.placeholder(tf.float32, [None, 10])

time2=time.time()
print ("Time2: "+str(time2-time1)+" seconds")

with tf.device("/job:local/task:2"):
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
#    sess = tf.InteractiveSession()
#    tf.global_variables_initializer().run()
    #init_op = tf.initialize_all_variables()
    #print("Variables initialized ...")


time3=time.time()
print ("Time3: "+str(time3-time2)+" seconds")

with tf.Session("grpc://localhost:2224", config=tf.ConfigProto(log_device_placement=True)) as sess:
#with tf.Session("grpc://localhost:2224") as sess:
    tf.global_variables_initializer().run()
    for _ in range(1000):
      batch_xs, batch_ys = mnist.train.next_batch(100)
      sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))


time4=time.time()
print ("Time4: "+str(time4-time3)+" seconds")


end=time.time()
print ("Computing time: "+str(end-start)+" seconds")





