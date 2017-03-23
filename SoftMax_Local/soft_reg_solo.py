from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import time
import tensorflow as tf

start=time.time()

x = tf.placeholder(tf.float32, [None, 784])

W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

time1=time.time()
print ("Time1: "+str(time1-start)+" seconds")

y = tf.nn.softmax(tf.matmul(x, W) + b)

y_ = tf.placeholder(tf.float32, [None, 10])

time2=time.time()
print ("Time2: "+str(time2-time1)+" seconds")

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

time3=time.time()
print ("Time3: "+str(time3-time2)+" seconds")

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

for _ in range(10000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})


time4=time.time()
print ("Time4: "+str(time4-time3)+" seconds")

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

time5=time.time()
print ("Time5: "+str(time5-time4)+" seconds")

end=time.time()
print ("Computing time: "+str(end-start)+" seconds")
