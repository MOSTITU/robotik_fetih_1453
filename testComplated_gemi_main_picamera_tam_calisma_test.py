from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import lib_gemi_hareket as gh
import RPi.GPIO as GPIO
import lib_tespit_ve_hareket as th

GPIO.setmode(GPIO.BOARD)
gh.motorlari_ayarla()

# Kamera kutuphanesinden bir nesne al ve kamera degiskenine ata
kamera = PiCamera()

# Kayıt/İşlem çözünürlüğü
kayitCozunurlugu = [640, 480]
islemCozunurlugu = [340, 220]
kamera.resolution = (kayitCozunurlugu[0], kayitCozunurlugu[1])

# Kameranin saniyedeki resim sayisini 50 olarak ayarla
kamera.framerate = 50

# # Kamera kablo baglantisindan dolayi ters durdugu ve goruntu ters gozukecegi icin goruntuyu ters cevir
# kamera.vflip = True

# Resimleri tutmak icin bellekte yer ac
resimBellegi = PiRGBArray(kamera, size=(kayitCozunurlugu[0], kayitCozunurlugu[1]))

# Kameranin hazir olmasi icin biraz bekle
time.sleep(0.1)

# Video kaydı için
kayitTime = time.strftime("%Y-%m-%d-%H-%M")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
temizKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'temizKayit.avi', fourcc, 10.0, (kayitCozunurlugu[0], kayitCozunurlugu[1]))
duvarKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'duvarKayit.avi', fourcc, 10.0, (islemCozunurlugu[0], islemCozunurlugu[1]))
gemiKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'gemiKayit.avi', fourcc, 10.0, (islemCozunurlugu[0], islemCozunurlugu[1]))
kapiKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'kapiKayit.avi', fourcc, 10.0, (islemCozunurlugu[0], islemCozunurlugu[1]))
surKayit = cv2.VideoWriter('./Medya/Kayitlar/' + kayitTime + 'surKayit.avi', fourcc, 10.0, (islemCozunurlugu[0], islemCozunurlugu[1]))

# Gemi toplama/boşaltma işlemi için
gemiTopla = True
gemiBosalt = False

# Bir for dongusu icinde kameradan resim yakalamaya basla
for resimKaresi in kamera.capture_continuous(resimBellegi, format="bgr", use_video_port=True):
    # Resim karesinin piksellerini resim isimli bir degiskene yaz
    anaResim = resimKaresi.array
    temizKayit.write(anaResim)
    anaResim = cv2.resize(anaResim, (islemCozunurlugu[0], islemCozunurlugu[1]))

    if gemiTopla:
        gemiResim = th.gemi_bul_ve_hareket_et(anaResim)
        gemiKayit.write(gemiResim)
        cv2.imshow("Gemiler", gemiResim)

    if gemiBosalt:
        kapiResim = th.kapi_bul_ve_hareket_et(anaResim)
        kapiKayit.write(kapiResim)
        cv2.imshow("Kapı", kapiResim)

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
