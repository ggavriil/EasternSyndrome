import RPi.GPIO as GPIO
import time
import threading


# This is not a class. We are trying to emulate a singleton class 
# that controls access to the vibration motor.

# We could use a blocking queue to ensure "fairness". This is probably
# not required in this case as not a lot of threads will need to access
# the motor at the same time.

VIBR_PIN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(VIBR_PIN, GPIO.OUT)
lock = threading.Lock()


def vibrate(duration, repetitions, ltimeout):
    thread = threading.Thread(target = __vibrate, args = (duration, repetitions, ltimeout))
    thread.start()


def __vibrate(duration, repetitions, ltimeout):
    acq = lock.acquire(timeout=ltimeout)
    if not acq:
        return
    for i in range(repetitions):
        GPIO.output(VIBR_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(VIBR_PIN, GPIO.LOW)
        if i < repetitions - 1:
            time.sleep(duration)
    lock.release()

