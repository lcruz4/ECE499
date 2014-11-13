
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

import AngVelChan as angle



capture = cv2.VideoCapture()
capture.open(1)


cv.NamedWindow("frame", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("thresh2", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("img", cv.CV_WINDOW_AUTOSIZE)


newx = 320
newy = 240

nx = 640
ny = 480


a = ach.Channel(angle.CONTROLLER_REF_NAME)
a.flush()
angvel = angle.CONTROLLER_REF()

a.put(angvel)

def GetColorCenter(image,color):
	hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
	upper=lower=0
	if color == 'yellow':
		lower = np.array([10,80,160],np.uint8)
		upper = np.array([40,255,200],np.uint8)
	elif color=='blue':
		lower = np.array([110,50,50],np.uint8)
		upper = np.array([130,255,255],np.uint8)
	elif color=='red':
		lower = np.array([0,50,50],np.uint8)
		upper = np.array([50,255,255],np.uint8)
	else:
		lower = np.array([33,120,0],np.uint8)
		upper = np.array([42,187,255],np.uint8)

	thresh = cv2.inRange(hsv,lower, upper)
	thresh2 = thresh.copy()
	try:
		M=cv2.moments(thresh,True)
		cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
		cv2.circle(img,(cx,cy),5,(255,0,255),-1)
	except:
		cx=cy=-1
		print ("exception")
	cv2.imshow('thresh2',thresh2)
	return [cx,cy]
COLOR="yellow"
FrameAmount=0
while True:
	img = np.zeros((newx,newy,3), np.uint8)
	ret, img = capture.read()
	c_image = img.copy()
	vid = cv2.resize(c_image,(newx,newy))

	vid2 = cv2.resize(vid,(nx,ny))
	#img = cv2.cvtColor(vid2,cv2.COLOR_BGR2RGB)

	frame = cv2.blur(img,(3,3))
	
	loc=GetColorCenter(frame,COLOR)
	print loc
	x=float(loc[0])
	x=float(x-newx/2)/newx
	y=float(loc[1])
	y=(y-newy/2)/newy
        print(x,y)
	angvel.X=x
	angvel.Y=y
	a.put(angvel)
	
		
	cv2.imshow("img",img)
	

	cv2.waitKey(10)

	time.sleep(0.1)
