import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

kontrolPinleri = [7,11,13,15]

motor_pinlerini_ayarla(kontrolPinleri)

tur = float(input("Tur sayısını giriniz (negatif->ters yön): "))
bekleme = int(input("Bekleme süresini giriniz (ms): "))

GPIO_temizle()

# Motor pinlerini ayarlar
def motor_pinlerini_ayarla(motorPinleri):
  for pin in motorPinleri:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# turSayisi negatif ise geri (saat yönünün tersine) döner
# turSayisi float olabilir.
# beklemeSuresi milisaniye cinsindendir.
# motorPinleri 4 tane motor pininin listesidir.
def tam_tur_dön(turSayisi, beklemeSuresi, motorPinleri):
  beklemeSuresi = beklemeSuresi * 0.001
  if(bekleme < 0):	bekleme *= -1

  yarimAdimDizisi = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
  ]

  if(turSayisi < 0):
    turSayisi *= -1
    yarimAdimDizisi.reverse()

  for i in range(int(turSayisi * 512)):
    for yarimAdim in range(8):
      for pin in range(4):
        GPIO.output(motorPinleri[pin], yarimAdimDizisi[yarimAdim][pin])
      time.sleep(beklemeSuresi)

def GPIO_temizle():
  GPIO.cleanup()