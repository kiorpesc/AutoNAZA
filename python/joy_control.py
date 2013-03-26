import pygame
import socket
import sys
import time
import control_server

joy = []
axes = []
serv = [255, 90, 90, 90, 0, 95, 90, 90, 0, 254]
buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def command_string():
    output = ''
    for x in serv:
        output += chr(x)
    return output

def get_joy_pos():
        pygame.event.pump()
        for x in range(1, 5):
            pos = joy[0].get_axis(x - 1)
            serv[x] = int(round(pos * 90, 0) + 90)
        # reading buttons in this way will result in missed or duplicate inputs
        for x in range(12):
            if joy[0].get_button(x):
                buttons[x] = 1
            else:
                buttons[x] = 0
        time.sleep(0.03)

def convert_buttons():
    if buttons[2] == 1 and buttons[4] == 1:
        pass
    elif buttons[2] == 1:
        serv[5] = 95
    elif buttons[4] == 1:
        serv[5] = 28

def show_joy_pos():
        print serv
        print buttons

def control_loop():
    while True:
        get_joy_pos()
        convert_buttons()
        show_joy_pos()
        control_server.send_command(command_string())

def main():
    control_server.create_socket()
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
    control_loop()


# Allow use as a module or standalone script
if __name__ == "__main__":
    main()
