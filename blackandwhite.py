from tkinter.filedialog import *
import requests
import json
from tkinter import filedialog
import cv2
from urllib import request
import numpy as np

def colorizer_caffe(num, image, fln):
    if num == 1:
        new_img = colorizer_caffe_1(image)
        return new_img

def colorizer_caffe_1(image):
    print("loading models.....")
    #caffemodel: It is a pre-trained model stored in the Caffe framework’s format that can be used to predict new unseen data.
    #prototext: It consists of different parameters that define the network and it also helps in deploying the Caffe model.
    net = cv2.dnn.readNetFromCaffe('Models/colorization_deploy_v2.prototxt','Models/colorization_release_v2.caffemodel')
    #It is a NumPy file that stores the cluster center points in NumPy format. It consists of 313 cluster kernels, i.e (0-312).
    pts = np.load('Models/pts_in_hull.npy')

    #getLayerId: returns the id of the layer, or -1 if the layer wasn't found.
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    #it converts points to 1*1 convolutions and feed them to the model.
    pts = pts.transpose().reshape(2,313,1,1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1,313],2.606,dtype='float32')]


    #Scaling pixel intensities to the range [0, 1].
    scaled = image.astype("float32")/255.0
    lab = cv2.cvtColor(scaled,cv2.COLOR_BGR2LAB)


    resized = cv2.resize(lab,(224,224))
    #Then we grab the L channel only and perform mean subtraction
    L = cv2.split(resized)[0]
    L -= 50

    #predicting the ab component by giving the L channel of input image.
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1,2,0))

    ab = cv2.resize(ab, (image.shape[1],image.shape[0]))

    #combining the L and predicted ab channels.
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:,:,np.newaxis], ab), axis=2)

    #conversion from LAB to BGR
    colorized = cv2.cvtColor(colorized,cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized,0,1)

    #bringing the pixel intensities back into the range [0, 255]
    colorized = (255 * colorized).astype("uint8")
    return colorized