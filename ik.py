import numpy as np
from math import *
from matscript import *

def jacobian(xy0,xy1,xy2,delta):
  j00 = (xy1[0] - xy0[0])/delta
  j01 = (xy2[0] - xy0[0])/delta
  j10 = (xy1[1] - xy0[1])/delta
  j11 = (xy2[1] - xy0[1])/delta

def xysplit(xyd, xy0, samples):
  x = []
  y = []
  for i in range(1,samples+1):
    x.append(i*(xyd[0]-xy0[0])/samples + xy0[0])
    y.append(i*(xyd[1]-xy0[1])/samples + xy0[1])
  return np.matrix([x,y]).transpose()

def thetaout(x,y):
  L1 = 0.3
  L2 = 0.2
  theta1 = 0
  theta2 = 0
  delta = 0.01
  xyd = [x,y]
  xy0 = fk([L1,L2],[0,0])
  xy = xysplit(xyd,xy0,100)
  for i in range(100):
    xy0 = fk([L1,L2],[theta1,theta2])
    xy1 = fk([L1,L2],[theta1+delta,theta2])
    xy2 = fk([L1,L2],[theta1,theta2+delta])
    J = jacobian(xy0,xy1,xy2,delta)
    de = np.matrix([[xy[i,0]-xy0[0]],
                    [xy[i,1]-xy0[1]]])
    dtheta = J.getI()*de
    
