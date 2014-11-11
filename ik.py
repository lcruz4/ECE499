import hubo_ach as ha
import ach
import sys
import time
import numpy as np
from math import *
from ctypes import *
from matscript import *

def jacobian(xyz0,xyz1,xyz2,xyz3,delta):
  j00 = (xyz1[0] - xyz0[0])/delta
  j01 = (xyz1[1] - xyz0[1])/delta
  j02 = (xyz1[2] - xyz0[2])/delta
  j10 = (xyz2[0] - xyz0[0])/delta
  j11 = (xyz2[1] - xyz0[1])/delta
  j12 = (xyz2[2] - xyz0[2])/delta
  j20 = (xyz3[0] - xyz0[0])/delta
  j21 = (xyz3[1] - xyz0[1])/delta
  j22 = (xyz3[2] - xyz0[2])/delta
  return np.matrix([[j00,j01,j02],
                    [j10,j11,j12],
                    [j20,j21,j22]])

def xyzSplit(xyzd,xyz0,samples):
  x = []
  y = []
  z = []
  for i in range(1,samples+1):
    x.append(i*(xyzd[0]-xyz0[0])/samples + xyz0[0])
    y.append(i*(xyzd[1]-xyz0[1])/samples + xyz0[1])
    z.append(i*(xyzd[2]-xyz0[2])/samples + xyz0[2])
  return np.matrix([x,y,z]).transpose()

s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)

state = ha.HUBO_STATE()
ref = ha.HUBO_REF()

err = 0.01
delta = .01
shoulder = -.2145
forearm = -.18159
aftarm = -.17914
rsr = 0
reb = 0
rsp = 0
xyzd = [-.25,-.2,.2]
xdone = False
ydone = False
x=0
xyz0 = fk(aftarm,forearm,0,0,0)
xyz0[0] += shoulder
xyz = xyzSplit(xyzd,xyz0,100)
for i in range(100):
  xyz0 = fk(aftarm,forearm,-rsr,-reb,-rsp)
  xyz0[0] += shoulder
  xyz1 = fk(aftarm,forearm,-(rsr+delta),-reb,-rsp)
  xyz1[0] += shoulder
  xyz2 = fk(aftarm,forearm,-rsr,-(reb+delta),-rsp)
  xyz2[0] += shoulder
  xyz3 = fk(aftarm,forearm,-rsr,-reb,-(rsp+delta))
  xyz3[0] += shoulder
  J = jacobian(xyz0,xyz1,xyz2,xyz3,delta)
  de = np.matrix([[xyz[i,0]-xyz0[0]],
                  [xyz[i,1]-xyz0[1]],
                  [xyz[i,2]-xyz0[2]]])
  dtheta = J.getI()*de
  print 'current position'
  print xyz0
  print 'desired step position'
  print xyz[i,:]
  print 'change theta values rsr,reb,rsp'
  print dtheta
  rsr += dtheta[0,0]
  reb += dtheta[1,0]
  rsp += dtheta[2,0]
  print 'theta values rsr,reb,rsp'
  print [rsr,reb,rsp]
  ref.ref[ha.RSR] = -rsr+pi/12
  ref.ref[ha.REB] = -reb+pi/18
  ref.ref[ha.RSP] = -rsp+pi/18
  r.put(ref)
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  t=state.time
  while((state.time-t)<.1):
    [statuss, framesizes] = s.get(state, wait=False, last=False) 
  #try:
  #  input("Press enter to continue")
  #except SyntaxError:
  #  pass
  x += 1
r.close()
s.close()








