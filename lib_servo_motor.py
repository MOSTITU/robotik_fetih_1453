# Servo motor normalde 5V ile çalışır. Ama daha fazla akım çekme olasılığına karşın harici bir güç kaynağıyla kullanılması tavsiye edilir.
# Harici güç kaynağı kullanılınca harici güç kaynağının GND'si ile RPi GND'si ortak bağlanması gerekiyor.
# PWM için sadece BCM18 pin'ini kullanabiliyoruz.

import RPi.GPIO as GPIO


# Diğer fonksiyonları kullanmak için pinleri_ayarla() fonksiyonunun dönüş değeri kullanılır (pwn)
def pinleri_ayarla(pin):
    GPIO.setup(pin, GPIO.OUT)
    pwn = GPIO.PWM(pin, 50)
    baslat(pwn)
    return pwn


def baslat(pwn):
    pwn.start(0)


def gucu_degistir(pwn, aci):
    duty = float(aci) / 10.0 + 2.5
    pwn.ChangeDutyCycle(duty)


def durdur(pwn):
    pwn.stop()
