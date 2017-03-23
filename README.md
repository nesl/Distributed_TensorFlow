# Distributed_TensorFlow
This repository contains the code used to set up distributed TensorFlow cluster for the course project CSM213B.

## There are 4 folders the details of which are explained as below:

* Alex

* Backend

* FrontEnd

* SoftMax_Local

## 1. Alex

## 2. Backend
The backend server is developed using Flask in Python. The backend listend to the connections from the front end and process the request.
The code of the backend is present in Backend folder.
###  Installation
1. The cluster on raspberry pi devices is set up by following the procedure described [here](https://github.com/samjabrahams/tensorflow-on-raspberry-pi).
2. The flask installation is described in detail [here](http://flask.pocoo.org/docs/0.12/tutorial/).
3. Installing distributed TensorFlow on multiple machines is explained on the official page [here](https://www.tensorflow.org/deploy/distributed).
4. First add the cluster details in the server file, and then start the server process on each device of cluster as explained in the official documentation given in 3.
5. Now you can start the flask basked backend server to listen to the incoming connections.

## 3. FrontEnd
The frontend is developed using the Javascript. The server is hosted using the apache tomcat and is deveoped in eclipse.
###  Installation
The eclipse for web development can be downloaded from the [link](http://www.eclipse.org/downloads/packages/eclipse-ide-javascript-web-developers/indigosr2)

## 4. SoftMax_Local
This folder contains the local implementation the softmax in python.
