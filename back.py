import os
import dynamixel
import time
import random
import sys
import subprocess
import optparse
import yaml
import numpy as np
import ach
from math import *

RAR=2
RAP=3
RKN=4
RHP=5
RHR=6
RHY=7

LAR=8
LAP=9
LKN=10
LHP=11
LHR=12
LHY=13

IDNAMES=["","","RAR","RAP","RKN","RHP","RHR","RHY","LAR","LAP","LKN","LHP","LHR","LHY"]

def rad2dyn(rad):
    return np.int(np.floor( (rad + (np.pi*300/360))/(2.0 * np.pi * 300/360) * 1024 ))

def dyn2rad(en):
    return (en / 1024.0 * 2.0 * np.pi - np.pi) * 300/360
def setGoal(myActuators,ID,val):
	for actuator in myActuators:
		if actuator.id==ID:
			actuator.goal_position = rad2dyn(val)
def getGoal(myActuators,ID):
	for actuator in myActuators:
		if actuator.id==ID:
			return dyn2rad(actuator.goal_position)

def main(settings):
    portName = settings['port']
    baudRate = settings['baudRate']
    highestServoId = settings['highestServoId']

    # Establish a serial connection to the dynamixel network.
    # This usually requires a USB2Dynamixel
    serial = dynamixel.SerialStream(port=portName, baudrate=baudRate, timeout=1)
    net = dynamixel.DynamixelNetwork(serial)
    
    # Ping the range of servos that are attached
    print "Scanning for Dynamixels..."
    net.scan(1, highestServoId)
    
    myActuators = []
    
    for dyn in net.get_dynamixels():
        print dyn.id
        myActuators.append(net[dyn.id])
    
    if not myActuators:
      print 'No Dynamixels Found!'
      sys.exit(0)
    else:
      print "...Done"
    
    for actuator in myActuators:
        actuator.moving_speed = 50
        actuator.synchronized = True
        actuator.torque_enable = True
        actuator.torque_limit = 800
        actuator.max_torque = 800
    
    # Randomly vary servo position within a small range

    enc = 0.0;
    angleToMove = -0.1
 	#set the starting position, standing straight
    for actuator in myActuators:
		if actuator.id==RHY or actuator.id==LHY:
			actuator.goal_position = rad2dyn(-.78)
		else:
			actuator.goal_position = rad2dyn(0)
    net.synchronize()
    time.sleep(4)

    while(1):
        for x in range(1,20):
            setGoal(myActuators,LHR,-0.16+.16*cos((x*.05)*pi))
            setGoal(myActuators,RHR,-0.16+.16*cos((x*.05)*pi))
            setGoal(myActuators,LAR,-0.16+.16*cos((x*.05)*pi))
            setGoal(myActuators,RAR,-0.16+.16*cos((x*.05)*pi))
            net.synchronize()
            time.sleep(.01)
        print "phase1R done"
        time.sleep(4)

        for x in range(1,20):
            setGoal(myActuators,RHP,0.25-.25*cos((x*.05)*pi))
            setGoal(myActuators,RAP,0.5-.5*cos((x*.05)*pi))
            setGoal(myActuators,RKN,-.25+.25*cos((x*.05)*pi))
            net.synchronize()
            time.sleep(.01)
        print "phase2R done"
        time.sleep(4)

        for x in range(1,20):
            setGoal(myActuators,LHR,0.16+.16*cos((x*.05)*pi))
            setGoal(myActuators,RHR,0.16+.16*cos((x*.05)*pi))
            setGoal(myActuators,LAR,0.16+.16*cos((x*.05)*pi))
            setGoal(myActuators,RAR,0.16+.16*cos((x*.05)*pi))
            setGoal(myActuators,RHP,0.5*cos((x*.05)*pi))
            setGoal(myActuators,RAP,1-.5+.5*cos((x*.05)*pi))
            setGoal(myActuators,LHP,0.25-.25*cos((x*.05)*pi))
            setGoal(myActuators,LKN,0.25-.25*cos((x*.05)*pi))
            net.synchronize()
            time.sleep(.01)
        print "phase3R done"
        time.sleep(.2)
        for x in range(1,20):
            setGoal(myActuators,LKN,0.5-.25+.25*cos((x*.05)*pi))
            setGoal(myActuators,RKN,-.5+.25-.25*cos((x*.05)*pi))
            setGoal(myActuators,LHP,0.5-.25+.25*cos((x*.05)*pi))
            setGoal(myActuators,RHP,-.5+.25-.25*cos((x*.05)*pi))
            net.synchronize()
            time.sleep(.01)
        print "phase4R done"
        time.sleep(4)
        for x in range(1,20):
            setGoal(myActuators,LHR,0.16-.16*cos((x*.05)*pi))
            setGoal(myActuators,RHR,0.16-.16*cos((x*.05)*pi))
            setGoal(myActuators,LAR,0.16-.16*cos((x*.05)*pi))
            setGoal(myActuators,RAR,0.16-.16*cos((x*.05)*pi))
            net.synchronize()
            time.sleep(.01)
        print "phase1L done"
        time.sleep(4)

        for x in range(1,20):
            setGoal(myActuators,LHP,-.25+.25*cos((x*.05)*pi))
            setGoal(myActuators,LAP,-.5+.5*cos((x*.05)*pi))
            setGoal(myActuators,LKN,0.25-.25*cos((x*.05)*pi))
            net.synchronize()
            time.sleep(.01)
        print "phase2L done"
        time.sleep(4)

        for x in range(1,20):
            setGoal(myActuators,LHR,-.16-.16*cos((x*.05)*pi))
            setGoal(myActuators,RHR,-.16-.16*cos((x*.05)*pi))
            setGoal(myActuators,LAR,-.16-.16*cos((x*.05)*pi))
            setGoal(myActuators,RAR,-.16-.16*cos((x*.05)*pi))
            setGoal(myActuators,LHP,-.5*cos((x*.05)*pi))
            setGoal(myActuators,LAP,-1+.5-.5*cos((x*.05)*pi))
            setGoal(myActuators,RHP,-.25+.25*cos((x*.05)*pi))
            setGoal(myActuators,RKN,-.25+.25*cos((x*.05)*pi))
            net.synchronize()
            time.sleep(.01)
        print "phase3L done"
        time.sleep(.2)
        for x in range(1,20):
            setGoal(myActuators,LKN,0.5-.25+.25*cos((x*.05)*pi))
            setGoal(myActuators,RKN,-.5+.25-.25*cos((x*.05)*pi))
            setGoal(myActuators,LHP,0.5-.25+.25*cos((x*.05)*pi))
            setGoal(myActuators,RHP,-.5+.25-.25*cos((x*.05)*pi))
            net.synchronize()
            time.sleep(.01)
        print "phase4L done"
        time.sleep(4)

