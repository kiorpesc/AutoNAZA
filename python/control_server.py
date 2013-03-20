import socket
import sys

HOST = ''
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error code: ' + str(msg[0]) + ' Message: ' + str(msg[1])
    sys.exit()

print 'Socket bind complete.'

s.listen(10)
print 'Socket now listening'

conn, addr = s.accept()

print 'Connected with ' + addr[0] + ':' + str(addr[1])

data = conn.recv(10)
if data == 'AutoNAZAOn':
    conn.sendall('potatoTime')
    while True:
else:
    conn.close()

s.close()
