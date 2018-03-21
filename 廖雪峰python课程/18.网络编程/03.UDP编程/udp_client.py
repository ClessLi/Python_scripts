import socket
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
for data in ['Cless','Mint','Chester','Arche']:
    #Send data
    s.sendto(data,('127.0.0.1',9999))
    #Receive data
    print s.recv(1024)
s.close()