import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

cv.NamedWindow("name", cv.CV_WINDOW_AUTOSIZE)
capture  = cv2.VideoCapture()
capture.open(0)

newx = 320
newy = 240

nx = 640
ny = 480

while True:#Dr. Lofaro's code for getting video feed to a matrix var
  img = np.zeros((newx,newy,3), np.uint8)
  ret, img = capture.read()

  height, width = img.shape[:2]
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  h,s,v =np.mean(np.mean(hsv[50:70,140:160],axis=0),axis=0)
  upper_white = np.array([272,s+10,v+10], dtype=np.uint8)
  lower_white = np.array([160,s-10,v-10], dtype=np.uint8)
  mask = cv2.inRange(hsv, lower_white, upper_white)
  mom = cv2.moments(mask, True)
  print(np.mean(np.mean(hsv[50:70,140:160],axis=1),axis=0))
#  print(hsv[8:18,158:168])
  if(mom['m00']!=0):
    xf = int(mom['m10']/mom['m00'])
    yf = int(mom['m01']/mom['m00'])
#    cv2.circle(img,(8,158), 1, (255,0,255),-1)
#    cv2.circle(img,(18,158), 1, (255,0,255),-1)
#    cv2.circle(img,(8,168), 1, (255,0,255),-1)
#    cv2.circle(img,(18,168), 1, (255,0,255),-1)
    cv2.circle(img,(50,140), 1, (255,0,255),-1)
    cv2.circle(img,(70,140), 1, (255,0,255),-1)
    cv2.circle(img,(50,160), 1, (255,0,255),-1)
    cv2.circle(img,(70,160), 1, (255,0,255),-1)
    cv2.circle(img,(xf,yf), 5, (255,50,255),-1)
    print(xf,yf)
  cv2.imshow("hsv", hsv)
  cv2.imshow("mask", mask)
  cv2.imshow("name", img)
  cv2.waitKey(10)
  time.sleep(1)
