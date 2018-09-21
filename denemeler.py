print("     MODÜLLER")
print("1 - DC Motor")
print("2 - Mesafe Sensörü")
print("3 - Gemi Hareket")
print("4 - Step Motor")

secenek = int(input("Kullanmak istediginiz modülün numarasını giriniz:"))

if secenek == 1:
    print("DC Motor seçildi. DC Motor örnek çalışma başlıyor...")

    import RPi.GPIO as GPIO
    from time import sleep
    import lib_dc_motor as dc

    GPIO.setmode(GPIO.BOARD)

    # İlk iki pin ileri-geri'yi yönetiyor
    # Üçüncü pin motorun çalışıp çalışmadığını
    motorA = [8, 10, 12]

    dc.pin_ayarla(motorA)

    dc.gucu_degistir(motorA, 45)
    dc.ileri(motorA)
    sleep(3)
    dc.durdur(motorA)
    print("hızlan")
    dc.gucu_degistir(motorA, 100)
    dc.ileri(motorA)
    sleep(3)

    dc.durdur(motorA)

    GPIO.cleanup()

elif secenek == 2:
    print("Mesafe Sensörü seçildi. 15 sn HC-SR04 Mesafe Sensörü örnek çalışma başlıyor...")

    import RPi.GPIO as GPIO
    import time
    import lib_mesafe_sensoru as ms

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    print("Mesafe sensörü ayarlanıyor...")
    ms.pin_ayarla([16, 18])

    for i in range(0, 15):

        print("Olculuyor...")
        time.sleep(1)

        mesafe = ms.mesafe_olc([16, 18])

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

elif (secenek == 4):
    print("Step Motor seçildi. Step Motor örnek çalışma başlıyor...")

    import RPi.GPIO as GPIO
    import lib_step_motor as step

    GPIO.setmode(GPIO.BOARD)

    kontrolPinleri = [31, 33, 35, 37]
    step.motor_pinlerini_ayarla(kontrolPinleri)

    tur = float(input("Tur sayısını giriniz (negatif->ters yön): "))
    bekleme = int(input("Bekleme süresini giriniz (ms): "))
    step.tam_tur_don(tur, bekleme, kontrolPinleri)

    GPIO.cleanup()

else:
    print("Hatalı giriş yaptınız. Programı tekrar alıştırınız.")
