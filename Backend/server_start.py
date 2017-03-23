import sys
task_number=int(sys.argv[1])
import tensorflow as tf

#cluster = tf.train.ClusterSpec({"DSGraph":["172.17.5.168:2222","localhost:2222","172.17.100.200:2222","172.17.100.244:2222"]})
#cluster = tf.train.ClusterSpec({"DSGraph":["localhost:2222","172.17.5.168:2222"]})

macc1="192.168.2.4:2222"
macc2="172.17.5.168:2222"
macc3="172.17.100.219:2222"
macc4="172.17.100.200:2222"
macc5="172.17.100.244:2222"

cluster = tf.train.ClusterSpec({"DSGraph":[macc1,macc2,macc3,macc4,macc5]})
server = tf.train.Server(cluster, job_name="DSGraph", task_index=task_number)

print("Server starting #{}".format(task_number))

server.start()
server.join()

