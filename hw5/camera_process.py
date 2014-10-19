import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

dd= diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN = 'robot-diff-drive'
ROBOT_CHAN_VIEW = 'robot-vid-chan'
ROBOT_TIME_CHAN = 'robot-time'

cv.NamedWindow("wctrl", cv.CV_WINDOW_AUTOSIZE)

newx = 320
newy = 240

nx = 640
ny = 480

r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
v = ach.Channel(ROBOT_CHAN_VIEW)
v.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()

while True:
  img = np.zeros((newx,newy,3), np.uint8)
  c_image = img.copy()
  vid = cv2.resize(c_image,(newx,newy))
  [status, framesize] = v.get(vid, wait=False, last=True)
  if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
    vid2 = cv2.resize(vid,(nx,ny))
    img = cv2.cvtColor(vid2,cv2.COLOR_BGR2RGB)
    cv2.waitKey(10)
  else:
    raise ach.AchException(v.result_string(status))

  [status, framesize] = t.get(tim, wait=False, last=True)
  if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
    pass
  else:
    raise ach.AchException(v.result_string(status))

  rImg, gImg, Bimg = cv2.split(img)
  ret, gThresh = cv2.threshold(gImg, 100, 1, cv2.THRESH_BINARY)
  ret, rThresh = cv2.threshold(rImg, 100, 1, cv2.THRESH_BINARY_INV)
  mask = gThresh & rThresh
  gCount = 0
  xTot = 0
  for i in range(mask[200].size):
    xTot += i*mask[200][i]
    gCount += 1*mask[200][i]
    i += 1
  if(gCount):
    print(xTot/gCount,200)
    img[200][xTot/gCount]= [0,0,0xFF]
    img[200][xTot/gCount+1]= [0,0,0xFF]
    img[200][xTot/gCount-1]= [0,0,0xFF]
    img[201][xTot/gCount]= [0,0,0xFF]
    img[199][xTot/gCount]= [0,0,0xFF]
    img[201][xTot/gCount+1]= [0,0,0xFF]
    img[201][xTot/gCount-1]= [0,0,0xFF]
    img[199][xTot/gCount+1]= [0,0,0xFF]
    img[199][xTot/gCount-1]= [0,0,0xFF]
  cv2.imshow("wctrl", img)
  time.sleep(0.1)
