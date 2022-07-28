import pigpio # Import Raspberry Pi GPIO library
import time # Import time library
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import logging # Import logging module

logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
pi1 = pigpio.pi()
#pi1.set_mode(17, pigpio.OUTPUT) #STEP
#pi1.set_mode(25, pigpio.OUTPUT) #Direction
#GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
#GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
#GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 8 to be an input pin and set initial value to be pulled low (off)
#GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 12 to be an input pin and set initial value to be pulled low (off)
#GPIO.setup(14, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN) # Set pin 14 to be an output pin to control the LEDs

led = 'off'
#def camera():
    
    
def write(pin, state): # Set a pin to HIGH or LOW
    try:
        pi1.write(pin, state)
        logging.info('Pin', pin, 'was set to', state)
    except:
        logging.exception('Unable to set pin', pin, 'to state', state)                

def pwm(pin, dutycycle, frequency): # Sets a pin to produce a square wave with a fixed dutycycle and frequency
    try:
        pi1.set_PWM_frequency(pin, frequency)
        pi1.set_PWM_dutycycle(pin, dutycycle)
        logging.info('Pin', pin, 'was set to PWM with', frequency, 'Hz and', dutycycle, 'dutycycle')
    except:
        logging.exception('Unable to set pin', pin, 'to PWM')

def leds():
    global led
    try:
        if led == 'off':
            GPIO.output(14, GPIO.HIGH)
            logging.info('LEDs turned ON')
            led = 'on'
        else:
            GPIO.output(14, GPIO.LOW)
            logging.info('LEDs were turned OFF')
            led = 'off'
    except:
        logging.exception('Error turning LEDs ON/OFF')

def read_temp_humid():
    https://github.com/karlrupp/i2cHoneywellHumidity
def actuation():
        write(25, 0)
        time.sleep(0.01)
        pwm(17, 128, 500)
        time.sleep(0.5)
        write(25, 1)
        time.sleep(0.01)
        pwm(17, 128, 500)
        time.sleep(0.5)