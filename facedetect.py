#)!/usr/bin/env python

import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

import AngVelChan as angle

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3,
            minNeighbors=2, minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

cascade_fn = "haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_fn)

cam = cv2.VideoCapture()
cam.open(0)

cv.NamedWindow("img", cv.CV_WINDOW_AUTOSIZE)

a = ach.Channel(angle.CONTROLLER_REF_NAME)
a.flush()
angvel = angle.CONTROLLER_REF()

a.put(angvel)

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    dimx = img.shape[1]/2
    dimy = img.shape[0]/2

    rects = detect(gray, cascade)
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255), 2)
    if(rects == []):
        x = dimx
        y = dimy
    else:
        x = (x1+x2)/2
        y = (y1+y2)/2
    x = float(x-dimx)/dimx
    y = float(dimy-y)/dimy
    print x,y
    angvel.X=x
    angvel.Y=y
    a.put(angvel)

    cv2.imshow('facedetect', img)

    if 0xFF & cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()
