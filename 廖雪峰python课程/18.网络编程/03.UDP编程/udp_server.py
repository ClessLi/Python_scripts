import socket
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#Binding socket
s.bind(('127.0.0.1',9999))
print 'Bind UDP on 9999...'
while True:
    #Receive data
    data,addr=s.recvfrom(1024)
    print 'Received from %s:%s.' % addr
    s.sendto('Hello %s.' % data,addr)