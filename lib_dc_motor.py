import RPi.GPIO as GPIO


def pin_ayarla(pinler):
    for pin in pinler:
        GPIO.setup(pin, GPIO.OUT)


# pinler -> 3 elemanlı liste
def ileri(pinler):
    GPIO.output(pinler[0], GPIO.HIGH)
    GPIO.output(pinler[1], GPIO.LOW)
    GPIO.output(pinler[2], GPIO.HIGH)


# pinler -> 3 elemanlı liste
def geri(pinler):
    GPIO.output(pinler[0], GPIO.LOW)
    GPIO.output(pinler[1], GPIO.HIGH)
    GPIO.output(pinler[2], GPIO.HIGH)


def durdur(pinler):
    GPIO.output(pinler[2], GPIO.LOW)
