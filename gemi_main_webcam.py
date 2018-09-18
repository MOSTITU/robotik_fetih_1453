# TODO Son gelişmeler gemi_main_picamera'dan alınacak.
# TODO Kameraya göre resmi çevirme yapılacak.
aynaEtkisi = False

import cv2
import lib_gemi_hareket as gh
import lib_cv_yardimci as yar
import os
import RPi.GPIO as GPIO
import lib_tespit_sonrasi as ts

GPIO.setmode(GPIO.BOARD)
gh.motorlari_ayarla()

# kamera açılır, kamera açılamazsa video açılır
kamera = cv2.VideoCapture(1)
if not kamera.isOpened():
    kamera = cv2.VideoCapture(0)
if not kamera.isOpened():
    kamera = cv2.VideoCapture("./Medya/smile.mp4")

kayitSayisi = int(len(os.listdir('./Medya/Kayitlar')) / 2)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
temizKayit = cv2.VideoWriter('./Medya/Kayitlar/temizKayit' + str(kayitSayisi) + '.avi', fourcc, 10.0, (640, 480))
islenmisKayit = cv2.VideoWriter('./Medya/Kayitlar/islenmisKayit' + str(kayitSayisi) + '.avi', fourcc, 10.0, (340, 220))

while True:
    _, resim = kamera.read()
    temizKayit.write(resim)

    # Ayna etkisi
    if aynaEtkisi:
        resim = cv2.flip(resim, 1)

    resim = cv2.resize(resim, (340, 220))

    gemiMaske = yar.maske_olustur(resim, yar.renk_siniri["yesil"], yar.cekirdek)
    gemiAlanlar = yar.cerceve_ciz(resim, gemiMaske)

    # print("Tespit edilen cisim sayisi:", len(gemiAlanlar))
    enBuyukGemi = yar.en_buyugu_bul(gemiAlanlar)

    # cismin etrafına dikdörtgen çizme
    cv2.rectangle(resim, (enBuyukGemi['solUstKose'][0], enBuyukGemi['solUstKose'][1]),
                  (enBuyukGemi["sagAltKose"][0], enBuyukGemi["sagAltKose"][1]), (255, 0, 0), 3)
    ts.goruntuye_gore_hareket(resim, enBuyukGemi)

    islenmisKayit.write(resim)
    cv2.imshow("Video", resim)
    if cv2.waitKey(20) == 27:
        break

# GPIO cikislarini kapat
GPIO.cleanup()

kamera.release()
temizKayit.release()
islenmisKayit.release()
cv2.destroyAllWindows()
