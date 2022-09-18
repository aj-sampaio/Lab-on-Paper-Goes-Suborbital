import time             # Import time library
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import logging
import os
import socket

#<-----SETTINGS----->#
step_pin = 17
direction_pin = 23
led_pin = 5
start_sensor_pin = 22
end_sensor_pin = 25
sensor_supply_pin = 24
step_delay = 0.0002
led = 'off'
pwm_frequency = 500

ugravity_pin = 12   # μG signal is high as soon as microgravity
                    #   is achieved. Pin 10 of the DB15 connector
liftoff_pin = 16    # Liftoff signal goes high when the rocket
                    #   leaves the pad. Pin 5 of the DB15 connector
ugravity_power = 20     #also for liftoff
ugravity_ground = 21    #also for liftoff

#<------------------>#
GPIO.setmode(GPIO.BCM)
#pi1 = pigpio.pi()
#pi1.set_mode(step_pin, pigpio.OUTPUT) #STEP = GPIO17
#pi1.set_mode(direction_pin, pigpio.OUTPUT) #Direction = GPIO23
GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(led_pin, GPIO.OUT) # Set pin XX to be an output pin to control the LEDs
GPIO.setup(start_sensor_pin, GPIO.IN) # Set pin for beginning of rail touch sensor
GPIO.setup(end_sensor_pin, GPIO.IN) # Set pin for ending of rail touch sensor
GPIO.setup(sensor_supply_pin, GPIO.OUT) # Set pin for touch sensor supply
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(direction_pin, GPIO.OUT)
GPIO.setup(ugravity_pin, GPIO.IN)
GPIO.setup(ugravity_power, GPIO.OUT)
GPIO.setup(ugravity_ground, GPIO.OUT)
GPIO.setup(liftoff_pin, GPIO.IN)

GPIO.output(sensor_supply_pin, GPIO.HIGH)
GPIO.output(ugravity_ground, GPIO.LOW)     # activate ground of optocouplers
GPIO.output(ugravity_power, GPIO.HIGH)      # ativate power of optocouplers

logging.basicConfig(filename="log.txt", format='%(asctime)s %(message)s', filemode='a', datefmt='%d/%m/%Y %H:%M:%S')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

print('operations init done')

def write(pin, state): # Set a pin to HIGH or LOW
    try:
        GPIO.output(pin, state)
    except:
        print('failed')


def pwm():
    try:
        pwm = GPIO.PWM(step_pin, pwm_frequency)
        pwm.start(50)
    except:
        print('failed')

def leds():
    global led
    try:
        if led == 'off':
            GPIO.output(led_pin, GPIO.HIGH)
            led = 'on'
        else:
            GPIO.output(led_pin, GPIO.LOW)
            led = 'off'
    except:
        print('leds failed')

#def read_temp_humid():
 #   https://github.com/karlrupp/i2cHoneywellHumidity


def lift_off():
    if GPIO.input(liftoff_pin) == 0:
        return False
    time.sleep(0.1)
    if GPIO.input(liftoff_pin) == 0:
        return False
    else:
        return True

def ugravity():
    if GPIO.input(ugravity_pin) == 0:
        return False
    time.sleep(0.1)
    if GPIO.input(ugravity_pin) == 0:
        return False
    else:
        return True

def motorfront(duration):
    write(direction_pin, 0)
    timer = duration
    while (timer > 0):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(step_delay)
        timer = timer - step_delay
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(step_delay)
        timer = timer - step_delay
        if (GPIO.input(end_sensor_pin) == 1):
            print("Fim de curso")
            break

def motorback(duration):
    write(direction_pin, 1)
    timer = duration
    while (timer > 0):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(step_delay)
        timer = timer - step_delay
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(step_delay)
        timer = timer - step_delay
        if (GPIO.input(start_sensor_pin) == 1):
            print("Início de curso")
            break

def actuation():
    timer = 0
    dir = 1
    while (GPIO.input(end_sensor_pin) == 0):
        if (timer < 50):
            if (dir == 1):
                time.sleep(0.1)
                write(direction_pin, 0)
                dir = 0
        if (timer >= 50):
            if (dir == 0):
                time.sleep(0.1)
                write(direction_pin, 1)
                dir = 1
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(step_delay)
        timer = timer + step_delay
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(step_delay)
        timer = timer + step_delay
        if (timer >= 55):
            timer = 0
            dir = 1
    timer = 0
    dir = 0
    while (GPIO.input(start_sensor_pin) == 0):
        if (timer < 50):
            if (dir == 0):
                time.sleep(0.1)
                write(direction_pin, 1)
                dir = 1
        if (timer >= 50):
            if (dir == 1):
                time.sleep(0.1)
                write(direction_pin, 0)
                dir = 0
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(step_delay)
        timer = timer + step_delay
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(step_delay)
        timer = timer + step_delay
        if (timer >= 55):
            timer = 0
            dir = 0
    time.sleep(0.1)

def test_mode():
    global logger
    HOST = '193.137.214.251' # Server IP
    PORT = 40220
    socket.setdefaulttimeout(1) # we look frequently for the liftoff signal - Liftoff signal goes high when the rocket leaves the pad, from that moment on no more communciation through the socket are accepted.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Socket created')

    try:
        s.bind((HOST, PORT))
    except socket.error:
        print ('Bind failed ')
        s.close()
        return

    s.listen(5)
    print ('Socket awaiting messages')
    new_connection = False
    while ((new_connection == False) and (lift_off() == False)) :
            try:
                new_connection = True
                (conn, addr) = s.accept()
            except socket.timeout:
                new_connection = False
                print("Retry connection")
            except:
                print("Something else went wrong in s.accept")
                s.close()
                return
    if (lift_off() == True):
        return
    print ('Connected')

    # process test messages
    while True:
        # awaiting for message
        new_message = False
        while ((new_message == False) and (lift_off() == False)) :
            new_message = True
            try:
                data = conn.recv(1024)
            except socket.timeout:
                new_message = False
                print("Retry receive message")
            except:
                print("Something else went wrong in conn.recv")
                conn.close() # Close connections
                s.close()
                return

        if (lift_off() == True):
            return
        print ('I received a message: ' + str(data))
        reply = ' '

        # process message
        if data == b'Hello':
            reply = b'Hi, back!'
            logger.info(data)
        elif data == b'led':
            leds()
            reply = b'LEDs toggled'
            logger.info(reply)
        elif data == b'm':
            reply = b'Front motor movement activated'
            logger.info(reply)
            motorfront(3)
        elif data == b'-m':
            reply = b'Backwards motor movement activated'
            logger.info(reply)
            motorback(3)
        elif data == b'actuation':
            reply = b'Actuation test'
            logger.info(reply)
            actuation()
        elif data == b'video':
            reply = b'camera video recording test'
            logger.info(reply)
            rec_video()
        elif data == b'quit':
            break
        else:
            reply = b'Unknown command'
        conn.send(reply)   # Sending reply
        print ('I sent a reply: ' + str(reply))

    reply = b'Terminating'
    conn.send(reply)
    logger.info(reply)
    print (str(reply))
    conn.close() # Close connections
    s.close()
    return

def rec_video():
    os.system('chmod +x rec_video.py')
    os.system('nohup python rec_video.py &')
    return

def perform_experiment():
    actuation()
    logger.info('Experiment done')
    return
