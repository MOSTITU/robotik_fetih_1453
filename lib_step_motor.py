import RPi.GPIO as GPIO
import time


# Motor pinlerini ayarlar
def motor_pinlerini_ayarla(motorPinleri):
    for pin in motorPinleri:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)


# turSayisi negatif ise geri (saat yönünün tersine) döner
# turSayisi float olabilir.
# beklemeSuresi milisaniye cinsindendir.
# motorPinleri 4 tane motor pininin listesidir.
def tam_tur_don(turSayisi, beklemeSuresi, motorPinleri):
    beklemeSuresi = beklemeSuresi * 0.001
    if beklemeSuresi < 0:  beklemeSuresi *= -1

    yarimAdimDizisi = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]
    ]

    if turSayisi < 0:
        turSayisi *= -1
        yarimAdimDizisi.reverse()

    for i in range(int(turSayisi * 512)):
        for yarimAdim in range(8):
            for pin in range(4):
                GPIO.output(motorPinleri[pin], yarimAdimDizisi[yarimAdim][pin])
            time.sleep(beklemeSuresi)
