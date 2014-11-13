import math
import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

import actuator_sim as ser
#Change these if you have more than 10 speed bits
SPEED_BITS=10
MASK=int(math.pow(2,SPEED_BITS)-1)
#Calculates the checksum and appends it to the end of the array, Returns the array
def CalcCheckSum(Packet):
	CheckSum=0
	for x in range(len(Packet)):
		if(x==0 or x==1):
			pass
		else:
			CheckSum=CheckSum+Packet[x];
	
	CheckSum=~CheckSum
	CheckSum&=0xff
	Packet.append(CheckSum)
	return Packet
#Creates the velocity packet and returns it
#value needs to be between -1 and 1 
def VelocityPacket(velocity):
	velocity=int(MASK*velocity)
	mag=0
	direct=0	
	if velocity<0:
		direct=0
	else:
		direct=1
	mag = abs(velocity)
	mag &= MASK

	pack=direct << SPEED_BITS
	pack|=mag

	byte1=pack&0xFF00
	byte1=byte1>>8
	byte2=pack&0xFF
	packet=[byte1,byte2]

	return packet

#sets the wheels to rotate, returns ref
#value needs to be between -1 and 1 
def rotate(r,ref,velocity):
	
        rightVelocPack=VelocityPacket(velocity)
	rightPacket=[255,255,0,0x20,0x00,rightVelocPack[1],rightVelocPack[0]]
	rightPacket=CalcCheckSum(rightPacket)
        
        leftVelocPack=VelocityPacket(-velocity)
	leftPacket=[255,255,1,0x20,0x00,leftVelocPack[1],leftVelocPack[0]]
	leftPacket=CalcCheckSum(leftPacket)

	ref = ser.serial_sim(r,ref,rightPacket)
	ref = ser.serial_sim(r,ref,leftPacket)
	
        return ref

#sets the right wheel to go forward or backwards, returns ref
#value needs to be between -1 and 1 
def rightWheel(r,ref,velocity):
        rightVelocPack=VelocityPacket(velocity)
	rightPacket=[255,255,0,0x00,0x20,rightVelocPack[1],rightVelocPack[0]]
	rightPacket=CalcCheckSum(rightPacket)

	ref = ser.serial_sim(r,ref,rightPacket)
	
        return ref

#sets the left wheel to go forward or backwards, returns ref
#value needs to be between -1 and 1 
def leftWheel(r,ref,velocity):        
        leftVelocPack=VelocityPacket(velocity)
	leftPacket=[255,255,1,0x00,0x20,leftVelocPack[1],leftVelocPack[0]]
	leftPacket=CalcCheckSum(leftPacket)

	ref = ser.serial_sim(r,ref,leftPacket)
	
        return ref

