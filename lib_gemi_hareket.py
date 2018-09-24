# Geminin iki motorunu birlikte kontrol ederek geminin hareketini sağlayan modul
import lib_dc_motor as dc
import lib_sabitler as sbt


# Motor pinlerini ayarla
def motorlari_ayarla():
    dc.pin_ayarla(sbt.SOL_DC_MOTOR_PIN)
    dc.pin_ayarla(sbt.SAG_DC_MOTOR_PIN)


# Gemiyi sola döndür
def sola_don():
    dc.ileri(sbt.SAG_DC_MOTOR_PIN)
    dc.geri(sbt.SOL_DC_MOTOR_PIN)


# Gemiyi sağa döndür
def saga_don():
    dc.ileri(sbt.SOL_DC_MOTOR_PIN)
    dc.geri(sbt.SAG_DC_MOTOR_PIN)


# Gemiyi ileri yönde hareket ettir
def ileri():
    dc.ileri(sbt.SOL_DC_MOTOR_PIN)
    dc.ileri(sbt.SAG_DC_MOTOR_PIN)


# Motorları durdur
def dur():
    dc.durdur(sbt.SOL_DC_MOTOR_PIN)
    dc.durdur(sbt.SAG_DC_MOTOR_PIN)


# Gemiri geri yönde hareket ettir
def geri():
    dc.geri(sbt.SOL_DC_MOTOR_PIN)
    dc.geri(sbt.SAG_DC_MOTOR_PIN)
