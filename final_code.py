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
servo1.start(0)

# Servo 2
SERVO2 = 13
GPIO.setup(SERVO2, GPIO.OUT)
servo2 = GPIO.PWM(SERVO2, 50)
servo2.start(0)

status = "idle"
humanStanding = 0


def checkHuman():
    dis = ultrasonic.distance(US_TRIG1, US_ECHO1)
    print(dis)
    if dis < 10:
        return True
    elif dis > 10:
        return False


def open_close():
    while True:
        if checkHuman() == True:
            print('open_close',)
            servoControl.RollToAngle(servo1, 90)
            time.sleep(3)
            classify.gabIsAvail = 1
        else:
            servoControl.RollToAngle(servo1, 0)
            if classify.gabIsAvail == 1:
                classify.count = 3
                threadClassify = threading.Thread(
                    target=classify_garbage, args=())
                threadClassify.start()
                threadClassify.join()


def classify_garbage():
    classify.Classify()
    if classify.labelExport == 0:
        servoControl.RollToAngle(servo2, 45)
        time.sleep(2)
        servoControl.RollToAngle(servo2, 90)
        time.sleep(2)
        servoControl.RollToAngle(servo2, 135)
        print("Huu Co xoayyy")
    elif classify.labelExport == 1:
#         servoControl.RollToAngle(servo2, 135)
        print("Vo co xoayyy")
    else:
        print("Undefined xoayyy")
#         servoControl.RollToAngle(servo2, 90)
        # print('classify')
        # time.sleep(2)


def check_percent_garbage(typeGb,height,trig, echo):
    while True:
        dis = ultrasonic.distance(trig, echo)
        percent = 100-(dis/height)*100
        print("percent", percent)
        # return 100-(dis/heightAtEmpty)*100
        # print('checkpercent')
        try:
            firebase.updateTrashPercent(typeGb, percent)
        except:
            print('error posting firebase')

        time.sleep(3)


if __name__ == '__main__':
    try:
        threadCheckPercentInOrganic = threading.Thread(
            target=check_percent_garbage, args=("inorganic",40,US_TRIG1, US_ECHO1))
        threadCheckPercent.start()
        
        threadCheckPercentOrganic = threading.Thread(
            target=check_percent_garbage, args=("organic",40,US_TRIG2, US_ECHO2))
        threadCheckPercent.start()

        threadOpenClose = threading.Thread(target=open_close, args=())
        threadOpenClose.start()
        
        threadCheckPercentInOrganic.join()
        threadCheckPercentOrganic.join()
        threadOpenClose.join()
        
        

    except:
        GPIO.cleanup()
        print('done')
