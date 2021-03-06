#!/usr/bin/env python

################################################
# Module:   servo.py
# Created:  2 April 2008
# Author:   Brian D. Wendt
#   http://principialabs.com/
# Version:  0.3
# License:  GPLv3
#   http://www.fsf.org/licensing/
'''
Provides a serial connection abstraction layer
for use with Arduino "MultipleSerialServoControl" sketch.
'''
################################################

import serial
import sys

# Assign Arduino's serial port address
#   Windows example
#     usbport = 'COM3'
#   Linux example
#     usbport = '/dev/ttyUSB0'
#   MacOSX example
#     usbport = '/dev/tty.usbserial-FTALLOK2'

baud_rate = 9600

if sys.platform[0:5] == 'linux':
    usbport0 = '/dev/ttyACM0'
    usbport1 = '/dev/ttyACM1'
elif sys.platform[0:3] == 'win':
    usbport0 = 'COM3'
    usbport1 = 'COM5'
elif sys.platform == 'darwin' or sys.platform == 'mac':
    usbport0 = '/dev/tty.usbserial-FTALLOK2'
    usbport1 = '/dev/tty.usbserial-FTALLOK3'
else:
    print "\nSystem not supported, exiting... "
    quit()

# Set up serial baud rate
try:
    ser = serial.Serial(usbport0, baud_rate, timeout=1)
except:
    print "\nTrying alternate port..."
    try:
        ser = serial.Serial(usbport1, baud_rate, timeout=1)
    except:
        print "\nCan't find serial port, exiting."
        quit()


def move(servo, angle):
    '''Moves the specified servo to the supplied angle.

    Arguments:
        servo
          the servo number to command, an integer from 1-4
        angle
          the desired servo angle, an integer from 0 to 180

    (e.g.) >>> servo.move(2, 90)
           ... # "move servo #2 to 90 degrees"'''

    if (0 <= angle <= 180):
        ser.write(chr(255))
        ser.write(chr(servo))
        ser.write(chr(angle))
    else:
        print "Servo angle must be an integer between 0 and 180.\n"
