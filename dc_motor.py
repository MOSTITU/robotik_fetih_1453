import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BOARD)

# İlk iki pin ileri-geri'yi yönetiyor
# Üçüncü pin motorun çalışıp çalışmadığını
pinler = [16,18,22]

pins_setup(pinler)

ileri(pinler, 5)
geri(pinler, 5)
durdur()
 
GPIO.cleanup()

def pins_setup(pinler):
	for pin in pinler:
		GPIO.setup(pin,GPIO.OUT)

# pinler -> 3 elemanlı liste
# sure -> saniye cinsinden
def ileri(pinler, sure):
	print "Ileri hareket"
	GPIO.output(pinler[0],GPIO.HIGH)
	GPIO.output(pinler[1],GPIO.LOW)
	GPIO.output(pinler[2],GPIO.HIGH)
	sleep(sure)

# pinler -> 3 elemanlı liste
# sure -> saniye cinsinden
def geri(pinler, sure):
	print "Geri hareket"
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor1B,GPIO.HIGH)
	GPIO.output(Motor1E,GPIO.HIGH)
	sleep(sure)

def durdur(pin):
	print "Motor durdu"
	GPIO.output(pin,GPIO.LOW)