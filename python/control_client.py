import socket
import sys
import servo

last = chr(255) + chr(90) + chr(90) + chr(90) + chr(0) + chr(95) + chr(90) + chr(90) + chr(0) + chr(254)

def convert(s):
    global last
    values = map(ord, s)
    output = ''
    # this causes a backup - need to rate limit incoming control messages
    # or only send to servos that have changed
    for x in range(1, 6):
        if values[x] != last[x]:
            servo.move(x, values[x])
        
        output +=str(values[x]) + ' '
    print output
    last = s

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]
    sys.exit()

print 'Socket Created'

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
except socket.error:
    print 'Send failed'
    sys.exit()

print 'Message sent successfully'

# reply will be 'potatoTime' for now
reply = s.recv(10)

print reply

while True:
    reply = s.recv(10)
    convert(reply)

s.close()



