import time
import tensorflow as tf
from scipy.misc import imread
from scipy.misc import imresize
import numpy as np
start=time.time()


file_name = '8.png'
image_contents = tf.read_file(file_name)
image = tf.image.decode_image(image_contents, channels=1)
# problem here: why the result of decode image has no "shape"?
image = tf.image.resize_image_with_crop_or_pad(image, 250, 250)
image.set_shape([250, 250, 1])

# alternative : native method for TF
# sess = tf.Session()
# img2 = tf.constant(sess.run(image))
# sess.close()

# alternative: using scipy
# image = imread('0.jpg', mode='L')
# img = tf.constant(image)
# img2 = tf.expand_dims(img, -1)

img_resize = tf.image.resize_images(image, [28,28])

img_max = tf.reduce_max(img_resize)
img_min = tf.reduce_min(img_resize)

std_img = tf.div( tf.subtract( img_resize, img_min), tf.subtract(img_max, img_min) )
bin_img = tf.ceil( tf.subtract(std_img, 0.7) )
inv_img = tf.abs( tf.subtract(bin_img, 1) )
input_img = tf.reshape(inv_img, [1, 784])


# image = imread('0.jpg', mode='L')
# image = imresize(image, (28, 28))
# # image normalization 0-1 value
# img = image.reshape((1, 784))
# img_max = max(img[0])
# img_min = min(img[0])
# img = (img*1.0 - img_min )/(img_max - img_min)* 255.0
# img = (255.0-img)/255.0
# # binarization
# for i in range(784):
#     if img[0][i]<=0.5:
#         img[0][i]=0


x = tf.placeholder(tf.float32, [None, 784], name="input")
W = tf.Variable(tf.zeros([784, 10]), name = "w1")
b = tf.Variable(tf.zeros([10]), name = "b1")
y = tf.nn.softmax(tf.matmul(x, W) + b)

# swd--save the Checkpoint file
saver = tf.train.Saver()
with tf.Session() as sess:
    # swd save ckpt
    saver.restore(sess, "saved_model/model.ckpt")
    print("Model restored.")
    np.set_printoptions(precision = 2)
    # result=sess.run(y,feed_dict={x: img})
    result=sess.run(y,  feed_dict={x: input_img.eval()})
    print(result)
    print('The number is: '+str(np.argmax(result)))
    
end=time.time()
print ("Computing time: "+str(end-start)+" seconds")


# using TF(scipy input), about 0.048 - 0.05 seconds
# using TF(all), about 0.068 - 0.071 seconds
# using scipy, about 0.036 - 0.038 seconds

# using TF(all, set shape), about 0.10 - 0.11 seconds