# Kullanılan pinler ->
# Stepler -> [31, 33, 35, 37], [32, 36, 38, 40]
# Sensörler -> [16,18] , [11,13]
# Motorlar -> [8, 10, 12], [3, 5, 7]
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import RPi.GPIO as GPIO
import lib_sabitler as sbt
import lib_step_motor as sm
import lib_gemi_hareket as gh
import lib_mesafe_sensoru as ms
import lib_tespit_ve_hareket as th


GPIO.setmode(GPIO.BOARD)
gh.motorlari_ayarla()
# Çarpraz sensör
ms.pin_ayarla(sbt.CAPRAZ_SENSOR_PIN)
# Direk aşağı sensör
ms.pin_ayarla(sbt.DIKEY_SENSOR_PIN)
sm.motor_pinlerini_ayarla(sbt.BANT_PIN)
sm.motor_pinlerini_ayarla(sbt.ON_KOL_PIN)
# Kapalı olan kollar açılıyor.
sm.tam_tur_don(sbt.ON_KOL_TUR_SAYISI, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.ON_KOL_PIN)

# Kamera kutuphanesinden bir nesne al ve kamera degiskenine ata
kamera = PiCamera()

# Kayıt/İşlem çözünürlüğü
kamera.resolution = (sbt.KAMERA_COZUNURLUGU[0], sbt.KAMERA_COZUNURLUGU[1])

# Kameranin saniyedeki resim sayisini 50 olarak ayarla
kamera.framerate = 50

# # Kamera kablo baglantisindan dolayi ters durdugu ve goruntu ters gozukecegi icin goruntuyu ters cevir
# kamera.vflip = True

# Resimleri tutmak icin bellekte yer ac
resimBellegi = PiRGBArray(kamera, size=(sbt.KAMERA_COZUNURLUGU[0], sbt.KAMERA_COZUNURLUGU[1]))

# Kameranin hazir olmasi icin biraz bekle
time.sleep(0.1)

# Video kaydı için
kayitTime = time.strftime("%Y-%m-%d-%H-%M")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
temizKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'temizKayit.avi', fourcc, 10.0, (sbt.KAMERA_COZUNURLUGU[0], sbt.KAMERA_COZUNURLUGU[1]))
duvarKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'duvarKayit.avi', fourcc, 10.0, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))
gemiKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'gemiKayit.avi', fourcc, 10.0, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))
kapiKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'kapiKayit.avi', fourcc, 10.0, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))
surKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'surKayit.avi', fourcc, 10.0, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))

# Gemi toplama/boşaltma işlemi için
gemiTopla = True
gemiBosalt = False
toplananGemiSayisi = 0
maxGemiKapasitesi = 2
bandaTirman = False

# Bir for dongusu icinde kameradan resim yakalamaya basla
for resimKaresi in kamera.capture_continuous(resimBellegi, format="bgr", use_video_port=True):
    # Resim karesinin piksellerini resim isimli bir degiskene yaz
    anaResim = resimKaresi.array
    temizKayit.write(anaResim)
    anaResim = cv2.resize(anaResim, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))

    if gemiTopla:
        gemiResim = th.gemi_bul_ve_hareket_et(anaResim)
        if th.gemi_bulundu():
            th.gemi_topla()
            toplananGemiSayisi += 1
            # Geminin taşıma kapasitesi dolduysa gemi toplamayı bırak, gemi boşaltmaya başla.
            if toplananGemiSayisi >= maxGemiKapasitesi:
                gemiTopla = False
                gemiBosalt = True
        gemiKayit.write(gemiResim)
        cv2.imshow("Gemiler", gemiResim)

    if gemiBosalt:
        kapiResim = th.kapi_bul_ve_hareket_et(anaResim)
        gemiTopla = True
        gemiBosalt = False
        kapiKayit.write(kapiResim)
        cv2.imshow("Kapı (Gemi bosalt)", kapiResim)

    if bandaTirman:
        kapiResim = th.banda_tirman(anaResim)
        kapiKayit.write(kapiResim)
        cv2.imshow("Kapı (Banda tırman)", kapiResim)

    duvarResim = th.duvar_bul_ve_carpma(anaResim)

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
