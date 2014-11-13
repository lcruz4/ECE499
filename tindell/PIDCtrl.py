import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np
import controller_def as ctrl
import AngVelChan as angle
import LRValChan as LRVAL


ai = ach.Channel(angle.CONTROLLER_REF_NAME)
ai.flush()
a = angle.CONTROLLER_REF()
LRi = ach.Channel(LRVAL.CONTROLLER_REF_NAME)
LRi.flush()
LR = LRVAL.CONTROLLER_REF()
LRi.put(LR)

kp=1
ki=0
kd=0

while(1):
	[statuss, framesizes] = ai.get(a, wait=False, last=False)
	print(a.AngVel)
	if a.AngVel==-2:
		a.AnVel=0
	elif a.AngVel>1:
		a.AngVel=1
	elif a.AngVel<-1:
		a.AngVel=-1
	LR.Left=a.AngVel*kp
	LR.Right=-a.AngVel*kp
	LRi.put(LR)
	
	