def validateInput(userInput, rangeMin, rangeMax):
    '''
    Returns valid user input or None
    '''
    try:
        inTest = int(userInput)
        if inTest < rangeMin or inTest > rangeMax:
            print "ERROR: Value out of range [" + str(rangeMin) + '-' + str(rangeMax) + "]"
            return None
    except ValueError:
        print("ERROR: Please enter an integer")
        return None
    
    return inTest

if __name__ == '__main__':
    
    parser = optparse.OptionParser()
    parser.add_option("-c", "--clean",
                      action="store_true", dest="clean", default=False,
                      help="Ignore the settings.yaml file if it exists and \
                      prompt for new settings.")
    
    (options, args) = parser.parse_args()
    
    # Look for a settings.yaml file
    settingsFile = 'settings.yaml'
    if not options.clean and os.path.exists(settingsFile):
        with open(settingsFile, 'r') as fh:
            settings = yaml.load(fh)
    # If we were asked to bypass, or don't have settings
    else:
        settings = {}
        if os.name == "posix":
            portPrompt = "Which port corresponds to your USB2Dynamixel? \n"
            # Get a list of ports that mention USB
            try:
                possiblePorts = subprocess.check_output('ls /dev/ | grep -i usb',
                                                        shell=True).split()
                possiblePorts = ['/dev/' + port for port in possiblePorts]
            except subprocess.CalledProcessError:
                sys.exit("USB2Dynamixel not found. Please connect one.")
                
            counter = 1
            portCount = len(possiblePorts)
            for port in possiblePorts:
                portPrompt += "\t" + str(counter) + " - " + port + "\n"
                counter += 1
            portPrompt += "Enter Choice: "
            portChoice = None
            while not portChoice:                
                portTest = raw_input(portPrompt)
                portTest = validateInput(portTest, 1, portCount)
                if portTest:
                    portChoice = possiblePorts[portTest - 1]

        else:
            portPrompt = "Please enter the port name to which the USB2Dynamixel is connected: "
            portChoice = raw_input(portPrompt)
    
        settings['port'] = portChoice
        
        # Baud rate
        baudRate = None
        while not baudRate:
            brTest = raw_input("Enter baud rate [Default: 1000000 bps]:")
            if not brTest:
                baudRate = 1000000
            else:
                baudRate = validateInput(brTest, 9600, 1000000)
                    
        settings['baudRate'] = baudRate
        
        # Servo ID
        highestServoId = None
        while not highestServoId:
            hsiTest = raw_input("Please enter the highest ID of the connected servos: ")
            highestServoId = validateInput(hsiTest, 1, 255)
        
        settings['highestServoId'] = highestServoId
        
        # Save the output settings to a yaml file
        with open(settingsFile, 'w') as fh:
            yaml.dump(settings, fh)
            print("Your settings have been saved to 'settings.yaml'. \nTo " +
                   "change them in the future either edit that file or run " +
                   "this example with -c.")
    
    main(settings)
