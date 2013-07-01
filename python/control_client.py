import socket
import sys
import time
import BBIO.PWM as PWM

# initial data
# START BYTE, X, Y, Z, THROTTLE, MODE, HAT X, HAT Y, FAILSAFE/ARM, END BYTE
last = chr(255) + chr(125) + chr(125) + chr(125) + chr(250) + chr(132) + chr(125) + chr(125) + chr(0) + chr(254)

DEAD_RADIUS = 0.41667
#pins           roll     pitch     yaw    throttle   aux
pins = [ ' ', 'P9_14', 'P9_16', 'P8_13', 'P8_19', 'P9_22']


def init_pwm():
    PWM.start(pins[1], 7.5)
    time.sleep(0.5)
    PWM.stop(pins[1])
    time.sleep(0.5)
    # start PWM output at 50Hz, all middle except throttle
    # 1.5/20 = .075 = 7.5%
    PWM.start(pins[1], 7.5, 50)
    PWM.start(pins[2], 7.5, 50)
    PWM.start(pins[3], 7.5, 50)
    PWM.start(pins[4], 10, 50)
    PWM.start(pins[5], 7.64, 50)
    PWM.on(pins[1])
    PWM.on(pins[2])
    PWM.on(pins[3])
    PWM.on(pins[4])
    PWM.on(pins[5])

def arm_motors():
    PWM.set_duty_cycle(pins[1], 5)
    PWM.set_duty_cycle(pins[2], 10)
    PWM.set_duty_cycle(pins[3], 5)
    PWM.set_duty_cycle(pins[4], 10)
'''
    servo.move(1, 0)
    servo.move(2, 250)
    servo.move(3, 0)
    servo.move(4, 250)
'''
#dead zone for joystick - only applied to x,y,z axes
def dead_zone(val):
    global DEAD_RADIUS
    
    #add dead zone as necessary (maybe should handle deadzone in server code?)
    if val >= (7.5 - DEAD_RADIUS) and val <= (7.5 + DEAD_RADIUS):
        return 7.5
    elif val < 7.5 - DEAD_RADIUS:
        return float(val) + float(DEAD_RADIUS)/2.0
    else:
        return float(val) - float(DEAD_RADIUS)/2.0

#map the input (0 - 180) to the proper output value (5.0 - 10.0)
def map_val(val, in_low, in_high, out_low, out_high):
    return float(val) * float(out_high - out_low)/float(in_high - in_low) + float(out_low - in_low)

# convert received string to ASCII values and send servo commands
def convert(s):
    global last
    values = map(ord, s)
    output = ''
    #send servo commands to Arduino based on command string
    for x in range(1, 6):
        if values[8] == 250:
            output = 'FAILSAFE MODE!!!!!!!!!!!!!!!!!!!!!!!'
        elif values[8] == 125:
            arm_motors()
        else:
            if values[x] != last[x]:
                mapped = map_val(values[x], 0, 250, 5.0, 10.0)
                if x < 4:
                    #calculate dead zone if necessary - this includes throttle
                    #just to make it easier to stay level using NAZA atti mode
                    #adjusted = dead_zone(mapped)                      
                    PWM.set_duty_cycle(pins[x], float(mapped))
                    output += ' | ' + str(adjusted) + ','
                else:
                    #buttons get no deadzone alteration
                    PWM.set_duty_cycle(pins[x], float(mapped))
                    output += ' | '

        output += str(values[x]) + ' | '
    print output
    last = s

def main():
    init_pwm()
    while True:
        # as this stands, it is impossible to get out of this script without a SIGKILL.
        # it just keeps looping, trying to make a socket connection.
        # this means that it will not exit cleanly, leaving the PWM pins enabled
        # THIS NEEDS TO CHANGE -- too any try/except blocks, not enough proper error handling.
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)

            print 'Socket Created'

            host = '69.249.183.97' 
            #host = 'exabase.org'
            #host = '192.168.1.21'
            #host = 'localhost'
            port = 8888

            try:
                remote_ip = socket.gethostbyname( host )
            except socket.gaierror:
                print 'Hostname could not be resolved.  Exiting'
                sys.exit()
            except KeyboardInterrupt:
                raise

            print 'Ip address of ' + host + ' is ' + remote_ip
        
            s.connect((remote_ip, port))

            print 'Socket Connected to ' + host + ' on ip ' + remote_ip

            message = "AutoNAZAOn"

            # TODO: Complex authorization?  
            # Expect correct message
            # if not correct, do not start receiving data

            try:
                s.sendall(message)
                print 'Message sent'
            
                # reply will be 'potatoTime' for now
                reply = s.recv(10)
    
                print reply

                
                #may change message length for more buttons
                try:
                    while True:
                        # if no data is received, the socket times out,
                        # which throws an exception, and the socket is closed and reopened
                        reply = s.recv(10)
                        convert(reply)
                        #this will eventually be used to send sensor data back to command
                        s.sendall(last)
                except KeyboardInterrupt:
                    raise
                except: 
                    s.close()
                    print 'CONNECTION LOST: ATTEMPTING RECONNECT -- '# + msg[1]

            #loop to beginning
            except socket.error, msg:
                print 'Send failed: '
            except KeyboardInterrupt:
                raise

        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]
        except KeyboardInterrupt:
               print 'Closing socket...'
               s.close()
               print 'Shutting down PWM outputs...'
               PWM.cleanup()
               time.sleep(.5)
               sys.exit()


# Allow use as a module or standalone script
if __name__ == "__main__":
    main()


