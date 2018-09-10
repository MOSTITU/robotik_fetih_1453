import cv2
import numpy as np

yesil = [np.array([33,88,40]), np.array([102,255,255])]
mavi = [np.array([100, 60, 60]), np.array([140, 255, 255])]
beyaz = [np.array([0,0,140]), np.array([256,60,256])]
sari = [np.array([5, 100, 100]), np.array([40, 255, 256])]
kirmizi = [np.array([160,30,30]), np.array([190,255,255])]

altSinir, ustSinir = kirmizi

# 33. Ders - Erosion, Dilation, Opening, Closing
# Gürültüyü azaltma/arttırma
cekirdekAcik = np.ones((5, 5))
cekirdekKapali = np.ones((20, 20))

# kamera açılır, kamera açılamazsa video açılır
video = cv2.VideoCapture(0)
if not video.isOpened():
	video = cv2.VideoCapture("Medya/smile.mp4")


while True:
	_, resim = video.read()
	resim = cv2.resize(resim, (340, 220))

	# BGR -> HSV dönüşümü
	resimHSV = cv2.cvtColor(resim, cv2.COLOR_BGR2HSV)

	# maske oluşturma
	maske = cv2.inRange(resimHSV, altSinir, ustSinir)

	# morfoloji (morphology)
	maskeAcik = cv2.morphologyEx(maske, cv2.MORPH_OPEN, cekirdekAcik)
	maskeKapali = cv2.morphologyEx(maskeAcik, cv2.MORPH_CLOSE, cekirdekKapali)
	maskeSon = maskeKapali

	# Bulunan alanın çerçevesini alma
	_, cerceveler, h = cv2.findContours(maskeSon.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	#Resme çerçeve çizme
	cv2.drawContours(resim, cerceveler, -1, (255,0,0), 3)
	for i in range(len(cerceveler)):
		# cismi dikdörtgen halinde sol üst köşe ve kenar uzunluklarını alma
		x, y, w, h = cv2.boundingRect(cerceveler[i])
		# cismin etrafına dökdörtgen çizme
		cv2.rectangle(resim, (x,y), (x+w, y+h), (0,0,255), 2)
		# cismin sol altına görüntüdeki kaçıncı cisim olduğunu yazma
		cv2.putText(resim, str(i + 1), (x, y+h), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,255,255), 2)

	cv2.imshow("maskeKapali", maskeKapali)
	cv2.imshow("maskeAcik", maskeAcik)
	cv2.imshow("maske", maske)
	cv2.imshow("Video", resim)

	if cv2.waitKey(10) == 27:
		break