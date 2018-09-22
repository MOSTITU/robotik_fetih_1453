import cv2
import time
import numpy as np
import lib_sabitler as sbt
import lib_step_motor as step
import lib_cv_yardimci as cvYar
import lib_dc_motor as dc
import lib_gemi_hareket as gemi
import lib_mesafe_sensoru as sensor


def butun_cihazlarin_pinlerini_ayarla():
    gemi.motorlari_ayarla()
    step.motor_pinlerini_ayarla(sbt.PIN_STEP_BOSALTMA_CUBUGU)
    step.motor_pinlerini_ayarla(sbt.PIN_STEP_DOLDURMA_CUBUGU)
    step.motor_pinlerini_ayarla(sbt.PIN_STEP_ROMORK)
    sensor.pin_ayarla(sbt.PIN_SENSOR_CAPRAZ)
    sensor.pin_ayarla(sbt.PIN_SENSOR_YATAY)


# TODO Başlangıç ayarlamaları yazılacak
def baslangic_ayarlamalari():
    step.tam_tur_don(-sbt.TUR_SAYISI_DOLDURMA_CUBUGU, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.PIN_STEP_DOLDURMA_CUBUGU)


def cisim_bulunamazsa():
    # Biraz daha düşün TODO cisim bulunamazsa ne yapılacak?
    gemi.sola_don()


def goruntuye_gore_hareket(img, merkez):
    genislik = img.shape[1]

    if merkez[0] < genislik / 2 - genislik / 16:
        print("Sola dön")
        gemi.sola_don()
    elif merkez[0] > genislik / 2 + genislik / 16:
        print("Sağ dön")
        gemi.saga_don()
    elif genislik / 2 + genislik / 16 >= merkez[0] >= genislik / 2 - genislik / 16:
        print("ileri git")
        gemi.ileri()
    return


def gemi_bul_ve_hareket_et(resim):
    gemiResim = resim.copy()
    gemiMaske = cvYar.maske_olustur(gemiResim, cvYar.renk_siniri["gemi"], cvYar.cekirdek)
    gemiAlanlar = cvYar.cerceve_ciz(gemiResim, gemiMaske)
    enBuyukGemi = cvYar.en_buyugu_bul(gemiAlanlar)
    # cismin etrafına dikdörtgen çizme
    cv2.rectangle(gemiResim, (enBuyukGemi['solUstKose'][0], enBuyukGemi['solUstKose'][1]),
                  (enBuyukGemi["sagAltKose"][0], enBuyukGemi["sagAltKose"][1]), (255, 0, 0), 3)
    if enBuyukGemi['alan'] > sbt.EN_KUCUK_GEMI_PIXEL_ALANI:
        goruntuye_gore_hareket(gemiResim, enBuyukGemi['merkez'])
    else:
        print("Gemi bulunamadı...")
        cisim_bulunamazsa()

    return gemiResim


def gemi_bulundu(resim):
    # mesafe = sensor_mesafe_bul(sbt.PIN_SENSOR_CAPRAZ, sbt.SENSOR_OLCUMU_KONTROL_SAYISI)
    # if mesafe < sbt.MESAFE_CAPRAZ_SU:
    #     return True
    gemiResim = resim.copy()
    gemiMaske = cvYar.maske_olustur(gemiResim, cvYar.renk_siniri["gemi"], cvYar.cekirdek)
    gemiAlanlar = cvYar.cerceve_ciz(gemiResim, gemiMaske)
    enBuyukGemi = cvYar.en_buyugu_bul(gemiAlanlar)
    # cismin etrafına dikdörtgen çizme
    cv2.rectangle(gemiResim, (enBuyukGemi['solUstKose'][0], enBuyukGemi['solUstKose'][1]),
                  (enBuyukGemi["sagAltKose"][0], enBuyukGemi["sagAltKose"][1]), (255, 0, 0), 3)
    if sbt.GEMI_ALMA_KONUM_PIXEL[0][0] < enBuyukGemi['merkez'][0] < sbt.GEMI_ALMA_KONUM_PIXEL[0][1] and sbt.GEMI_ALMA_KONUM_PIXEL[1][0] < enBuyukGemi['merkez'][1] < sbt.GEMI_ALMA_KONUM_PIXEL[1][1]:
        return True
    return False


def kapi_bul_ve_hareket_et(resim, tirman=False):
    kapiResim = resim.copy()
    kapiMaske = cvYar.maske_olustur(kapiResim, cvYar.renk_siniri["kapi"], cvYar.cekirdek)
    kapiAlanlar = cvYar.cerceve_ciz(kapiResim, kapiMaske)
    ret, kapiMerkez, kapiYon, s1, s2 = cvYar.kapiyi_tespit_et(kapiAlanlar)
    if not ret:
        cisim_bulunamazsa()
        return kapiResim
    # Sütunları dikdörtgen içine alma
    cv2.rectangle(kapiResim, (s1['solUstKose'][0], s1['solUstKose'][1]),
                  (s1["sagAltKose"][0], s1["sagAltKose"][1]), (255, 0, 0), 3)
    cv2.rectangle(kapiResim, (s2['solUstKose'][0], s2['solUstKose'][1]),
                  (s2["sagAltKose"][0], s2["sagAltKose"][1]), (255, 0, 0), 3)

    goruntuye_gore_hareket(kapiResim, kapiMerkez)

    return kapiResim


