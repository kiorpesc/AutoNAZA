import socket
import sys

conn = 0
s = 0

def create_socket():

    HOST = ''
    PORT = 8888

    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

def send_command(s):
    global conn
    try:
        conn.sendall(s)
    except:
        print 'Socket lost, closing.'
        close_socket()
        sys.exit()

def get_reply():
    try:
        conn.recv(10)
        return 1
    except:
        return 0

def close_socket():
    global conn
    global s
    #conn.close()
    s.close()
