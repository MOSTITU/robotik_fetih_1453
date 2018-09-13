import RPi.GPIO as GPIO
from time import sleep
 
def pin_ayarla(pinler):
	for pin in pinler:
		GPIO.setup(pin,GPIO.OUT)

# pinler -> 3 elemanlı liste
def ileri(pinler):
	GPIO.output(pinler[0],GPIO.HIGH)
	GPIO.output(pinler[1],GPIO.LOW)
	GPIO.output(pinler[2],GPIO.HIGH)

# pinler -> 3 elemanlı liste
def geri(pinler):
	GPIO.output(pinler[0],GPIO.LOW)
	GPIO.output(pinler[1],GPIO.HIGH)
	GPIO.output(pinler[2],GPIO.HIGH)

def durdur(pinler):
	GPIO.output(pinler[2],GPIO.LOW)

# guc -> 0-100 arasi olacak
def gucu_ayarla(pinler, guc):
	GPIO.PWM(pinler[2],100).start(guc)

def gucu_degistir(pinler, guc):
	GPIO.PWM(pinler[2],100).ChangeDutyCycle(guc)