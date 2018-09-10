import RPi.GPIO as GPIO
import time
 
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
 
GPIO.setup(27, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
 
 

def GPIOSiraVer():
  siralar = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]
  i = 0
  while True:
    i = (i + 1) %4
    yield siralar[i]

def motorDondur(adimSayisi, sira, sure):
  for adim in range(adimSayisi):
    cikislar = next(sira)
    GPIO.output(27, cikislar[0])
    GPIO.output(29, cikislar[1])
    GPIO.output(31, cikislar[2])
    GPIO.output(33, cikislar[3])
    time.sleep(sure)

sira = GPIOSiraVer()

motorDondur(100,sira,0.01)

