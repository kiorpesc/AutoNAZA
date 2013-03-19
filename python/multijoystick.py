#!/usr/bin/env python

###############################################################################
# Module:   multijoystick.py
# Created:  2 April 2008
# Last Updated: 19 March 2013
# Author:   Brian D. Wendt, Matt Sowden, Charles Kiorpes
#   http://principialabs.com/
#   http://exabase.org/
# Version:  0.6.1.2.3.BCCC
# License:  GPLv3
#   http://www.fsf.org/licensing/
'''
Provides four-axis control of the DJI NAZA flight controller
using a regular USB joystick (tested using Logitech Extreme3D Pro).
Handles 12 buttons, a hat, x y and z axes, and throttle.

This code was adapted from:
  http://svn.lee.org/swarm/trunk/mothernode/python/multijoy.py

Dependencies:
  pyserial - http://pyserial.sourceforge.net/
  pygame   - http://www.pygame.org/
  servo    - http://principialabs.com/arduino-python-4-axis-servo-control/
  
Furthermore, I am an egg.
'''
###############################################################################

print "\n================================================"
print "        Hey There Everyone!"
print "================================================"

# Import dependent Python modules
try:
	import servo
except:
	print "\nPlease ensure that 'servo.py' is installed in the current directory.\n"
	quit()
try:
	import pygame.joystick
except:
	print "\nPlease install the 'pygame' module <http://www.pygame.org/>.\n"
	quit()

import time

# Allow for multiple joysticks
joy = []


# Handle joystick event
def handleJoyEvent(e):
    # Identify joystick axes and assign events
    # Throttle and Z reversed?
    if e.type == pygame.JOYAXISMOTION:
        axis = "unknown"
        if (e.dict['axis'] == 0):
            axis = "X"
        elif (e.dict['axis'] == 1):
            axis = "Y"
        elif (e.dict['axis'] == 2):
            axis = "Z"
        elif (e.dict['axis'] == 3):
            axis = "Throttle"

        # Convert joystick value to servo position for each axis
        if (axis != "unknown"):
            str = "Axis: %s; Value: %f" % (axis, e.dict['value'])
            # Uncomment to display axis values:
            #output(str, e.dict['joy'])

            # X Axis
            if (axis == "X"):
                pos = e.dict['value']
                # convert joystick position to servo increment, 0-180
                move = round(pos * 90, 0)
                serv = int(90 + move)
                # and send to Arduino over serial connection
                servo.move(1, serv)
            # Y Axis
            elif (axis == "Y"):
                pos = e.dict['value']
                move = round(pos * 90, 0)
                serv = int(90 + move)
                servo.move(2, serv)
            # Z Axis - on NAZA, servo 4
            elif (axis == "Z"):
                pos = e.dict['value']
                move = round(pos * 90, 0)
                serv = int(90 + move)
                servo.move(4, serv)
            # Throttle - on NAZA, servo 3
            elif (axis == "Throttle"):
                pos = e.dict['value']
                move = round(pos * 90, 0)
                serv = int(90 + move)
                servo.move(3, serv)

    # Assign actions for Button DOWN events
    elif e.type == pygame.JOYBUTTONDOWN:
        # Button 1 (trigger)
        if (e.dict['button'] == 0):
            print "Trigger Down"
        # Button 2
        elif (e.dict['button'] == 1):
            print "Button 2 Down"
        # Button 3
        elif (e.dict['button'] == 2):
            print "Button 3 Down, Attitude Mode"
            servo.move(5, 95)
        # Button 4
        elif (e.dict['button'] == 3):
            print "Button 4 Down"
        # Button 5
        elif (e.dict['button'] == 4):
            print "Button 5 Down, Manual Mode"
            servo.move(5, 28)
        # Button 6
        elif (e.dict['button'] == 5):
            print "Button 6 Down"
            quit()
        elif (e.dict['button'] == 6):
            print "Button 7 Down"
        elif (e.dict['button'] == 7):
            print "Button 8 Down"
        elif (e.dict['button'] == 8):
            print "Button 9 Down"
        elif (e.dict['button'] == 9):
            print "Button 10 Down"
        elif (e.dict['button'] == 10):
            print "Button 11 Down"
        elif (e.dict['button'] == 11):
            print "Button 12 Down"

    # Assign actions for Button UP events
    elif e.type == pygame.JOYBUTTONUP:
        # Button 1 (trigger)
        if (e.dict['button'] == 0):
            print "Trigger Up"
        # Button 2
        elif (e.dict['button'] == 1):
            print "Button 2 Up"
        # Button 3
        elif (e.dict['button'] == 2):
            print "Button 3 Up"
        # Button 4
        elif (e.dict['button'] == 3):
            print "Button 4 Up"
        # Button 5
        elif (e.dict['button'] == 4):
            print "Button 5 Up"
        # Button 6
        elif (e.dict['button'] == 5):
            print "Button 6 Up"
        elif (e.dict['button'] == 6):
            print "Button 7 Up"
        elif (e.dict['button'] == 7):
            print "Button 8 Up"
        elif (e.dict['button'] == 8):
            print "Button 9 Up"
        elif (e.dict['button'] == 9):
            print "Button 10 Up"
        elif (e.dict['button'] == 10):
            print "Button 11 Up"
        elif (e.dict['button'] == 11):
            print "Button 12 Up"

    # Assign actions for Coolie Hat Switch events
    elif e.type == pygame.JOYHATMOTION:
        if (e.dict['value'][0] == -1):
            print "Hat Left"
            servo.move(4, 0)
        elif (e.dict['value'][0] == 1):
            print "Hat Right"
            servo.move(4, 180)
        elif (e.dict['value'][1] == -1):
            print "Hat Down"
        elif (e.dict['value'][1] == 1):
            print "Hat Up"
        elif (e.dict['value'][0] == 0 and e.dict['value'][1] == 0):
            print "Hat Centered"
		
    else:
        pass

# Print the joystick position
def output(line, stick):
    print "Joystick: %d; %s" % (stick, line)

# Wait for joystick input
def joystickControl():
    while True:
        #constantPWM()
        e = pygame.event.wait()
        if (e.type == pygame.JOYAXISMOTION or e.type == pygame.JOYBUTTONDOWN or e.type == pygame.JOYBUTTONUP or e.type == pygame.JOYHATMOTION):
            handleJoyEvent(e)
        #time.sleep(.01)

# Send constant control values
def constantPWM():
    servo.move(1, serv[0])
    servo.move(2, serv[1])
    servo.move(3, serv[2])
    servo.move(4, serv[3])
    servo.move(5, serv[4])

# Main method
def main():
    # Initialize pygame
    pygame.joystick.init()
    pygame.display.init()
    if not pygame.joystick.get_count():
        print "\nPlease connect a joystick and run again.\n"
        quit()
    print "\n%d joystick(s) detected." % pygame.joystick.get_count()
    for i in range(pygame.joystick.get_count()):
        myjoy = pygame.joystick.Joystick(i)
        myjoy.init()
        joy.append(myjoy)
        print "Joystick %d: " % (i) + joy[i].get_name()
    print "Depress joystick button 6 to quit.\n"

    # Run joystick listener loop
    joystickControl()

# Allow use as a module or standalone script
if __name__ == "__main__":
    main()
