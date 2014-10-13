import hubo_ach as ha
import ach
import sys
import time
import math
from ctypes import *

s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)

state = ha.HUBO_STATE()
ref = ha.HUBO_REF()

[statuss, framesizes] = s.get(state, wait=False, last=False)
t=state.time
print("Phase4")
for x in range(1,200):
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  ref.ref[ha.LKN] = 0.38
  ref.ref[ha.LHP] = -.38
  ref.ref[ha.LAP] = -.19
  ref.ref[ha.RHP] = -.38+.19-.19*math.cos((state.time-t)*0.1*math.pi)
  ref.ref[ha.RAP] = 0.19-.095+.095*math.cos((state.time-t)*0.1*math.pi)
  ref.ref[ha.LHR] = -.152+.152-.152*math.cos((state.time-t)*0.1*math.pi)
  ref.ref[ha.RHR] = -.152+.152-.152*math.cos((state.time-t)*0.1*math.pi)
  ref.ref[ha.LAR] = .152-.152+.152*math.cos((state.time-t)*0.1*math.pi)
  ref.ref[ha.RAR] = .152-.152+.152*math.cos((state.time-t)*0.1*math.pi)
  r.put(ref)
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  while((state.time-t)<0.05*x):
    [statuss, framesizes] = s.get(state, wait=False, last=False)
print("RHP", ref.ref[ha.RHP])
print("RAP", ref.ref[ha.RAP])
print("LHR", ref.ref[ha.LHR])
print("RHR", ref.ref[ha.RHR])
print("LAR", ref.ref[ha.LAR])
print("RAR", ref.ref[ha.RAR])
[statuss, framesizes] = s.get(state, wait=False, last=False)
t=state.time
print("Phase5")
for x in range(1,100):
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  ref.ref[ha.RKN] = .19-.19*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.RHP] = -.19+.19*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.RAP] = -.095+.095*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.LKN] = .19+.19*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.LAP] = -.19+.19-.19*math.cos((state.time-t)*0.2*math.pi)
  r.put(ref)
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  while((state.time-t)<0.05*x):
    [statuss, framesizes] = s.get(state, wait=False, last=False)
print("LKN", ref.ref[ha.LKN])
print("LHP", ref.ref[ha.LHP])
print("LAP", ref.ref[ha.LAP])
print("RKN", ref.ref[ha.RKN])
print("RAP", ref.ref[ha.RAP])

r.close()
s.close()









