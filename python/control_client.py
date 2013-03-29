import socket
import sys
import time
import servo
#from RPIO import PWM

#ailerons = PWM.Servo()
#elevators = PWM.Servo()
#rudder = PWM.Servo()
#throttle = PWM.Servo()
#gear = PWM.Servo()

#servos = [ailerons, elevators, rudder, throttle, gear]
#servo_gpio = [2, 3, 27, 17, 22]
last = chr(255) + chr(90) + chr(90) + chr(90) + chr(0) + chr(95) + chr(90) + chr(90) + chr(0) + chr(254)

#LOW_PULSE = 1050
#HIGH_PULSE = 1950

def arm_motors():
    servo.move(1, 0)
    servo.move(2, 180)
    servo.move(3, 0)
    servo.move(4, 180)

def map_val(val, in_low, in_high, out_low, out_high):
    # scale like farenheit to celsius
    # in_low = 0
    # in_high = 180
    # out_low = LOW_PULSE
    # out_high = HIGH_PULSE
    if val >= 85 and val <= 95:
        return 90
    else:
        return float(val) * float(out_high - out_low)/float(in_high - in_low) + float(out_low - in_low)

# convert received string to ASCII values and send servo commands
def convert(s):
    global last, servo_gpio, servos
    values = map(ord, s)
    output = ''
    #send servo commands to Arduino based on command string
    for x in range(1, 6):
        if values[8] == 180:
            output = 'FAILSAFE MODE!!!!!!!!!!!!!!!!!!!!!!!'
        elif values[8] == 90:
            arm_motors()
        else:
            if values[x] != last[x]:
                if x < 4:
                    mapped = int(map_val(values[x], 0, 180, 45, 135))
                    servo.move(x, mapped)
                    output += ' | ' + str(mapped) + ','
                    #servos[x-1].set_servo(servo_gpio[x-1], mapped)
                else:
                    servo.move(x, values[x])
                    output += ' | '
        output += str(values[x]) + ' | '
    print output
    last = s

while True:
    #this should all be wrapped in a main function
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print 'Socket Created'

        # host = 'exabase.org'
        host = '192.168.1.2'
        port = 8888

        try:
            remote_ip = socket.gethostbyname( host )
        except socket.gaierror:
            print 'Hostname could not be resolved.  Exiting'
            sys.exit()

        print 'Ip address of ' + host + ' is ' + remote_ip
    
        s.connect((remote_ip, port))

        print 'Socket Connected to ' + host + ' on ip ' + remote_ip

        message = "AutoNAZAOn"

        # Authorization?  Expect correct message in reply
        # if not correct, do not start receiving data

        try:
            s.sendall(message)
            print 'Message sent successfully'
        
            # reply will be 'potatoTime' for now
            reply = s.recv(10)
    
            print reply
         
            #may change message length for more buttons
            try:
                while True:
                    reply = s.recv(10)
                    convert(reply)
            # handle IndexError if data received is to short
            # (i.e. stream cut off)
            except: #socket.error, msg:
                #need to close socket in case of errors
                s.close()
                print 'CONNECTION LOST: ATTEMPTING RECONNECT -- '# + msg[1]

        #loop to beginning
        except socket.error, msg:
            print 'Send failed: ' + msg[1]
            sys.exit()

    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]
