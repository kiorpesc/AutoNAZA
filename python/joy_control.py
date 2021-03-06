import argparse
import pygame
import socket
import sys
import time
import control_server

# in Windows, axis 3 is Throttle, 4 is rudder
# in Linux, axis 4 is Throttle, 3 is rudder.
# this is a pain in the ass, so it's been
# taken care of in the command_string() method

SCALING = 100
DEAD_RADIUS = 21

# changing range from 0 - 250
# midpoint is at 125
# 95 approximates to 132
# 28 approximates to 39

joy = []
axes = []
# START,X,Y,Z,THROTTLE,Atti/Man,hat x,hat y,failsafe,END
serv = [255, 125, 125, 125, 0, 125, 125, 125, 0, 254]
buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def parse_args():
    parser = argparse.ArgumentParser(description='Start joystick server.')
    parser.add_argument("-s","--scale",action="store",default=100,help="Control scaling percentage.")
    parser.add_argument("-d","--dead-zone",action="store",default=21,help="Joystick dead zone radius as a percentage.")
    args = vars(parser.parse_args())

    #check for unsafe values - exit if unsafe
    if int(args['dead_zone']) > 35 or int(args['dead_zone']) < 5:
        print 'This dead zone should be between 5 and 35 (inclusive).  Exiting...'
        sys.exit()
    else:
        DEAD_RADIUS = args['dead_zone']

    if int(args['scale']) < 50 or int(args['scale']) > 100:
        print 'Scale should be between 50 and 100 for safety.  Exiting...'
        sys.exit()
    else:
        SCALING = args['scale']

# very basic scaling
def scale_axes():
    for x in range(1, 5):
        serv[x] = (serv[x] - 125) * (SCALING / 100) + 125

# add dead zone to axes
def dead_zone(i):
    if serv[i] >= (125-DEAD_RADIUS) and serv[i] <= (125+DEAD_RADIUS):
        serv[i] =  125
    elif serv[i] < 125-DEAD_RADIUS:
        serv[i] = serv[i] + DEAD_RADIUS
    else:
        serv[i] = serv[i] - DEAD_RADIUS

    #prevent invalid values
    if serv[i] < 0:
        serv[i] = 0
    
    if serv[i] > 250:
        serv[i] = 250
        

def command_string():
    output = ''
    for x in serv:
        output += chr(x)
    # if Windows, swap Rudder and Throttle
    if sys.platform == 'win32':
	    output = output[0:3] + output[4] + output[3] + output[5:]
    return output

def get_joy_pos():
        pygame.event.pump()
        #read axes
        for x in range(1, 5):
            pos = joy[0].get_axis(x - 1)
            serv[x] = int(round(pos * 125, 0) + 125)
            # if x < 4:
            # apply dead zone calcualtion to all axes (incl throttle)
            dead_zone(x)
            
        # read buttons
        for x in range(12):
            if joy[0].get_button(x):
                buttons[x] = 1
            else:
                buttons[x] = 0
        time.sleep(0.05)

# handle button presses, being careful
# not to allow strange combinations of buttons
def convert_buttons():

    #flight mode switch
    if buttons[2] == 1 and buttons[4] == 1:
        pass
    elif buttons[2] == 1:
        serv[5] = 132
    elif buttons[4] == 1:
        serv[5] = 39

    #failsafe	
    if buttons[7] == 1:
        serv[8] = 250
    #deactivate failsafe	
    if buttons[6] == 1:
        serv[8] = 0

    #arm motors
    if buttons[11] == 1:
        serv[8] = 125
    if buttons[11] == 0 and serv[8] != 250:
        serv[8] = 0	

#quick print of array contents for debug purposes
def show_joy_pos():
        print serv
        print buttons

#the conversion and data transfer methods are called here
#and handling of the received sensor data will be done here as well.
def control_loop():
    while True:
        get_joy_pos()
        convert_buttons()
        scale_axes()
        show_joy_pos()
        control_server.send_command(command_string())
        if control_server.get_reply():
            #convert reply to something useful
            pass
        else:
            break

def main():
    parse_args()
    #loop, if socket recieve fails, retry.
    #need to check for incomplete packets on client
    while True:
        try:
            control_server.create_socket()
            
            #pygame joystick initialization code
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

            #start loop to convert, send, and receive values
            control_loop()
            
            #if loop ends (somehow) close the socket cleanly
            control_server.close_socket()
        #if Ctrl-C is pressed, close socket cleanly and exit
        except KeyboardInterrupt:
            print 'Closing socket'
            control_server.close_socket()
            sys.exit()
        #otherwise, close the socket and wait for another connection
        except:
            control_server.close_socket()

# Allow use as a module or standalone script
if __name__ == "__main__":
    main()
