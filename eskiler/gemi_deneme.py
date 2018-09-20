import lib_gemi_hareket as gemi
import time as t
import lib_mesafe_sensoru as ms
import RPi.GPIO as GPIO
print("Mission start...")

GPIO.setmode(GPIO.BOARD)


gemi.motorlari_ayarla()
baslangic = t.time()
kisalt = 0

while True:
	simdi = t.time()
	zaman = simdi - baslangic - kisalt

	mesafe = ms.hizli_hesapla()

	if(zaman.is_integer()):
		print("Zaman:", zaman, "\tMesafe:",mesafe)

	if (mesafe < 15):
		print("Mesafe 5'ten az, 5sn uyuma vakti.")
		kisalt += 5
		t.sleep(5)

	if (zaman < 5):
		gemi.ileri()
	elif (zaman >= 5 and zaman < 10):
		gemi.sola_don()
	elif (zaman >= 10 and zaman < 15):
		gemi.saga_don()
	elif (zaman >= 15 and zaman < 20):
		gemi.dur()
	elif (zaman >= 20 and zaman < 25):
		gemi.geri()
	else:
		gemi.dur()
		break

print("Mission complete :D")