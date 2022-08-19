import socket

HOST = '' # Server IP
PORT = 12345 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#flashmemory variable testmode/flightmode
#Primitiva non-blocking (incluido time.sleep) que permite testar se alguma imformação chegou, sem ficar preso
#
#Post-flight: automaticly go to testmode or 
#managing error exception
#dhcp protocolo de atribuicao de IP - configurar o lease do IP para não o perdermos
#macadress é um "nome" unico no mundo de cada maquina capaz de se ligar a internet
#Check if IP adress won't change. Neste macadress o IP adress é xxxxx
#Mais fácil é atribuiçao de IP estática.
#Descobrir como os IPs vao ser atribuidos no ambiente de teste pre-flight - STEFAN
#








try:
	s.bind((HOST, PORT))
except socket.error:
	print ('Bind failed ')

	s.listen(5)
	print ('Socket awaiting messages')
	(conn, addr) = s.accept()
	print ('Connected')

# awaiting for message
while True:
	data = conn.recv(1024)
	print ('I sent a message back in response to: ' + data)
	reply = ''

	# process your message
	if data == 'Hello':
		reply = 'Hi, back!'
	elif data == 'This is important':
		reply = 'OK, I have done the important thing you have asked me!'

	#and so on and on until...
	elif data == 'quit':
		conn.send('Terminating')
		break
	else:
		reply = 'Unknown command'

	# Sending reply
	conn.send(reply)
conn.close() # Close connections