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

# Kameranin saniyedeki resim sayisini 50 olarak ayarla
kamera.framerate = 50

# # Kamera kablo baglantisindan dolayi ters durdugu ve goruntu ters gozukecegi icin goruntuyu ters cevir
# kamera.vflip = True

# Resimleri tutmak icin bellekte yer ac
resimBellegi = PiRGBArray(kamera)

# Kameranin hazir olmasi icin biraz bekle
time.sleep(0.1)

# Bir for dongusu icinde kameradan resim yakalamaya basla
for resimKaresi in kamera.capture_continuous(resimBellegi, format="bgr", use_video_port=True):
    # Resim karesinin piksellerini resim isimli bir degiskene yaz
    anaResim = resimKaresi.array
    anaResim = cv2.resize(anaResim, (340, 220))

    # gemiResim = anaResim.copy()
    # gemiMaske = yar.maske_olustur(gemiResim, yar.renk_siniri["yesil"], yar.cekirdek)
    # gemiAlanlar = yar.cerceve_ciz(gemiResim, gemiMaske)
    # enBuyukGemi = yar.en_buyugu_bul(gemiAlanlar)
    # # cismin etrafına dikdörtgen çizme
    # cv2.rectangle(gemiResim, (enBuyukGemi['solUstKose'][0], enBuyukGemi['solUstKose'][1]),
    #               (enBuyukGemi["sagAltKose"][0], enBuyukGemi["sagAltKose"][1]), (255, 0, 0), 3)
    # ts.goruntuye_gore_hareket(gemiResim, enBuyukGemi)

    kapiResim = anaResim.copy()
    kapiMaske = yar.maske_olustur(kapiResim, yar.renk_siniri["yesil"], yar.cekirdek)
    kapiAlanlar = yar.cerceve_ciz(kapiResim, kapiMaske)
    _, kapiMerkez, kapiYon, s1, s2 = yar.kapiyi_tespit_et(kapiAlanlar)
    # Sütunları dikdörtgen içine alma
    cv2.rectangle(kapiResim, (s1['solUstKose'][0], s1['solUstKose'][1]),
                  (s1["sagAltKose"][0], s1["sagAltKose"][1]), (255, 0, 0), 3)
    cv2.rectangle(kapiResim, (s2['solUstKose'][0], s2['solUstKose'][1]),
                  (s2["sagAltKose"][0], s2["sagAltKose"][1]), (255, 0, 0), 3)
    
    
    # cv2.imshow("Gemiler", gemiResim)
    cv2.imshow("Kapı", kapiResim)
    cv2.imshow("Ana Resim", anaResim)
    resimBellegi.truncate(0)
    if cv2.waitKey(20) == 27:
        break

# GPIO cikislarini kapat
GPIO.cleanup()

cv2.destroyAllWindows()
