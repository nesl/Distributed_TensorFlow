# python soft_worker.py 0
# python worker.py 1

# Get task number from command line
import sys
task_number = int(sys.argv[1])

import tensorflow as tf

#cluster = tf.train.ClusterSpec({"local": ["172.17.5.8:2222", "172.17.5.98:2223"]})
cluster = tf.train.ClusterSpec({"local": ["localhost:2222", "localhost:2223", "localhost:2224"]})
server = tf.train.Server(cluster, job_name="local", task_index=task_number)

print("Starting server #{}".format(task_number))

server.start()
server.join()
