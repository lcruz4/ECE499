import hubo_ach as ha
import ach
import sys
import time
from math import *
from ctypes import *

s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)

state = ha.HUBO_STATE()
ref = ha.HUBO_REF()
err = .01
shoulder = .2145
forearm = .18159
aftarm = .17914
reb = 0
rsy = 0
posd = (-.25,-.2,.2)
pos = (-shoulder-sin(rsy)*sin(reb/2)*aftarm-sin(rsy)*sin(reb/2)*forearm,
       -sin(rsy)*cos(reb/2)*aftarm-sin(rsy)*cos(reb/2)*forearm,
       cos(rsy)*sin(reb/2)*aftarm-cos(rsy)*sin(reb/2)*forearm)
hyp = sqrt(pow(posd[0]+shoulder,2)+pow(posd[1],2))
arm = aftarm+forearm
print(hyp)
while(not(arm > hyp-err and arm < hyp+err)):
  reb = reb + .01
  rsy = pi/2
  pos = (-shoulder-sin(rsy)*sin(reb/2)*aftarm-sin(rsy)*sin(reb/2)*forearm,
         -sin(rsy)*cos(reb/2)*aftarm-sin(rsy)*cos(reb/2)*forearm,
         cos(rsy)*sin(reb/2)*aftarm-cos(rsy)*sin(reb/2)*forearm)
  ref.ref[ha.REB] = -pi/2
  ref.ref[ha.RSY] = -rsy
  ref.ref[ha.RSR] = pi/9
#  ref.ref[ha.LSP] = pi/2
#  ref.ref[ha.LSY] = pi/2
  ref.ref[ha.LSR] = pi/2-pi/8
  print('thetas')
  print(reb,rsy)
  print('pos')
  print(pos)
  arm = aftarm*cos(reb/2)+forearm*cos(reb/2)
  print('arm')
  print(arm)
#  print(arm)
  r.put(ref)
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  t=state.time
  while((state.time-t)<0.01):
    [statuss, framesizes] = s.get(state, wait=False, last=False)
while(1):
  print(theta)
r.close()
s.close()









