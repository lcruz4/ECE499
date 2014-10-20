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
err = .001
shoulder = .2145
forearm = .18159
aftarm = .17914
x = -.25
y = -.2
hyp = sqrt(pow(x+shoulder,2)+pow(y,2))
arm = aftarm+forearm

[statuss, framesizes] = s.get(state, wait=False, last=False)
t=state.time
print(hyp)
while(not(arm > hyp-err and arm < hyp+err))

for x in range(1,100):
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  ref.ref[ha.LHR] = -.076+.076*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.RHR] = -.076+.076*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.LAR] = .076-.076*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.RAR] = .076-.076*math.cos((state.time-t)*0.2*math.pi)
  r.put(ref)
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  while((state.time-t)<0.05*x):
    [statuss, framesizes] = s.get(state, wait=False, last=False)
print("LHR", ref.ref[ha.LHR])
print("RHR", ref.ref[ha.RHR])
print("LAR", ref.ref[ha.LAR])
print("RAR", ref.ref[ha.RAR])
[statuss, framesizes] = s.get(state, wait=False, last=False)
t=state.time
print("Phase2")
for x in range(1,100):
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  ref.ref[ha.RHP] = -.19+.19*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.RKN] = .19-.19*math.cos((state.time-t)*0.2*math.pi)
  r.put(ref)
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  while((state.time-t)<0.05*x):
    [statuss, framesizes] = s.get(state, wait=False, last=False)
print("RHP", ref.ref[ha.RHP])
print("RKN", ref.ref[ha.RKN])
[statuss, framesizes] = s.get(state, wait=False, last=False)
t=state.time
print("Phase3")
for x in range(1,100):
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  ref.ref[ha.LKN] = .19-.19*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.LHP] = -.19+.19*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.LAP] = -.095+.095*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.RKN] = .19+.19*math.cos((state.time-t)*0.2*math.pi)
  ref.ref[ha.RAP] = .095-.095*math.cos((state.time-t)*0.2*math.pi)
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









