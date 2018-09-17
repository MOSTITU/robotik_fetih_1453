# import lib_gemi_hareket as gh


def cisim_bulamazsa():
    print("Cisim bulunamadı...")
    # gh.dur()


def buyuk_cisim_bulamazsa():
    cisim_bulamazsa()


def goruntuye_gore_hareket(img, cisim):
    genislik = img.shape[1]
    if cisim["alan"] < 250:
        buyuk_cisim_bulamazsa()
        return False

    print("En büyük alan: ", cisim["alan"])

    if cisim["merkez"][0] < genislik / 2 - genislik / 16:
        print("Sola dön")
        # gh.sola_don()
    elif cisim["merkez"][0] > genislik / 2 + genislik / 16:
        print("Sağ dön")
        # gh.saga_don()
    elif genislik / 2 + genislik / 16 >= cisim["merkez"][0] >= genislik / 2 - genislik / 16:
        print("ileri git")
        # gh.ileri()
    return True

