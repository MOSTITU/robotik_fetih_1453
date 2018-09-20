import RPi.GPIO as GPIO
import time


def pin_ayarla(triggerPin, echoPin):
    GPIO.setup(triggerPin, GPIO.OUT)
    GPIO.setup(echoPin, GPIO.IN)

    GPIO.output(triggerPin, False)


def dalga_git_gel(triggerPin, echoPin):
    GPIO.output(triggerPin, True)
    time.sleep(0.00001)
    GPIO.output(triggerPin, False)

    while GPIO.input(echoPin) == 0:
        dalga_gonderis = time.time()

    while GPIO.input(echoPin) == 1:
        dalga_gelis = time.time()

    return dalga_gelis - dalga_gonderis


def mesafe_hesapla(sure):
    mesafe = sure * 17150
    return round(mesafe, 2)


def mesafe_olc(triggerPin, echoPin):
    return mesafe_hesapla(dalga_git_gel(triggerPin, echoPin))
