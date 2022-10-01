import picamera
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

led_pin = 5
video_duration = 600   #<----  video duration in seconds
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT) # Set pin XX to be an output pin to control the LEDs

GPIO.output(led_pin, GPIO.HIGH)  #turn on leds
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.start_recording('my_video.h264')
camera.wait_recording(video_duration)
camera.stop_recording()
GPIO.output(led_pin, GPIO.LOW)  #turn off leds
