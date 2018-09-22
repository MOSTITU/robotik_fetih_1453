import cv2
import numpy as np

# Renklerin alt ve üst sınırlarını tutan sözlük (dictionary) yapısı
renk_siniri = {
    "yesil": [np.array([33, 88, 40]), np.array([102, 255, 255])],
    "mavi": [np.array([100, 60, 60]), np.array([140, 255, 255])],
    "beyaz": [np.array([0, 0, 140]), np.array([256, 60, 256])],
    "sari": [np.array([5, 100, 100]), np.array([40, 255, 256])],
    "kirmizi": [np.array([160, 30, 30]), np.array([180, 255, 255])],
    "mavi2": [np.array((80, 100, 70)), np.array((120, 180, 255))],
    "gemi": [np.array([33, 88, 40]), np.array([102, 255, 255])],
    "duvar": [np.array([5, 100, 100]), np.array([40, 255, 256])],
    "kapi": [np.array([100, 60, 60]), np.array([140, 255, 255])],
    "sur": [np.array([160, 30, 30]), np.array([180, 255, 255])],
    "dusuk_kirmizi": [np.array([0, 50, 50]), np.array([10, 255, 255])],
    "yuksek_kirmizi": [np.array([170, 50, 50]), np.array([180, 255, 255])],
    "sur_dusuk": [np.array([0, 50, 50]), np.array([10, 255, 255])],
    "sur_yuksek": [np.array([170, 50, 50]), np.array([180, 255, 255])]
}

# 33. Ders - Erosion, Dilation, Opening, Closing
# Gürültüyü azaltma/arttırma
cekirdek = {
    "acik": np.ones((5, 5)),
    "kapali": np.ones((20, 20))
}


# Maske olusturur, son maske değerini döndürür
def maske_olustur(resim, sinirlar, incekirdek):
    altSinir, ustSinir = sinirlar

    # BGR -> HSV dönüşümü
    resimHSV = cv2.cvtColor(resim, cv2.COLOR_BGR2HSV)

    # maske oluşturma
    maske = cv2.inRange(resimHSV, altSinir, ustSinir)

    # morfoloji (morphology)
    maskeAcik = cv2.morphologyEx(maske, cv2.MORPH_OPEN, incekirdek["acik"])
    maskeKapali = cv2.morphologyEx(maskeAcik, cv2.MORPH_CLOSE, incekirdek["kapali"])

    # cv2.imshow("maskeKapali", maskeKapali)
    # cv2.imshow("maskeAcik", maskeAcik)
    # cv2.imshow("maske", maske)

    return maskeKapali


def cerceve_ciz(resim, maske):
    # Bulunan alanın çerçevesini alma
    _, cerceveler, h = cv2.findContours(maske.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Resme çerçeve çizme
    cv2.drawContours(resim, cerceveler, -1, (0, 0, 255), 2)

    return cerceveler


def en_buyugu_bul(alanlar):
    enBuyuk = {
        "alan": 0,
        "merkez": (0, 0),
        "sira": 0,
        "solUstKose": (0, 0),
        "sagAltKose": (0, 0),
        "kenar": (0, 0)
    }

    for i, alan in enumerate(alanlar):
        if cv2.contourArea(alan) > enBuyuk["alan"]:
            # cismi dikdörtgen halinde sol üst köşe ve kenar uzunluklarını alma
            x, y, w, h = cv2.boundingRect(alan)
            enBuyuk["alan"] = cv2.contourArea(alan)
            enBuyuk["merkez"] = [x + w / 2, y + h / 2]
            enBuyuk["sira"] = i
            enBuyuk["solUstKose"] = [x, y]
            enBuyuk["sagAltKose"] = [x + w, y + h]
            enBuyuk["kenar"] = [w, h]

    return enBuyuk


# ret değeri, merkez nokayı, geminin kapıya göre olan yönünü ve sütunları döner
# ret = False -> Kapı bulunamadı, ret = True -> Kapı bulundu
# yon = 0 -> kapının karşışında, yon = -1 -> kapının solunda, yon = 1 -> kapının sağında
def kapiyi_tespit_et(alanlar):
    ret = False
    merkez = (0, 0)
    yon = 0

    sutun1 = {
        "alan": 0,
        "merkez": (0, 0),
        "sira": 0,
        "solUstKose": (0, 0),
        "sagAltKose": (0, 0),
        "kenar": (0, 0)
    }

    sutun2 = sutun1.copy()

    for i, alan in enumerate(alanlar):
        # Cismin alanı 150'den küçükse onu kabul etme
        if cv2.contourArea(alan) < 150:
            continue

        if cv2.contourArea(alan) > sutun1["alan"]:
            # cismi dikdörtgen halinde sol üst köşe ve kenar uzunluklarını alma
            x, y, w, h = cv2.boundingRect(alan)
            sutun2 = sutun1.copy()
            sutun1['alan'] = cv2.contourArea(alan)
            sutun1['merkez'] = [x + w / 2, y + h / 2]
            sutun1['sira'] = i
            sutun1['solUstKose'] = [x, y]
            sutun1['sagAltKose'] = [x + w, y + h]
            sutun1['kenar'] = [w, h]
        elif cv2.contourArea(alan) > sutun2["alan"]:
            x, y, w, h = cv2.boundingRect(alan)
            sutun2['alan'] = cv2.contourArea(alan)
            sutun2['merkez'] = [x + w / 2, y + h / 2]
            sutun2['sira'] = i
            sutun2['solUstKose'] = [x, y]
            sutun2['sagAltKose'] = [x + w, y + h]
            sutun2['kenar'] = [w, h]

    # Eğer sutun2'nin alanı 0 ise kapı yok demektir. Kapıda 2 sütun olması gerekiyor
    if sutun2['alan'] == 0:
        return ret, merkez, yon, sutun1, sutun2

    if sutun2['alan'] != 0:
        ret = True

        if (sutun1['alan'] - sutun2['alan'] / sutun1['alan']) * 100 < 30:
            yon = 0
        # Fark çok büyükse o zaman yön belirle: -1 -> gemi kapının solunda, +1 -> gemi kapını sağında
        elif sutun1['merkez'][0] < sutun2['merkez'][0]:
            yon = -1
        elif sutun1['merkez'][0] > sutun2['merkez'][0]:
            yon = 1
        else:
            pass

    merkez = ((sutun1['merkez'][0] + sutun2['merkez'][0]) / 2, (sutun1['merkez'][1] + sutun2['merkez'][1]) / 2)
    return ret, merkez, yon, sutun1, sutun2
