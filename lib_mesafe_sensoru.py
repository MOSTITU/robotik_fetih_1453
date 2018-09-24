# Mesafe sensörüyle rahatça işlem yapabilmek için oluşturulmuş modül
import RPi.GPIO as GPIO
import time


# Mesafe sensörünün bağlı olduğu pinleri ayarla
def pin_ayarla(pinler):
    triggerPin = pinler[0]
    echoPin = pinler[1]

    GPIO.setup(triggerPin, GPIO.OUT)
    GPIO.setup(echoPin, GPIO.IN)

    GPIO.output(triggerPin, False)


# Dalga gönder, gelmesini bekle, arada geçen zamanı ölç
def dalga_git_gel(pinler):
    triggerPin = pinler[0]
    echoPin = pinler[1]

    GPIO.output(triggerPin, True)
    time.sleep(0.00001)
    GPIO.output(triggerPin, False)

    while GPIO.input(echoPin) == 0:
        dalga_gonderis = time.time()

    while GPIO.input(echoPin) == 1:
        dalga_gelis = time.time()

    return dalga_gelis - dalga_gonderis


# Dalga gidiş-gelişi arasındaki mesafeden mesafeyi hesapla
# Bu işlem dalganın havada yayılma hızına göre yapılır.
def mesafe_hesapla(sure):
    mesafe = sure * 17150
    return round(mesafe, 2)


# Tek fonksiyonla mesafeyi ölç ve döndür
def mesafe_olc(pinler):
    return mesafe_hesapla(dalga_git_gel(pinler))
