import hubo_ach as ha
import ach
import sys
import time
from ctypes import *

s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
state = ha.HUBO_STATE()

ref = ha.HUBO_REF()

[statuss, framesizes] = s.get(state, wait=False, last=False)
t=state.time
ref.ref[ha.LEB] = -2.8
ref.ref[ha.LSY] = 1.2
ref.ref[ha.LSR] = 0.7
ref.ref[ha.LWY] = -0.2
r.put(ref)
[statuss, framesizes] = s.get(state, wait=False, last=False)
while((state.time-t)<.3):
  [statuss, framesizes] = s.get(state, wait=False, last=False)
c=True
for i in range(3):
  for x in range(1,13):
    [statuss, framesizes] = s.get(state, wait=False, last=False)
    t=state.time
    ref.ref[ha.RKN] = 1*float(x)/12
    ref.ref[ha.RHP] = -.5*float(x)/12
    ref.ref[ha.LKN] = 1*float(x)/12
    ref.ref[ha.LHP] = -.5*float(x)/12
    ref.ref[ha.RAP] = -.5*float(x)/12
    ref.ref[ha.LAP] = -.5*float(x)/12
    if(x%4==0):
      ref.ref[ha.LEB] = -2.8
    elif(x%2==0):
      ref.ref[ha.LEB] = -1.2
    r.put(ref)
    [statuss, framesizes] = s.get(state, wait=False, last=False)
    while((state.time-t)<(0.015)*x):
      [statuss, framesizes] = s.get(state, wait=False, last=False)
  for x in range(1,13):
    [statuss, framesizes] = s.get(state, wait=False, last=False)
    t=state.time
    ref.ref[ha.RKN] = 1-1*float(x)/12
    ref.ref[ha.RHP] = -.5+.5*float(x)/12
    ref.ref[ha.LKN] = 1-1*float(x)/12
    ref.ref[ha.LHP] = -.5+.5*float(x)/12
    ref.ref[ha.RAP] = -.5+.5*float(x)/12
    ref.ref[ha.LAP] = -.5+.5*float(x)/12
    if(x%4==0):
      ref.ref[ha.LEB] = -2.8
    elif(x%2==0):
      ref.ref[ha.LEB] = -1.2
    r.put(ref)
    [statuss, framesizes] = s.get(state, wait=False, last=False)
    while((state.time-t)<(0.015)*x):
      [statuss, framesizes] = s.get(state, wait=False, last=False)
for x in range(16):
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  t=state.time
  if(c):
    ref.ref[ha.LEB] = -1.2
    c = False
  else:
    ref.ref[ha.LEB] = -2.8
    c = True
  r.put(ref)
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  while((state.time-t)<(0.03)*x):
    [statuss, framesizes] = s.get(state, wait=False, last=False)
ref.ref[ha.LEB] = 0
ref.ref[ha.LSY] = 0
ref.ref[ha.LSR] = 0
ref.ref[ha.LWY] = 0
r.put(ref)
r.close()
s.close()
