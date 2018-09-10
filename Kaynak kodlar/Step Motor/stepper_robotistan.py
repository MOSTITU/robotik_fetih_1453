import RPi.GPIO as GPIO
import time
 
#GPIO.setmode(GPIO.BCM)
 
#enable_pin = 18
#coil_A_1_pin = 4
#coil_A_2_pin = 17
#coil_B_1_pin = 23
#coil_B_2_pin = 24
 
GPIO.setmode(GPIO.BOARD)
 
#enable_pin = 12
coil_A_1_pin = 7
coil_A_2_pin = 11
coil_B_1_pin = 13
coil_B_2_pin = 15
 
#GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.output(coil_A_1_pin, 0)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.output(coil_A_2_pin, 0)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.output(coil_B_1_pin, 0)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.output(coil_B_2_pin, 0)
 
#GPIO.output(enable_pin, 1)
 
def forward(delay, steps):  
  for i in range(0, steps):
    print("step:",i)
    setStep(1,0,0,0)
    setStep(1,1,0,0)
    setStep(0,1,0,0)
    setStep(0,1,1,0)
    setStep(0,0,1,0)
    setStep(0,0,1,1)
    setStep(0,0,0,1)
    setStep(1,0,0,1)
    time.sleep(delay)
 
def backwards(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(1, 0, 1, 0)
    time.sleep(delay)
 
  
def setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)
 



#delay = raw_input("Adim arasi bekleme suresi (milisaniye)?")
delay = 1
#steps = raw_input("Ileri kac adim? ")
steps = 512
forward(0.001, int(steps))
  

GPIO.cleanup()