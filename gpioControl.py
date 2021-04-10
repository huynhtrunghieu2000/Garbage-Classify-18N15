import RPi.GPIO as GPIO
import time
import garbage_classify as ras


def quay(label):
    print('ok')
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

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


if __name__ == '__main__':
    print('ok')
    ras.main()
    label = ras.labels
    labels_id = ras.label_id
    quay(label)
