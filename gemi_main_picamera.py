from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import lib_gemi_hareket as gh
import lib_cv_yardimci as yar
import os
import RPi.GPIO as GPIO
import lib_tespit_sonrasi as ts


GPIO.setmode(GPIO.BOARD)
gh.motorlari_ayarla()


# Kamera kutuphanesinden bir nesne al ve kamera degiskenine ata
kamera = PiCamera()

# # Kamera cozunurlugunu GENISLIKxUZUNLUK olarak ayarla
# kamera.resolution = (GENISLIK, UZUNLUK)

# Kameranin saniyedeki resim sayisini 50 olarak ayarla
kamera.framerate = 50

# # Kamera kablo baglantisindan dolayi ters durdugu ve goruntu ters gozukecegi icin goruntuyu ters cevir
# kamera.vflip = True

# Resimleri tutmak icin bellekte yer ac
# resimBellegi = PiRGBArray(kamera, size = (GENISLIK, UZUNLUK))
resimBellegi = PiRGBArray(kamera)

# Kameranin hazir olmasi icin biraz bekle
time.sleep(0.1)

# Bir for dongusu icinde kameradan resim yakalamaya basla
for resimKaresi in kamera.capture_continuous(resimBellegi, format="bgr", use_video_port=True):
    # Resim karesinin piksellerini resim isimli bir degiskene yaz
    resim = resimKaresi.array

    resim = cv2.resize(resim, (340, 220))

    gemiMaske = yar.maske_olustur(resim, yar.renk_siniri["yesil"], yar.cekirdek)
    gemiAlanlar = yar.cerceve_ciz(resim, gemiMaske)

    # print("Tespit edilen cisim sayisi:", len(gemiAlanlar))
    enBuyukGemi = yar.en_buyugu_bul(gemiAlanlar)

    # cismin etrafına dikdörtgen çizme
    cv2.rectangle(resim, (enBuyukGemi['solUstKose'][0], enBuyukGemi['solUstKose'][1]),
                  (enBuyukGemi["sagAltKose"][0], enBuyukGemi["sagAltKose"][1]), (255, 0, 0), 3)
    ts.goruntuye_gore_hareket(resim, enBuyukGemi)

    cv2.imshow("Video", resim)
    resimBellegi.truncate(0)
    if cv2.waitKey(20) == 27:
        break

# GPIO cikislarini kapat
GPIO.cleanup()

cv2.destroyAllWindows()