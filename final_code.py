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
US_TRIG1 = 8
US_ECHO1 = 10
GPIO.setup(US_TRIG1, GPIO.OUT)
GPIO.setup(US_ECHO1, GPIO.IN)
# UltraSonic 2
US_TRIG2 = 16
US_ECHO2 = 18
GPIO.setup(US_TRIG2, GPIO.OUT)
GPIO.setup(US_ECHO2, GPIO.IN)
# UltraSonic 3
US_TRIG3 = 22
US_ECHO3 = 24
GPIO.setup(US_TRIG3, GPIO.OUT)
GPIO.setup(US_ECHO3, GPIO.IN)
# Servo 1
SERVO1 = 11
GPIO.setup(SERVO1, GPIO.OUT)
servo1 = GPIO.PWM(SERVO1, 50)

# Servo 2
SERVO2 = 13
GPIO.setup(SERVO2, GPIO.OUT)
servo2 = GPIO.PWM(SERVO2, 50)

status = "idle"
humanStanding = 0


def checkHuman():
    dis = ultrasonic.distance(US_TRIG1, US_ECHO1)
    if dis < 100:
        return True
    elif dis > 100:
        return False


def open_close():
    while True:
        if checkHuman() == True:
            print('open_close',)
            servoControl.RollToAngle(servo1, 90)
            time.sleep(3)
            continue
        else:
            servoControl.RollToAngle(servo1, 0)
            # threadClassify = threading.Thread(target=classify_garbage, args=())
            # threadClassify.start()
    # while True:
    #     if dist == 0:


def classify_garbage():
    if classify.gabIsEmpty == 0:
        classify.Classify()
    else:
        time.sleep(1)
        print('classify:', classify.labelExport)
    if classify.labelExport == 0:
        #servoControl.RollToAngle(servo2, 45)
        print("0")
    elif classify.labelExport == 1:
        #servoControl.RollToAngle(servo2, 135)
        print("1")
    else:
        print("2")
        #servoControl.RollToAngle(servo2, 90)
        # print('classify')
        # time.sleep(2)


def check_percent_garbage(trig, echo):
    while True:
        dis = ultrasonic.distance(trig, echo)
        heightAtEmpty = 100
        percent = 100-(dis/heightAtEmpty)*100
        print("percent", percent)
        # return 100-(dis/heightAtEmpty)*100
        # print('checkpercent')
        try:
            firebase.updateTrashPercent("inorganic", percent)
        except:
            print('error posting firebase')

        time.sleep(1)


if __name__ == '__main__':
    try:
        threadCheckPercent = threading.Thread(
            target=check_percent_garbage, args=(US_TRIG2, US_ECHO2))
        threadCheckPercent.start()

        threadOpenClose = threading.Thread(target=open_close, args=())
        threadOpenClose.start()

    except KeyboardInterrupt:
        # #         threadClassify.join()
        threadOpenClose.stop()
        threadCheckPercent.stop()
        GPIO.cleanup()
        print('done')
