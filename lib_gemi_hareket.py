import dc_motor as dc

solMotorPins = [8,10,12]
sagMotorPins = [11,13,15]

def motorlari_ayarla():
	dc.pin_ayarla(solMotorPins)
	dc.pin_ayarla(sagMotorPins)

def sola_don():
	dc.ileri(sagMotorPins)
	dc.geri(solMotorPins)

def saga_don():
	dc.ileri(solMotorPins)
	dc.geri(sagMotorPins)

def ileri():
	dc.ileri(solMotorPins)
	dc.ileri(sagMotorPins)

def dur():
	dc.durdur(solMotorPins)
	dc.durdur(sagMotorPins)

def geri():
	dc.geri(solMotorPins)
	dc.geri(sagMotorPins)

def motor_pinleri_ayarla(solPins, sagPins):
	solMotorPins = solPins
	sagMotorPins = sagPins
	motorlari_ayarla()