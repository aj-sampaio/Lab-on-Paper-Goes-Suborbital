import socket

server = socket.socket()
server.bind(('', 3333)) #binds the socket to address
server.listen(5) #number of clients

