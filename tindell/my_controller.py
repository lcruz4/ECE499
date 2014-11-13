
import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np
import pygame
import actuator_sim as ser
#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------

# Add imports here

import controller_def as ctrl

import LRValChan as LRVAL
#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW   = 'robot-vid-chan'
ROBOT_TIME_CHAN  = 'robot-time'
# CV setup 
r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()
LR = ach.Channel(LRVAL.CONTROLLER_REF_NAME)
LR.flush()


print '======================================'
print '============ My Controller ==========='
print '=========== Robert Tindell ==========='
print '========== rtindel2@gmu.edu =========='
print '======================================'

periodTime=0.0
timetochange=0.0
#State0 is rotate clockwise, State1 is rotate counterclockwise, State2 is move in square
controller = LRVAL.CONTROLLER_REF()
while True:
    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
	pass
	#print 'Sim Time = ', tim.sim[0]
    else:
	raise ach.AchException( v.result_string(status) )

#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------
    # Main Loop
    # Def:
    # tim.sim[0] = Sim Time
    #Will Update every 0.05 seconds(20 hz) SimTime
    
    while(periodTime-tim.sim[0]>0):
	[status, framesize] = t.get(tim, wait=False, last=True)
    else:
	#use the key controller to set the wheels
	[statuss, framesizes] = LR.get(controller, wait=False, last=False)
	ctrl.rightWheel(r,ref,controller.Right)
	ctrl.leftWheel(r,ref,controller.Left)

	print str(ref.ref[1])

	periodTime=tim.sim[0]+0.05

#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------