print("     MODÜLLER")
print("1 - DC Motor")
print("2 - Mesafe Sensörü")
print("3 - Gemi Hareket")
print("4 - Step Motor")
print("5 - Görüntü işleme")
print("---------------GEMİ CİHAZLARI DENEME----------------")
print("6 - Gemi Motorları çalıştır")
print("7 - Yatay Sensör")
print("8 - Çapraz Sensör")
print("9 - Römork Step Motor")
print("10 - Doldurma Çubuğu Step Motor")
print("11 - Boşaltma Çubuğu Step Motor")

secenek = int(input("Kullanmak istediginiz modülün numarasını giriniz:"))

if secenek == 1:
    print("DC Motor seçildi. DC Motor örnek çalışma başlıyor...")

    import RPi.GPIO as GPIO
    from time import sleep
    import lib_dc_motor as dc

    GPIO.setmode(GPIO.BOARD)

    # İlk iki pin ileri-geri'yi yönetiyor
    # Üçüncü pin motorun çalışıp çalışmadığını
    motorA = [3, 5, 7]
    motorB = [11, 13, 15]
    dc.pin_ayarla(motorA)
    dc.pin_ayarla(motorB)
    print("İleri")
    dc.ileri(motorA)
    dc.ileri(motorB)
    sleep(10)
    print("Geri")
    dc.geri(motorA)
    dc.geri(motorB)
    sleep(10)
    print("Dur")
    dc.durdur(motorA)
    dc.durdur(motorB)
    GPIO.cleanup()

elif secenek == 2:
    print("Mesafe Sensörü seçildi. 15 sn HC-SR04 Mesafe Sensörü örnek çalışma başlıyor...")

    import RPi.GPIO as GPIO
    import time
    import lib_mesafe_sensoru as ms

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    print("Mesafe sensörü ayarlanıyor...")
    ms.pin_ayarla([8, 10])

    for i in range(0, 15):

        print("Olculuyor...")
        time.sleep(1)

        mesafe = ms.mesafe_olc([8, 10])

        if mesafe < 2:
            print("Mesafe fazla yakın!")
        elif mesafe > 400:
            print("Mesafe fazla uzak!")
        else:
            print("Mesafe:", mesafe - 0.5, "cm")

    GPIO.cleanup()

elif secenek == 3:
    print("Gemi Hareket modülü seçildi. Gemi Hareketleri örnek çalışma başlıyor...")

    import RPi.GPIO as GPIO
    import lib_gemi_hareket as gemi
    import time as t

    GPIO.setmode(GPIO.BOARD)

    print("Gemi ayarlanıyor...")
    gemi.motor_pinleri_ayarla([8, 10, 12], [11, 13, 15])

    print("5 sn tam gaz ileri git...")
    gemi.ileri()
    t.sleep(5)

    print("5 sn tam gaz sola dön...")
    gemi.sola_don()
    t.sleep(5)

    print("5 sn tam gaz sağa dön...")
    gemi.saga_don()
    t.sleep(5)

    print("5 sn tam gaz geri git...")
    gemi.geri()
    t.sleep(5)

    print("Motorlar kapatiliyor...")
    gemi.dur()

    GPIO.cleanup()

elif secenek == 4:
    print("Step Motor seçildi. Step Motor örnek çalışma başlıyor...")

    import RPi.GPIO as GPIO
    import lib_step_motor as step

    GPIO.setmode(GPIO.BOARD)

    kontrolPinleri = [32, 36, 38, 40]
    step.motor_pinlerini_ayarla(kontrolPinleri)

    tur = float(input("Tur sayısını giriniz (negatif->ters yön): "))
    bekleme = int(input("Bekleme süresini giriniz (ms): "))
    step.tam_tur_don(tur, bekleme, kontrolPinleri)

    GPIO.cleanup()

