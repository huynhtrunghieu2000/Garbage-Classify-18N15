import threading
from threading import Thread
from time import sleep


def count10():
    i = 10
    while i >= 0:
        i = i-1
        print("Thread 1", i)
        sleep(1)


def count100():
    j = 1000
    while j >= 0:
        j = j-1
        print(j)
        sleep(1)
        t1 = threading.Thread(target=count10, args=()) 
        t1.start()
        sleep(5)
        t1.join()


# t1 = threading.Thread(
#     target=count10, args=())
# t1.start()

count100()
