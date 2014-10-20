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

r.close()
s.close()









