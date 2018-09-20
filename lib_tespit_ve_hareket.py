import cv2
import time
import lib_sabitler as sbt
import lib_step_motor as sm
import lib_cv_yardimci as yar
import lib_gemi_hareket as gh
import lib_mesafe_sensoru as ms


def cisim_bulunamazsa():
    # Biraz daha düşün TODO cisim bulunamazsa ne yapılacak?
    gh.sola_don()


def goruntuye_gore_hareket(img, merkez):
    genislik = img.shape[1]

    if merkez[0] < genislik / 2 - genislik / 16:
        print("Sola dön")
        gh.sola_don()
    elif merkez[0] > genislik / 2 + genislik / 16:
        print("Sağ dön")
        gh.saga_don()
    elif genislik / 2 + genislik / 16 >= merkez[0] >= genislik / 2 - genislik / 16:
        print("ileri git")
        gh.ileri()
    return


def gemi_bul_ve_hareket_et(resim):
    gemiResim = resim.copy()
    gemiMaske = yar.maske_olustur(gemiResim, yar.renk_siniri["gemi"], yar.cekirdek)
    gemiAlanlar = yar.cerceve_ciz(gemiResim, gemiMaske)
    enBuyukGemi = yar.en_buyugu_bul(gemiAlanlar)
    # cismin etrafına dikdörtgen çizme
    cv2.rectangle(gemiResim, (enBuyukGemi['solUstKose'][0], enBuyukGemi['solUstKose'][1]),
                  (enBuyukGemi["sagAltKose"][0], enBuyukGemi["sagAltKose"][1]), (255, 0, 0), 3)
    if enBuyukGemi['alan'] > sbt.EN_KUCUK_GEMI_PIXEL_ALANI:
        goruntuye_gore_hareket(gemiResim, enBuyukGemi['merkez'])
    else:
        print("Gemi bulunamadı...")
        cisim_bulunamazsa()

    return gemiResim


def kapi_bul_ve_hareket_et(resim, tirman=False):
    kapiResim = resim.copy()
    kapiMaske = yar.maske_olustur(kapiResim, yar.renk_siniri["kapi"], yar.cekirdek)
    kapiAlanlar = yar.cerceve_ciz(kapiResim, kapiMaske)
    ret, kapiMerkez, kapiYon, s1, s2 = yar.kapiyi_tespit_et(kapiAlanlar)
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
    gh.geri()
    time.sleep(1)
    gh.sola_don()
    time.sleep(1)


def duvar_bul_ve_carpma(resim):
    duvarResim = resim.copy()
    duvarMaske = yar.maske_olustur(duvarResim, yar.renk_siniri["duvar"], yar.cekirdek)
    duvarAlanlar = yar.cerceve_ciz(duvarResim, duvarMaske)


    # TODO Acaba sensörden tespit edilen şey duvar mı?
    # Eğer duvara fazla yakınsa duvardan kaç
    if sensor_mesafe_bul(sbt.CAPRAZ_SENSOR_PIN, sbt.SENSOR_OLCUMU_KONTROL_SAYISI) < sbt.CACAPRAZ_SU_MESAFESI:
        print("Duvar gördüm, kaçıyorum...")
        duvardan_kac()

    return duvarResim


def sensor_mesafe_bul(sensorPin, kontrolSayisi):
    ort = 0
    for i in range(kontrolSayisi):
        ort += ms.mesafe_olc(sensorPin)
    ort /= kontrolSayisi
    return ort


def gemi_bulundu():
    ort = sensor_mesafe_bul(sbt.DIKEY_SENSOR_PIN, sbt.SENSOR_OLCUMU_KONTROL_SAYISI)
    if ort < sbt.DIK_SU_MESAFESI:
        return True
    return False


def gemi_bosalt():
    sm.tam_tur_don(-sbt.BANT_TAM_TUR_SAYISI, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.BANT_PIN)


def gemi_topla():
    gh.dur()
    time.sleep(0.1)
    sm.tam_tur_don(-sbt.ON_KOL_TUR_SAYISI, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.ON_KOL_PIN)
    sm.tam_tur_don(sbt.BANT_TAM_TUR_SAYISI / 2, sbt.STEP_MOTOR_BEKLEME_SURESI, sbt.BANT_PIN)


def banda_tirman(resim):
    return kapi_bul_ve_hareket_et(resim)


def bant_bulundu():
    ort = sensor_mesafe_bul(sbt.CAPRAZ_SENSOR_PIN, sbt.SENSOR_OLCUMU_KONTROL_SAYISI)
    if ort < sbt.DIK_SU_MESAFESI:
        return True
    return False
