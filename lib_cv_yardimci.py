import cv2
import numpy as np

# Renklerin alt ve üst sınırlarını tutan sözlük (dictionary) yapısı
renk_siniri = {
	"yesil" : [np.array([33,88,40]), np.array([102,255,255])],
	"mavi" : [np.array([100, 60, 60]), np.array([140, 255, 255])],
	"beyaz" : [np.array([0,0,140]), np.array([256,60,256])],
	"sari" : [np.array([5, 100, 100]), np.array([40, 255, 256])],
	"kirmizi" : [np.array([160,30,30]), np.array([180,255,255])],
    "mavi2": [np.array((80, 100, 70)), np.array((120, 180, 255))]
}

# 33. Ders - Erosion, Dilation, Opening, Closing
# Gürültüyü azaltma/arttırma
cekirdek = {
	"acik":np.ones((5, 5)), 
	"kapali":np.ones((20, 20))
}

# Maske olusturur, son maske değerini döndürür
def maske_olustur(resim, sinirlar, cekirdek):

	altSinir, ustSinir = sinirlar

	# BGR -> HSV dönüşümü
	resimHSV = cv2.cvtColor(resim, cv2.COLOR_BGR2HSV)

	# maske oluşturma
	maske = cv2.inRange(resimHSV, altSinir, ustSinir)

	# morfoloji (morphology)
	maskeAcik = cv2.morphologyEx(maske, cv2.MORPH_OPEN, cekirdek["acik"])
	maskeKapali = cv2.morphologyEx(maskeAcik, cv2.MORPH_CLOSE, cekirdek["kapali"])
	
	cv2.imshow("maskeKapali", maskeKapali)
	cv2.imshow("maskeAcik", maskeAcik)
	cv2.imshow("maske", maske)

	return maskeKapali

def cerceve_ciz(resim, maske):
	# Bulunan alanın çerçevesini alma
	_, cerceveler, h = cv2.findContours(maske.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	#Resme çerçeve çizme
	cv2.drawContours(resim, cerceveler, -1, (255,0,0), 3)

	return cerceveler