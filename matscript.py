import numpy as np
from math import *

f = open('data', 'r')

l1 = float(f.readline())
l2 = float(f.readline())
l3 = float(f.readline())
th1= radians(float(f.readline()))
th2= radians(float(f.readline()))
th3= radians(float(f.readline()))

R1 = np.matrix([[cos(th1), -sin(th1), 0],[sin(th1),cos(th1),0],[0,0,1]])
R2 = np.matrix([[cos(th2), -sin(th2), 0],[sin(th2),cos(th2),0],[0,0,1]])
R3 = np.matrix([[cos(th3), -sin(th3), 0],[sin(th3),cos(th3),0],[0,0,1]])
R4 = np.matrix([[1,0,0],[0,1,0],[0,0,1]])
Dx = np.matrix([[1],[0],[0]])
D1 = Dx*0
D2 = Dx*l1
D3 = Dx*l2
D4 = Dx*l3
low= np.matrix([0,0,0,1])
T1 = np.concatenate([R1, D1], axis=1)
T1 = np.concatenate([T1, low], axis=0)
T2 = np.concatenate([R2, D2], axis=1)
T2 = np.concatenate([T2, low], axis=0)
T3 = np.concatenate([R3, D3], axis=1)
T3 = np.concatenate([T3, low], axis=0)
T4 = np.concatenate([R4, D4], axis=1)
T4 = np.concatenate([T4, low], axis=0)
T = T1*T2*T3*T4
print(T)
