import cv2
import lib_cv_yardimci as yar
import lib_tespit_sonrasi as ts
import lib_gemi_hareket as gh

enKucukGemiAlani = 250


def cisim_bulunamazsa():
    # TODO cisim bulunamazsa ne yapılacak?
    gh.dur()


def goruntuye_gore_hareket(img, cisim):
    genislik = img.shape[1]

    print("En büyük alan: ", cisim["alan"])

    if cisim["merkez"][0] < genislik / 2 - genislik / 16:
        print("Sola dön")
        gh.sola_don()
    elif cisim["merkez"][0] > genislik / 2 + genislik / 16:
        print("Sağ dön")
        gh.saga_don()
    elif genislik / 2 + genislik / 16 >= cisim["merkez"][0] >= genislik / 2 - genislik / 16:
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
        ts.goruntuye_gore_hareket(gemiResim, enBuyukGemi)
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
    _, kapiMerkez, kapiYon, s1, s2 = yar.kapiyi_tespit_et(kapiAlanlar)
    # Sütunları dikdörtgen içine alma
    cv2.rectangle(kapiResim, (s1['solUstKose'][0], s1['solUstKose'][1]),
                  (s1["sagAltKose"][0], s1["sagAltKose"][1]), (255, 0, 0), 3)
    cv2.rectangle(kapiResim, (s2['solUstKose'][0], s2['solUstKose'][1]),
                  (s2["sagAltKose"][0], s2["sagAltKose"][1]), (255, 0, 0), 3)

    # TODO Görüntüye (kapıya) doğru hareket et
    # TODO tirman'ın durumuna göre banda tırman

    return kapiResim


def duvar_bul_ve_carpma(resim):
    duvarResim = resim.copy()
    duvarMaske = yar.maske_olustur(duvarResim, yar.renk_siniri["duvar"], yar.cekirdek)
    duvarAlanlar = yar.cerceve_ciz(duvarResim, duvarMaske)

    # TODO Sensör ve kamera yardımı ile duvara olan uzaklık tespit edilecek (Ekranın altında olması yakında olması anlamına geliyor olabiliri düşün)
    # TODO Duvar yakındaysa duvardan kaçınma fonksiyonunu çalıştır (Motor durdur, geri git, dön, kontrol et)

    return duvarResim
