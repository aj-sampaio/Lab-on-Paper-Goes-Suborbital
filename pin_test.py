#teste de pinos do Raspberry
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setmode(GPIO.BCM)
ugravity_power = 20     #supply for liftoff and ugravity
ugravity_ground = 21    #ground for liftoff and ugravity
sensor_supply_pin = 24    #end and start sensors supply
GPIO.setup(ugravity_power, GPIO.OUT)
GPIO.setup(ugravity_ground, GPIO.OUT)
GPIO.setup(sensor_supply_pin, GPIO.OUT)

GPIO.output(sensor_supply_pin, GPIO.HIGH)
GPIO.output(ugravity_ground, GPIO.LOW)
GPIO.output(ugravity_power, GPIO.HIGH)

while True:
    pin_number = int(input('Número do pino: '))
    escolha = input("Entrada ou Saída: ")
    if (escolha != 's' and escolha != 'S') :
        #Entrada
        GPIO.setup(pin_number, GPIO.IN)
        print('Estado do pino ' + str(pin_number) + ' = ' + str (GPIO.input(pin_number)))
    else :
        GPIO.setup(pin_number, GPIO.OUT)
        valor = input('0 ou 1 ')
        if (valor == 0):
            GPIO.output(pin_number, GPIO.HIGH)
        else:
            GPIO.output(pin_number, GPIO.LOW)
