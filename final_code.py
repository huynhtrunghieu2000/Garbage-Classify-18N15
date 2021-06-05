import RPi.GPIO as GPIO
import servoControl
import ultrasonic
import garbage_classify as classify
import threading
from threading import Thread
import time
import firebase

GPIO.setmode(GPIO.BOARD)

# UltraSonic 1
US_TRIG1 = 18
US_ECHO1 = 24
GPIO.setup(US_TRIG1, GPIO.OUT)
GPIO.setup(US_TRIG1, GPIO.IN)
# UltraSonic 2
US_TRIG2 = 18
US_ECHO2 = 24
GPIO.setup(US_TRIG2, GPIO.OUT)
GPIO.setup(US_ECHO2, GPIO.IN)
# UltraSonic 3
US_TRIG3 = 18
US_ECHO3 = 24
GPIO.setup(US_TRIG3, GPIO.OUT)
GPIO.setup(US_ECHO3, GPIO.IN)
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
        dis = ultrasonic.distance(US_TRIG1, US_ECHO1)
        if dis < 100:
            servoControl.RollToAngle(servo1, 90)
            time.sleep(3)
        if dis > 100:
            servoControl.RollToAngle(servo1, 0)
    # while True:
    #     if dist == 0:


def classify_garbage():
    while True:
        classify.Classify()
        time.sleep(1)
        if classify.labelExport == 0:
            servoControl.RollToAngle(servo2, 45)
        elif classify.labelExport == 1:
            servoControl.RollToAngle(servo2, 135)
        elif classify.labelExport == 2:
            servoControl.RollToAngle(servo2, 90)
        # print('classify')
        # time.sleep(2)


def check_percent_garbage(trig, echo):
    while True:
        dis = ultrasonic.distance(trig, echo)
        heightAtEmpty = 100
        percent = 100-(dis/heightAtEmpty)*100
        print(percent)
        # return 100-(dis/heightAtEmpty)*100
        # print('checkpercent')
        try:
            firebase.updateTrashPercent("inorganic", percent)
        except:
            print('error posting firebase')

        time.sleep(1)


if __name__ == '__main__':
    try:
        threadOpenClose = threading.Thread(target=open_close, args=())
        threadCheckPercent = threading.Thread(
            target=check_percent_garbage, args=(US_TRIG2, US_ECHO2))
        threadClassify = threading.Thread(target=classify_garbage, args=())
        threadOpenClose.start()
        threadClassify.start()
        threadCheckPercent.start()
    except KeyboardInterrupt:
        print('done')
        GPIO.cleanup()
