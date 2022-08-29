import socket
import operations
import time

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

led_flag = 'off'






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
        
	# LED command -> led
    	elif data == 'led':
        	global led_flag
        	if led_flag == 'off':
            	    operations.leds()
            	    time.sleep(0.1)
            	    led_flag = 'on'
            	    print('LEDs turned', led_flag)
                else:
                    operations.leds()
                    time.sleep(0.1)
                    led_flag = 'off'
                    print('LEDs turned')
                reply = 'LED function activated'
    
   	 # Stepper motor command -> motor<direction><duration>      Eg. motorfront500/motorback100 (direction=front/back; duration in miliseconds)
    	# Right now duration is set to 500 miliseconds, duration control to be implemented later
    	elif data == 'motorfront':
        	operations.motorfront()
		time.sleep(0.1)
        print('Motor moved frontwards')
        
        elif data == 'motorback':
            operations.motorback()
            time.sleep(0.1)
            print('Motor moved frontwards')
	    #and so on and on until...
	elif data == 'quit':
		conn.send('Terminating')
		break
	else:
		reply = 'Unknown command'

	# Sending reply
	conn.send(reply)
conn.close() # Close connections
