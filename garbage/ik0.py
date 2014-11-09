import hubo_ach as ha
import ach
import sys
import time
import numpy as np
from math import *
from ctypes import *
from matscript0 import *

def jacobian(xy0,xy1,xy2,delta):
  j00 = (xy1[0] - xy0[0])/delta
  j01 = (xy1[1] - xy0[1])/delta
  j10 = (xy2[0] - xy0[0])/delta
  j11 = (xy2[1] - xy0[1])/delta
  return np.matrix([[j00,j01],[j10,j11]])

s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)

state = ha.HUBO_STATE()
ref = ha.HUBO_REF()

err = 0.01
delta = -.01
shoulder = -.2145
forearm = -.18159
aftarm = -.17914
reb = 0
rsr = 0
rsy = -pi/2
xyd = [-.39609,-.17914]
xdone = False
ydone = False
ref.ref[ha.RSY] = -pi/2

while((not xdone) or (not ydone)):
  delta1 = 0
  delta2 = 0
  xory = 0
  xy0 = fk(aftarm,forearm,0,-reb,-rsr,0)
  xy0[0] += shoulder
  xy1 = fk(aftarm,forearm,0,-reb-delta,-rsr,0)
  xy1[0] += shoulder
  xy2 = fk(aftarm,forearm,0,-reb,-rsr-delta,0)
  xy2[0] += shoulder
  J = jacobian(xy0,xy1,xy2,delta)
  print(J)
  if(xy0[0] <= xyd[0]+err and xy0[0] >= xyd[0]-err):
    xdone = True
  if(xy0[1] <= xyd[1]+err and xy0[1] >= xyd[1]-err):
    ydone = True
  if(abs(xy0[0]-xyd[0])>abs(xy0[1]-xyd[1])):
    delta1 = J[0,0]
    delta2 = J[1,0]
    xory = 0
  else:
    delta1 = J[0,1]
    delta2 = J[1,1]
    xory = 1
  if(xdone and ydone):
    print("DONE")
  else:
    ref.ref[ha.REB] = -reb
    ref.ref[ha.RSR] = rsr-pi/9
    r.put(ref)
    [statuss, framesizes] = s.get(state, wait=False, last=False)
    t=state.time
    while((state.time-t)<0.01):
      [statuss, framesizes] = s.get(state, wait=False, last=False)

r.close()
s.close()








