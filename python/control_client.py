import socket
import sys
import servo

last = chr(255) + chr(90) + chr(90) + chr(90) + chr(0) + chr(95) + chr(90) + chr(90) + chr(0) + chr(254)

# convert received string to ASCII values and send servo commands
def convert(s):
    global last
    values = map(ord, s)
    output = ''
    #send servo commands to Arduino based on command string
    for x in range(1, 6):
        if values[x] != last[x]:
            servo.move(x, values[x])
        
        output +=str(values[x]) + ' '
    print output
    last = s

while True:
    #this should all be wrapped in a main function
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print 'Socket Created'

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
            except:
                #need to close socket in case of errors
                s.close()
                print 'CONNECTION LOST: ATTEMPTING RECONNECT'

        #loop to beginning
        except socket.error:
            print 'Send failed'
            sys.exit()

    except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]
sys.exit()
