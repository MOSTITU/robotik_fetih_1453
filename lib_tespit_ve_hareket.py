import cv2
import time
import lib_step_motor as sm
import lib_cv_yardimci as yar
import lib_gemi_hareket as gh
import lib_mesafe_sensoru as ms
enKucukGemiAlani = 250
SU_MESAFESI = 35


def cisim_bulunamazsa():
    # TODO cisim bulunamazsa ne yapılacak?
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
    if enBuyukGemi['alan'] > enKucukGemiAlani:
        goruntuye_gore_hareket(gemiResim, enBuyukGemi['merkez'])
    else:
        print("Gemi bulunamadı...")
        cisim_bulunamazsa()

    # TODO Geminin yakında olduğunu tespit etme
    # TODO Gemi alma eklenecek

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
    # TODO tirman'ın durumuna göre banda tırman

    return kapiResim


def duvar_bul_ve_carpma(resim):
    duvarResim = resim.copy()
    duvarMaske = yar.maske_olustur(duvarResim, yar.renk_siniri["duvar"], yar.cekirdek)
    duvarAlanlar = yar.cerceve_ciz(duvarResim, duvarMaske)

    # SU_MESAFESI'nden daha yakın olan yer duvar (sarı) mı?
    if ms.mesafe_olc(38, 40) < SU_MESAFESI and True:
        print("Duvar gördüm, kaçıyorum...")
        gh.geri()
        time.sleep(1)
        gh.sola_don()
        time.sleep(1)
    # TODO Sensör ve kamera yardımı ile duvara olan uzaklık tespit edilecek (Ekranın altında olması yakında olması anlamına geliyor olabiliri düşün)
    # TODO Duvar yakındaysa duvardan kaçınma fonksiyonunu çalıştır (Motor durdur, geri git, dön, kontrol et)

    return duvarResim
