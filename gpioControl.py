import RPi.GPIO as GPIO
import time
import garbage_classify as ras

GPIO.setmode(GPIO.BCM)
# Servo
servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)

# Ultra Sonic
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Classify by Servo


def classifyGB(label):
    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    p.start(2.5)  # Initialization
    try:
        if label[labels_id] == 1:
            # 7-> 90*
            p.ChangeDutyCycle(7)
            time.sleep(3)
            p.ChangeDutyCycle(3.8)
            time.sleep(3)
            p.ChangeDutyCycle(7)
        elif label[labels_id] == 0:
            p.ChangeDutyCycle(7)
            time.sleep(3)
            p.ChangeDutyCycle(9.4)
            time.sleep(3)
            p.ChangeDutyCycle(7)

    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()

# Get distance with Ultra Sonic Sensor


def distUltraSonic():
    GPIO.output(TRIG, False)


print('ok')
ras.main()
print("Chay main")
label = ras.labels
labels_id = ras.label_id
print(labels_id)
classifyGB(label)
