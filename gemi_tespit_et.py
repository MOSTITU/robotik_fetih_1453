import cv2
# import lib_gemi_hareket as gh
import lib_cv_yardimci as yar


def goruntuye_gore_hareket(img, merkez):
    genislik = img.shape[1]
    yukseklik = img.shape[0]
    if merkez[0] < genislik / 2:
        print("Sola dön")
        # gh.sola_don()
    else:
        print("Sağ dön")
        # gh.saga_don()


# kamera açılır, kamera açılamazsa video açılır
video = cv2.VideoCapture(0)
if not video.isOpened():
    video = cv2.VideoCapture(1)
if not video.isOpened():
    video = cv2.VideoCapture("./Medya/smile.mp4")

while True:
    _, resim = video.read()
    # Ayna etkisi
    resim = cv2.flip(resim, 1)
    resim = cv2.resize(resim, (340, 220))

    maskeSon = yar.maske_olustur(resim, yar.renk_siniri["mavi2"], yar.cekirdek)

    alanlar = yar.cerceve_ciz(resim, maskeSon)

    enBuyuk = {
        "alan": 0,
        "merkez": [0, 0],
        "sira": 0,
        "kose": [0, 0],
        "kenar": [0, 0]
    }

    for i, alan in enumerate(alanlar):
        print("Tespit edilen cisim sayisi:", len(alanlar))
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

        goruntuye_gore_hareket(resim, enBuyuk['merkez'])

    cv2.imshow("Video", resim)

    if cv2.waitKey(10) == 27:
        break
