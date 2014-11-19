import numpy as np
from math import *

def fk(ls,thetas):
  x = 0
  y = 0
  for i in range(len(ls)):
    x = x+ls[i]*cos(sum(thetas[0:i+1]))
    y = y+ls[i]*sin(sum(thetas[0:i+1]))
  return [x,y]
