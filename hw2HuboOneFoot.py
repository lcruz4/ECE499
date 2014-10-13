import hubo_ach as ha
import ach
import sys
import time
import math
from ctypes import *

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()
# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()
# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)
for x in range(1,10):
  ref.ref[ha.LHR] = (-0.1275*x)/10
  ref.ref[ha.RHR] = (-0.1275*x)/10
  ref.ref[ha.LAR] = (0.1275*x)/10
  ref.ref[ha.RAR] = (0.1275*x)/10
  r.put(ref)
  time.sleep(1.5)
for x in range(1,50):
  ref.ref[ha.RKN] = 1.5*float(x)/50
  ref.ref[ha.RHP] = -1.5*float(x)/50
  r.put(ref)
  time.sleep(1.5)
[statuss, framesizes] = s.get(state, wait=False, last=False)
t=state.time
for x in range(1,1000):
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  print(state.time)
  ref.ref[ha.LKN] = 0.7-0.7*math.cos((state.time-t)*1*math.pi)
  ref.ref[ha.LHP] = -0.35+0.35*math.cos((state.time-t)*1*math.pi)
  ref.ref[ha.LAP] = -0.35+0.35*math.cos((state.time-t)*1*math.pi)
  r.put(ref)
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  while((state.time-t)<0.01*x):
    [statuss, framesizes] = s.get(state, wait=False, last=False)
# Close the connection to the channels
r.close()
s.close()
