import hubo_ach as ha
import ach
import sys
import time
import numpy as np
from math import *
from ctypes import *
from matscript import *

s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)

state = ha.HUBO_STATE()
ref = ha.HUBO_REF()

ref.ref[ha.RSR] = -pi/2+pi/12
#ref.ref[ha.REB] = -pi/2+pi/18
#ref.ref[ha.RSP] = -pi/2+pi/18
r.put(ref)
r.close()
s.close()








