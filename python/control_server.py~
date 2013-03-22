import socket
import sys

conn = 0
s = 0

def create_socket():

    HOST = ''
    PORT = 8888

    global s
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
    
    global conn
    conn, addr = s.accept()

    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    data = conn.recv(10)
    if data == 'AutoNAZAOn':
        conn.sendall('potatoTime')
        #for x in range(10):
        #    control = chr(255) + chr(90) + chr(90) + chr(90) + chr(0) + chr(95) + chr(90) + chr(90) + chr(x) + chr(254)
        #    conn.sendall(control)

def send_command(s):
    global conn
    conn.sendall(s)

def close_socket():
    global conn
    global s
    conn.close()
    s.close()
