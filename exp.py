import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW   = 'robot-vid-chan'#video feed channel
ROBOT_TIME_CHAN  = 'robot-time'
cv.NamedWindow("wctrl", cv.CV_WINDOW_AUTOSIZE)

newx = 320
newy = 240

nx = 640
ny = 480

r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
v = ach.Channel(ROBOT_CHAN_VIEW)#open video feed channel
v.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()

f = open('data.csv', 'w')#file for writing error values

while True:#Dr. Lofaro's code for getting video feed to a matrix var
    img = np.zeros((newx,newy,3), np.uint8)
    c_image = img.copy()
    vid = cv2.resize(c_image,(newx,newy))
    [status, framesize] = v.get(vid, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        vid2 = cv2.resize(vid,(nx,ny))
        img = cv2.cvtColor(vid2,cv2.COLOR_BGR2RGB)
        cv2.waitKey(10)
    else:
        raise ach.AchException( v.result_string(status) )


    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
    else:
        raise ach.AchException( v.result_string(status) )

    [status, framesize] = t.get(tim, wait=False, last=True)
    oldtim = tim.sim[0]#save time for reference
    height, width = img.shape[:2]#define dims of image
    mid = width/2#midpoint of image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)#convert to hsv
    #define threshold for blue hue
    upper_white = np.array([130,255,255], dtype=np.uint8)
    lower_white = np.array([110,0,0], dtype=np.uint8)
    #create binary mask for blue
    mask = cv2.inRange(hsv, lower_white, upper_white)
    mom = cv2.moments(mask, True)#moments to get center of blue
    if(mom['m00']!=0):
      xf = int(mom['m10']/mom['m00'])
      yf = int(mom['m01']/mom['m00'])
      cv2.circle(img,(xf,yf), 10, (255,0,255),-1)#add circle on center
    else:
      xf = 0
      yf = 0
    cv2.imshow("wctrl", img)#show image
    diff = (float(xf)-mid)/mid#percent difference from center
    print(xf,yf,diff)
    #if image blanks out record 0 instead of -1
    if(diff == -1):
      f.write('0,')
    else:
      f.write(str(diff)+',')#write percent difference to file
    if((3*diff)>1):#if diff*3 is over 1 set to max
      ref.ref[0] = -1
      ref.ref[1] = 1
    elif((3*diff)<-1):#if diff*3 under 1 set to min
      ref.ref[0] = 1
      ref.ref[1] = -1
    else:
      ref.ref[0] = -1*(3*diff)#use difference to set speed of mots
      ref.ref[1] = 1*(3*diff)

    # Sets reference to robot
    r.put(ref)

    # Sleeps
    [status, framesize] = t.get(tim, wait=False, last=True)
    print(tim.sim[0]-oldtim)
    while(tim.sim[0]-oldtim<0.05):#wait for 50ms
      [status, framesize] = t.get(tim, wait=False, last=True)
