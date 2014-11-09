import numpy as np
from math import *

def fk(l1,l2,th1,th2,th3):
  th1 = radians(th1)
  th2 = radians(th2)
  th3 = radians(th3)

  Rz1 = np.matrix([[cos(th1),-sin(th1),0,0],
                   [sin(th1),cos(th1),0,0],
                   [0,0,1,0],
                   [0,0,0,1]])
  Rx1 = np.matrix([[1,0,0,0],
                   [0,cos(th3),-sin(th3),0],
                   [0,sin(th3),cos(th3),0],
                   [0,0,0,1]])
  Rz2 = np.matrix([[cos(th2),-sin(th2),0,0],
                   [sin(th2),cos(th2),0,0],
                   [0,0,1,0],
                   [0,0,0,1]])
  Dy1 = np.matrix([[1,0,0,0],
                   [0,1,0,l1],
                   [0,0,1,0],
                   [0,0,0,1]])
  Dy2 = np.matrix([[1,0,0,0],
                   [0,1,0,l2],
                   [0,0,1,0],
                   [0,0,0,1]])
  T01 = Rz1*Rx1*Dy1
  T12 = Rz2*Dy2
  T = T01*T12
  return [T[0,3],T[1,3],T[2,3]]
