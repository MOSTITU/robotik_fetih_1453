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
import lib_step_motor as step
import lib_gemi_hareket as gemi
import lib_mesafe_sensoru as ms
import lib_tespit_ve_hareket as th

print("Başlangıç ayarlamaları yapılıyor...")
GPIO.setmode(GPIO.BOARD)
th.butun_cihazlarin_pinlerini_ayarla()
th.baslangic_ayarlamalari()

print("Görüntü alınıyor...")
kamera = cv2.VideoCapture(0)

print("Video kaydı için hazırlıklar yapılıyor...")
# Video kaydı için
kayitTime = time.strftime("%Y-%m-%d-%H-%M")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
temizKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'temizKayit.avi', fourcc, 10.0, (sbt.KAMERA_COZUNURLUGU[0], sbt.KAMERA_COZUNURLUGU[1]))
duvarKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'duvarKayit.avi', fourcc, 10.0, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))
gemiKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'gemiKayit.avi', fourcc, 10.0, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))
kapiKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'kapiKayit.avi', fourcc, 10.0, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))
surKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'surKayit.avi', fourcc, 10.0, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))

print("Görevlere hazırlanılıyor...")
# Gemi toplama/boşaltma işlemi için
gemiTopla = True
gemiBosalt = False
toplananGemiSayisi = 0
maxGemiKapasitesi = 2
bandaTirman = False
bosaltmaSayisi = 0

# Bir for dongusu icinde kameradan resim yakalamaya basla
while True:
    _, anaResim = kamera.read()

    temizKayit.write(anaResim)
    anaResim = cv2.resize(anaResim, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))
    # # Ayna etkisi
    # anaResim = cv2.flip(anaResim, 1)

    print("Duvar tespit etme ve duvardan kaçınma...")
    duvarResim = th.duvar_bul_ve_carpma(anaResim)
    duvarKayit.write(duvarResim)
    cv2.imshow("Duvarlar", duvarResim)

    if gemiTopla:
        print("Gemi toplama aşaması...")
        gemiResim = th.gemi_bul_ve_hareket_et(anaResim)
        if th.gemi_bulundu():
            print("Gemi tespit edildi...")
            th.gemi_topla()
            toplananGemiSayisi += 1
            # Geminin taşıma kapasitesi dolduysa gemi toplamayı bırak, gemi boşaltmaya başla.
            if toplananGemiSayisi >= maxGemiKapasitesi:
                print("Kapasite doldu...")
                gemiTopla = False
                gemiBosalt = True
        gemiKayit.write(gemiResim)
        cv2.imshow("Gemiler", gemiResim)

    if gemiBosalt:
        print("Gemi boşaltma aşaması...")
        if not th.bant_bulundu():
            print("Bant tespit ediliyor, banda doğru hareket ediliyor...")
            kapiResim = th.kapi_bul_ve_hareket_et(anaResim)
            kapiKayit.write(kapiResim)
            cv2.imshow("Kapı (Gemi bosalt)", kapiResim)
        else:
            print("Banda gelindi, gemi boşaltılıyor")
            th.gemi_bosalt()
            bosaltmaSayisi += 1
            if bosaltmaSayisi>= 2:
                gemiTopla = False
                gemiBosalt = False
                bandaTirman = True
            else:
                gemiTopla = True
                gemiBosalt = False

    # TODO bandaTirman ne zaman True olacak?
    if bandaTirman:
        print("Banda tırmanma aşaması...")
        kapiResim = th.banda_tirman(anaResim)
        kapiKayit.write(kapiResim)
        cv2.imshow("Kapı (Banda tırman)", kapiResim)

    cv2.imshow("Temiz Görüntü", anaResim)

    if cv2.waitKey(20) == 27:
        break

print("Görev tamamlandı. Gemi kapatılıyor...")
# GPIO cikislarini kapat
GPIO.cleanup()

temizKayit.release()
duvarKayit.release()
gemiKayit.release()
kapiKayit.release()
surKayit.release()
kamera.release()
cv2.destroyAllWindows()
