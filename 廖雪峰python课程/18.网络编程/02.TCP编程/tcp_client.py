import socket
import time
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#Creat a connection
s.connect(('127.0.0.1',9999))
#Accept a message with "Welcome"
print s.recv(1024)
for data in ['Cless','Chester','Mint','Arche']:
    #Send data to server
    s.send(data)
    print s.recv(1024)
s.send('exit')
s.close()