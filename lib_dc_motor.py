import RPi.GPIO as GPIO


# DC Motor'un bağlı olduğu pinleri ayarla
def pin_ayarla(pinler):
    for pin in pinler:
        GPIO.setup(pin, GPIO.OUT)


# pinler -> 3 elemanlı liste
# Motorun ileri önde hareketini sağla
def ileri(pinler):
    GPIO.output(pinler[0], GPIO.HIGH)
    GPIO.output(pinler[1], GPIO.LOW)
    GPIO.output(pinler[2], GPIO.HIGH)


# pinler -> 3 elemanlı liste
# Motorun geri yönde hareketini sağla
def geri(pinler):
    GPIO.output(pinler[0], GPIO.LOW)
    GPIO.output(pinler[1], GPIO.HIGH)
    GPIO.output(pinler[2], GPIO.HIGH)


# Motoru durdur
def durdur(pinler):
    GPIO.output(pinler[2], GPIO.LOW)
