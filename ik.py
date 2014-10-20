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
x = -.25
y = -.2
hyp = sqrt(pow(x+shoulder,2)+pow(y,2))
arm = aftarm+forearm
theta = 0
print(hyp)
while(not(arm > hyp-err and arm < hyp+err)):
  theta = theta + .01
  ref.ref[ha.REB] = -theta
  ref.ref[ha.RSY] = -pi/2
  arm = aftarm*sin(theta/2)+forearm*sin(theta/2)
  print(arm)
  r.put(ref)
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  t=state.time
  while((state.time-t)<0.01):
    [statuss, framesizes] = s.get(state, wait=False, last=False)
while(1):
  print(theta)
r.close()
s.close()









