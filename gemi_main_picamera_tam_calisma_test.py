from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import lib_gemi_hareket as gh
import lib_cv_yardimci as yar
import os
import RPi.GPIO as GPIO
import lib_tespit_ve_hareket as th
import datetime

GPIO.setmode(GPIO.BOARD)
gh.motorlari_ayarla()

# Kamera kutuphanesinden bir nesne al ve kamera degiskenine ata
kamera = PiCamera()

# Kayıt çözünürlüğü
cozunurluk = [640, 480]
kamera.resolution = (cozunurluk[0], cozunurluk[1])
# Kameranin saniyedeki resim sayisini 50 olarak ayarla
kamera.framerate = 50

# # Kamera kablo baglantisindan dolayi ters durdugu ve goruntu ters gozukecegi icin goruntuyu ters cevir
# kamera.vflip = True

# Resimleri tutmak icin bellekte yer ac
resimBellegi = PiRGBArray(kamera, size=(cozunurluk[0], cozunurluk[1]))

# Kameranin hazir olmasi icin biraz bekle
time.sleep(0.1)

# Video kaydı için
kayitID = time.strftime("%Y-%m-%d-%H-%M")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
temizKayit = cv2.VideoWriter('./Medya/Kayitlar/temizKayit' + kayitID + '.avi', fourcc, 10.0, (640, 480))
duvarKayit = cv2.VideoWriter('./Medya/Kayitlar/duvarKayit' + kayitID + '.avi', fourcc, 10.0, (340, 220))
gemiKayit = cv2.VideoWriter('./Medya/Kayitlar/gemiKayit' + kayitID + '.avi', fourcc, 10.0, (340, 220))
kapiKayit = cv2.VideoWriter('./Medya/Kayitlar/kapiKayit' + kayitID + '.avi', fourcc, 10.0, (340, 220))
surKayit = cv2.VideoWriter('./Medya/Kayitlar/surKayit' + kayitID + '.avi', fourcc, 10.0, (340, 220))

# Gemi toplama/boşaltma işlemi için
gemiTopla = True
gemiBosalt = False

# Bir for dongusu icinde kameradan resim yakalamaya basla
for resimKaresi in kamera.capture_continuous(resimBellegi, format="bgr", use_video_port=True):
    # Resim karesinin piksellerini resim isimli bir degiskene yaz
    anaResim = resimKaresi.array
    anaResim = cv2.resize(anaResim, (340, 220))

    if gemiTopla:
        gemiResim = th.gemi_bul_ve_hareket_et(anaResim)
        gemiKayit.write(gemiResim)
        cv2.imshow("Gemiler", gemiResim)

    if gemiBosalt:
        kapiResim = th.kapi_bul_ve_hareket_et(anaResim)
        kapiKayit.write(kapiResim)
        cv2.imshow("Kapı", kapiResim)

    duvarResim = th.duvar_bul_ve_carpma(anaResim)

    temizKayit.write(anaResim)
    cv2.imshow("Temiz Görüntü", anaResim)
    duvarKayit.write(duvarResim)
    cv2.imshow("Duvarlar", duvarResim)

    resimBellegi.truncate(0)
    if cv2.waitKey(20) == 27:
        break

# GPIO cikislarini kapat
GPIO.cleanup()

temizKayit.release()
duvarKayit.release()
gemiKayit.release()
kapiKayit.release()
surKayit.release()
cv2.destroyAllWindows()
