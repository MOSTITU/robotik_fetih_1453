# Kod estetiği TODO Sağ/Sol motor pinleri de fonksiyonlarda alınacak. Değişken silinecek.

import lib_dc_motor as dc
import lib_sabitler as sbt

def motorlari_ayarla():
    dc.pin_ayarla(sbt.SOL_DC_MOTOR_PIN)
    dc.pin_ayarla(sbt.SAG_DC_MOTOR_PIN)


def sola_don():
    dc.ileri(sbt.SAG_DC_MOTOR_PIN)
    dc.geri(sbt.SOL_DC_MOTOR_PIN)


def saga_don():
    dc.ileri(sbt.SOL_DC_MOTOR_PIN)
    dc.geri(sbt.SAG_DC_MOTOR_PIN)


def ileri():
    dc.ileri(sbt.SOL_DC_MOTOR_PIN)
    dc.ileri(sbt.SAG_DC_MOTOR_PIN)


def dur():
    dc.durdur(sbt.SOL_DC_MOTOR_PIN)
    dc.durdur(sbt.SAG_DC_MOTOR_PIN)


def geri():
    dc.geri(sbt.SOL_DC_MOTOR_PIN)
    dc.geri(sbt.SAG_DC_MOTOR_PIN)
