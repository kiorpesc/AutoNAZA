import socket
import sys

def convert(s):
    values = map(ord, s)
    output = ''
    for x in values:
        output += (str(x) + ' ')
    print output

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



