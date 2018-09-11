import dc_motor as dc

solMotorPins = [0,0,0]
sagMotorPins = [0,0,0]


def sola_don():
	dc.ileri(sagMotorPins,0)
	print("Sola dön")

def saga_don():
	dc.ileri(solMotorPins,0)
	print("Sağa dön")

def ileri_git():
	dc.ileri(solMotorPins,0)
	dc.ileri(sagMotorPins,0)
	print("İleri git")

def dur():
	dc.durdur(solMotorPins[2])
	dc.durdur(sagMotorPins[2])
	print("Dur")