def duvardan_kac():
    gemi.geri()
    time.sleep(1)
    gemi.sola_don()
    time.sleep(1)


def duvar_bul_ve_carpma(resim):
    duvarResim = resim.copy()
    duvarMaske = cvYar.maske_olustur(duvarResim, cvYar.renk_siniri["duvar"], cvYar.cekirdek)
    duvarAlanlar = cvYar.cerceve_ciz(duvarResim, duvarMaske)

    # Eğer duvara fazla yakınsa duvardan kaç
    mesafe = sensor_mesafe_bul(sbt.PIN_SENSOR_YATAY, sbt.SENSOR_OLCUMU_KONTROL_SAYISI)
    if mesafe < sbt.MESAFE_YATAY_DUVAR:
        print("Duvar gördüm, kaçıyorum...")
        duvardan_kac()

    return duvarResim


def sensor_mesafe_bul(sensorPin, kontrolSayisi):
    ort = 0
    for i in range(kontrolSayisi):
        ort += sensor.mesafe_olc(sensorPin)
    ort /= kontrolSayisi
    return ort


def gemi_bosalt():
    # Öndeki çubuk yukarı kalkar
    step.tam_tur_don(-sbt.TUR_SAYISI_BOSALTMA_CUBUGU, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.PIN_STEP_BOSALTMA_CUBUGU)
    # Romork yukarı kalkar
    step.tam_tur_don(sbt.TUR_SAYISI_ROMORK, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.PIN_STEP_ROMORK)
    # Romork geri yerine iner
    step.tam_tur_don(-sbt.TUR_SAYISI_ROMORK, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.PIN_STEP_ROMORK)
    # Öndeki çubuk geri yerine iner
    step.tam_tur_don(sbt.TUR_SAYISI_BOSALTMA_CUBUGU, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.PIN_STEP_BOSALTMA_CUBUGU)


def gemi_topla():
    gemi.dur()
    time.sleep(0.1)
    step.tam_tur_don(sbt.TUR_SAYISI_DOLDURMA_CUBUGU + 1, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.PIN_STEP_DOLDURMA_CUBUGU)
    step.tam_tur_don(-sbt.TUR_SAYISI_DOLDURMA_CUBUGU, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.PIN_STEP_DOLDURMA_CUBUGU)


def banda_tirman(resim):
    return kapi_bul_ve_hareket_et(resim)


def bant_bulundu():
    mesafe = sensor_mesafe_bul(sbt.PIN_SENSOR_YATAY, sbt.SENSOR_OLCUMU_KONTROL_SAYISI)
    if mesafe < sbt.MESAFE_YATAY_DUVAR:
        return True
    return False


def sur_bul_ve_hareket_et(resim):
    surResim = resim.copy()
    img_hsv = cv2.cvtColor(surResim, cv2.COLOR_BGR2HSV)

    # alt maske (0-10)
    mask0 = cv2.inRange(img_hsv, cvYar.renk_siniri["sur_dusuk"][0], cvYar.renk_siniri["sur_dusuk"][1])
    # üst maske (170-180)
    mask1 = cv2.inRange(img_hsv, cvYar.renk_siniri["sur_yuksek"][0], cvYar.renk_siniri["sur_yuksek"][1])
    # maskeleri birleştir
    surMaske = mask0 + mask1
    # surMaske = cvYar.maske_olustur(surResim, cvYar.renk_siniri["sur"], cvYar.cekirdek)

    surAlanlar = cvYar.cerceve_ciz(surResim, surMaske)
    enBuyukSur = cvYar.en_buyugu_bul(surAlanlar)
    # cismin etrafına dikdörtgen çizme
    cv2.rectangle(surResim, (enBuyukSur['solUstKose'][0], enBuyukSur['solUstKose'][1]),
                  (enBuyukSur["sagAltKose"][0], enBuyukSur["sagAltKose"][1]), (255, 0, 0), 3)
    if enBuyukSur['alan'] > sbt.EN_KUCUK_SUR_PIXEL_ALANI:
        goruntuye_gore_hareket(surResim, enBuyukSur['merkez'])
    else:
        print("Sur bulunamadı...")
        cisim_bulunamazsa()

    return surResim


def sur_bulundu():
    mesafe = sensor_mesafe_bul(sbt.PIN_SENSOR_YATAY, sbt.SENSOR_OLCUMU_KONTROL_SAYISI)
    if mesafe < sbt.MESAFE_YATAY_DUVAR:
        return True
    return False


# TODO Top atma eklenecek
def top_at():
    dc.pin_ayarla(19, 21, 23)
    dc.ileri()
    time.sleep(10)
    dc.durdur()
    return
