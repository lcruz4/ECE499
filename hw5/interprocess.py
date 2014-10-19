import controller_include as ci
import ach
import sys
import time
import numpy as np
from AX12 import *
import diff_drive
import socket
import actuator_sim as ser

dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN = 'robot-diff-drive'
ROBOT_CHAN_VIEW = 'robot-vid-chan'
ROBOT_TIME_CHAN = 'robot-time'

r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()
c = ach.Channel(ci.CONTROLLER_REF_NAME)
c.flush()
controller = ci.CONTROLLER_REF()
c.put(controller)

while True:
  [statuss, framesizes] = c.get(controller, wait=False, last= False)
  ref = ser.serial_sim(r,ref,speedcmd(0,controller.mot1))
  ref = ser.serial_sim(r,ref,speedcmd(1,controller.mot2))
