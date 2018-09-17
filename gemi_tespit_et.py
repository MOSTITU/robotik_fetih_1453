import cv2
import lib_gemi_hareket as gh
import lib_cv_yardimci as yar
import os
import RPi.GPIO as GPIO

def goruntuye_gore_hareket(img, cisim):
    genislik = img.shape[1]
    yukseklik = img.shape[0]
    if cisim["alan"] < 250:
        print("Dur")
        gh.dur()
        return False

    print("En büyük alan: ", cisim["alan"])

    if cisim["merkez"][0] < genislik / 2 - 20:
        print("Sola dön")
        gh.sola_don()
    elif cisim["merkez"][0] > genislik / 2 + 20:
        print("Sağ dön")
        gh.saga_don()
    elif cisim["merkez"][0] <= genislik / 2 + 20 and cisim["merkez"][0] >= genislik / 2 - 20:
        print("ileri git")
        gh.ileri()
    else:
        print("Dur")
        gh.dur()
    return True


GPIO.setmode(GPIO.BOARD)
gh.motorlari_ayarla()
# kamera açılır, kamera açılamazsa video açılır
kamera = cv2.VideoCapture(1)
if not kamera.isOpened():
    kamera = cv2.VideoCapture(0)
if not kamera.isOpened():
    kamera = cv2.VideoCapture("./Medya/smile.mp4")

kayitSayisi = int(len(os.listdir('./Medya/Kayitlar')) / 2)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
temizKayit = cv2.VideoWriter('./Medya/Kayitlar/temizKayit'+str(kayitSayisi)+'.avi', fourcc, 10.0, (640, 480))
islenmisKayit = cv2.VideoWriter('./Medya/Kayitlar/islenmisKayit'+str(kayitSayisi)+'.avi', fourcc, 10.0, (340, 220))

while True:
    _, resim = kamera.read()
    temizKayit.write(resim)
    # Ayna etkisi
    #resim = cv2.flip(resim, 1)
    resim = cv2.resize(resim, (340, 220))

    maskeSon = yar.maske_olustur(resim, yar.renk_siniri["yesil"], yar.cekirdek)

    alanlar = yar.cerceve_ciz(resim, maskeSon)

    enBuyuk = {
        "alan": 0,
        "merkez": [0, 0],
        "sira": 0,
        "kose": [0, 0],
        "kenar": [0, 0]
    }

    for i, alan in enumerate(alanlar):
        # print("Tespit edilen cisim sayisi:", len(alanlar))
        # cismi dikdörtgen halinde sol üst köşe ve kenar uzunluklarını alma
        x, y, w, h = cv2.boundingRect(alan)

        # cismin etrafına dikdörtgen çizme
        cv2.rectangle(resim, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # # cismin sol altına görüntüdeki kaçıncı cisim olduğunu yazma
        # cv2.putText(resim, str(i + 1), (x, y + h), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1)

        if cv2.contourArea(alan) > enBuyuk["alan"]:
            enBuyuk["alan"] = cv2.contourArea(alan)
            enBuyuk["merkez"] = [x + w / 2, y + h / 2]
            enBuyuk["sira"] = i
            enBuyuk["kose"] = [x, y]
            enBuyuk["kenar"] = [w, h]

        goruntuye_gore_hareket(resim, enBuyuk)

    islenmisKayit.write(resim)
    cv2.imshow("Video", resim)
    if cv2.waitKey(20) == 27:
        break

kamera.release()
temizKayit.release()
islenmisKayit.release()
cv2.destroyAllWindows()
