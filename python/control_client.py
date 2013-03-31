import socket
import sys
import time
import servo

# initial data
# START BYTE, X, Y, Z, THROTTLE, MODE, HAT X, HAT Y, FAILSAFE/ARM, END BYTE
last = chr(255) + chr(90) + chr(90) + chr(90) + chr(180) + chr(95) + chr(90) + chr(90) + chr(0) + chr(254)

DEAD_RADIUS = 15

def arm_motors():
    servo.move(1, 0)
    servo.move(2, 180)
    servo.move(3, 0)
    servo.move(4, 180)

#scales input values, also takes care of dead zone for joystick
def map_val(val, in_low, in_high, out_low, out_high):
    global DEAD_RADIUS
    # in_low = 0
    # in_high = 180
    # out_low = LOW_PULSE
    # out_high = HIGH_PULSE
    scaled_val = float(val) * float(out_high - out_low)/float(in_high - in_low) + float(out_low - in_low)
    if val >= (90 - DEAD_RADIUS) and val <= (90 + DEAD_RADIUS):
        return 90
    elif val < 90 - DEAD_RADIUS:
        return scaled_val + float(DEAD_RADIUS)/2
    else:
        return scaled_val - float(DEAD_RADIUS)/2

# convert received string to ASCII values and send servo commands
def convert(s):
    global last
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
                else:
                    servo.move(x, values[x])
                    output += ' | '
        output += str(values[x]) + ' | '
    print output
    last = s

def main():
    while True:
        #this should all be wrapped in a main function
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)

            print 'Socket Created'

            #host = 'exabase.org'
            #host = '192.168.1.21'
            host = 'localhost'
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
                print 'Message sent'
            
                # reply will be 'potatoTime' for now
                reply = s.recv(10)
    
                print reply

                
                #may change message length for more buttons
                try:
                    while True:
                        # if no data is received, socket times out,
                        # throws exception, and the socket is closed and reopened
                        reply = s.recv(10)
                        convert(reply)
                        #this will eventually be used to send sensor data back to command
                        s.sendall(last)
                except: 
                    s.close()
                    print 'CONNECTION LOST: ATTEMPTING RECONNECT -- '# + msg[1]

            #loop to beginning
            except socket.error, msg:
                print 'Send failed: ' + msg[1]

        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]


# Allow use as a module or standalone script
if __name__ == "__main__":
    main()


