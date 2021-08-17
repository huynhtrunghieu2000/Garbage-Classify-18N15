# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# # Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(15, GPIO.OUT)
servo1 = GPIO.PWM(15, 50)  # pin 11 for servo1, pulse 50Hz

# # Start PWM running, with value of 0 (pulse off)
servo1.start(0)

# Loop to allow user to set servo angle. Try/finally allows exit
# with execution of servo.stop and GPIO cleanup :)


def RollToAngle(servo, angle):
    servo.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

RollToAngle(servo1,100)
# RollToAngle(servo1,40)
LED =37
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED,GPIO.HIGH)
time.sleep(1)
GPIO.output(LED,GPIO.LOW)
GPIO.cleanup()
