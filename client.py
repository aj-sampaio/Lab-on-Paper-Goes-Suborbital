import socket

HOST = '193.137.214.251' # Enter IP or Hostname of your server
PORT = 40220 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT)) #Lets loop awaiting for your input
while True:
	command = input('Enter your command: ')
	s.send(bytes(command,'utf-8'))
	reply = s.recv(1024)
	if reply == 'Terminate':
		break
	print (reply)
