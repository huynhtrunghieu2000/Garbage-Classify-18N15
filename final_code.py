import RPi.GPIO as GPIO
import servoControl
import garbage_classify as classify
import threading
from threading import Thread
import time

GPIO.setmode(GPIO.BOARD)

# UltraSonic 1
US_TRIG1 = 18
US_ECHO1 = 24
GPIO.setup(US_TRIG1, GPIO.OUT)
GPIO.setup(US_TRIG1, GPIO.IN)
# UltraSonic 2
US_TRIG2 = 18
US_ECHO2 = 24
GPIO.setup(US_TRIG1, GPIO.OUT)
GPIO.setup(US_TRIG1, GPIO.IN)
# UltraSonic 3
US_TRIG3 = 18
US_ECHO3 = 24
GPIO.setup(US_TRIG1, GPIO.OUT)
GPIO.setup(US_TRIG1, GPIO.IN)
# Servo 1
SERVO1 = 11
GPIO.setup(SERVO1, GPIO.OUT)
servo1 = GPIO.PWM(SERVO1, 50)

# Servo 2
SERVO2 = 12
GPIO.setup(SERVO2, GPIO.OUT)
servo2 = GPIO.PWM(SERVO2, 50)


def open_close():
    while True:
        if dist == 0:


def classify_garbage():
    print('')


def check_percent_garbage():
    print('')


if __name__ == '__main__':
    try:
        threadOpenClose = threading.Thread(target=open_close, args=())
        threadCheckPercent = threading.Thread(
            target=check_percent_garbage, args=())
    except KeyboardInterrupt:
        GPIO.cleanup()