elif secenek == 5:
    import time
    import cv2
    import numpy as np
    import lib_sabitler as sbt
    import lib_cv_yardimci as cvYar

    kamera = cv2.VideoCapture("Medya/Kayitlar/temizKayit4.avi")
    while True:
        _, anaResim = kamera.read()
        anaResim = cv2.resize(anaResim, (sbt.CV_COZUNURLUGU[0], sbt.CV_COZUNURLUGU[1]))

        def sur_bul_ve_hareket_et(resim):
            surResim = resim.copy()

            img_hsv = cv2.cvtColor(surResim, cv2.COLOR_BGR2HSV)

            # lower mask (0-10)
            lower_red = np.array([0, 50, 50])
            upper_red = np.array([10, 255, 255])
            mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

            # upper mask (170-180)
            lower_red = np.array([170, 50, 50])
            upper_red = np.array([180, 255, 255])
            mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

            # join my masks
            surMaske = mask0 + mask1
            # surMaske = cvYar.maske_olustur(surResim, cvYar.renk_siniri["sur"], cvYar.cekirdek)
            surAlanlar = cvYar.cerceve_ciz(surResim, surMaske)
            enBuyukSur = cvYar.en_buyugu_bul(surAlanlar)
            # cismin etrafına dikdörtgen çizme
            cv2.rectangle(surResim, (enBuyukSur['solUstKose'][0], enBuyukSur['solUstKose'][1]),
                          (enBuyukSur["sagAltKose"][0], enBuyukSur["sagAltKose"][1]), (255, 0, 0), 3)

            return surResim


        surResim = sur_bul_ve_hareket_et(anaResim)
        cv2.imshow("Sur", surResim)
        if cv2.waitKey(80) == 27:
            break
    kamera.release()
    cv2.destroyAllWindows()

elif secenek == 6:
    print("Gemi motorlarını çalıştırma testi seçildi...")
    from time import sleep
    import RPi.GPIO as GPIO
    import lib_sabitler as sbt
    import lib_gemi_hareket as gemi

    GPIO.setmode(GPIO.BOARD)

    gemi.motorlari_ayarla()

    sure = int(input("Kaç sn ileri gitsin: "))
    gemi.ileri()
    sleep(sure)

    sure = int(input("Kaç sn geri gitsin: "))
    gemi.geri()
    sleep(sure)

    gemi.dur()
    print("Gemi motorlari çalıştırma testi bitti...")

elif secenek == 7:
    print("Yatay sensör seçildi, 15sn mesafeyi gösterecek...")
    from time import sleep
    import RPi.GPIO as GPIO
    import lib_sabitler as sbt
    import lib_mesafe_sensoru as ms

    GPIO.setmode(GPIO.BOARD)
    ms.pin_ayarla(sbt.PIN_SENSOR_YATAY)
    for i in range(15):
        mesafe = ms.mesafe_olc([8, 10])
        if mesafe < 2:
            print("Mesafe fazla yakın!")
        elif mesafe > 400:
            print("Mesafe fazla uzak!")
        else:
            print("Mesafe:", mesafe - 0.5, "cm")
        sleep(1)

elif secenek == 8:
    print("Çapraz sensör seçildi, 15sn mesafeyi gösterecek...")
    from time import sleep
    import RPi.GPIO as GPIO
    import lib_sabitler as sbt
    import lib_mesafe_sensoru as ms

    GPIO.setmode(GPIO.BOARD)
    ms.pin_ayarla(sbt.PIN_CAPRAZ_YATAY)
    for i in range(15):
        mesafe = ms.mesafe_olc([8, 10])
        if mesafe < 2:
            print("Mesafe fazla yakın!")
        elif mesafe > 400:
            print("Mesafe fazla uzak!")
        else:
            print("Mesafe:", mesafe - 0.5, "cm")
        sleep(1)

elif secenek == 9:
    print("Römork Step Motoru seçildi...")
    import RPi.GPIO as GPIO
    import lib_sabitler as sbt
    import lib_step_motor as step

    GPIO.setmode(GPIO.BOARD)

    step.motor_pinlerini_ayarla(sbt.PIN_STEP_ROMORK)
    tur = float(input("Tur sayısını giriniz (negatif->ters yön): "))
    step.tam_tur_don(tur, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.PIN_STEP_ROMORK)

    GPIO.cleanup()

elif secenek == 10:
    print("Doldurma Çubuğu Step Motoru seçildi...")
    import RPi.GPIO as GPIO
    import lib_sabitler as sbt
    import lib_step_motor as step

    GPIO.setmode(GPIO.BOARD)

    step.motor_pinlerini_ayarla(sbt.PIN_STEP_DOLDURMA_CUBUGU)
    tur = float(input("Tur sayısını giriniz (negatif->ters yön): "))
    step.tam_tur_don(tur, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.PIN_STEP_DOLDURMA_CUBUGU)

    GPIO.cleanup()

elif secenek == 11:
    print("Boşaltma Çubuğu Step Motoru seçildi...")
    import RPi.GPIO as GPIO
    import lib_sabitler as sbt
    import lib_step_motor as step

    GPIO.setmode(GPIO.BOARD)

    step.motor_pinlerini_ayarla(sbt.PIN_STEP_BOSALTMA_CUBUGU)
    tur = float(input("Tur sayısını giriniz (negatif->ters yön): "))
    step.tam_tur_don(tur, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.PIN_STEP_BOSALTMA_CUBUGU)

    GPIO.cleanup()

else:
    print("Hatalı giriş yaptınız. Programı tekrar alıştırınız.")
