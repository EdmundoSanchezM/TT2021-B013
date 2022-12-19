from multiprocessing import Process
from MotoresDC import *
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def getGyroYaw():#Obtenemos el valor yaw del giroscopio con tipo string
	f = open(os.path.join(__location__, "GyroYawdata.txt"))
	lines = f.readlines()
	return lines[0].strip(),lines[1]

def detectaDesviacion():
	direc, yawValueFile = getGyroYaw()
	if(direc != 'Ok'):
		yawValue = float(yawValueFile)
		print(direc)
		print(yawValue)
		if(direc == "N"):
			if(yawValue > 0):
				moverMotorDer(False,(yawValue*0.3)/2.8459 )
			else:
				yawValue = yawValue * -1
				moverMotorIzq(False,(yawValue*0.3)/ 1.6578 )
		elif(direc == "W"):
			if(yawValue > 0):
				moverMotorDer(False,(yawValue*0.3)/ 4.4 )
			else:
				yawValue = yawValue * -1
				moverMotorIzq(False,(yawValue*0.3)/ 1.6578 )
		if(direc == "E"):
			if(yawValue > 0):
				moverMotorDer(False,(yawValue*0.3)/2.86 )
			else:
				yawValue = yawValue * -1
				moverMotorIzq(False,(yawValue*0.3)/ 1.6578 )
		if(direc == "SP"):
			if(yawValue < 0):
				yawValue = yawValue * -1
				moverMotorIzq(False,(yawValue*0.3)/ 1.8 )
			else:
				moverMotorIzq(False,(yawValue*0.3)/ 1.8 )
		if(direc == "SN"):
			if(yawValue < 0):
				yawValue = yawValue * -1
				moverMotorDer(False,(yawValue*0.3)/ 1.95 )
			else:
				moverMotorDer(False,(yawValue*0.3)/ 1.95 )				
def moverMotorAdelante(tmp=4,ext=False):
	print("Moviendo hacia delante")
	p1 = Process(target=motorIzq, args=(True,tmp,))
	p2 = Process(target=motorDer, args=(True,tmp,))
	p1.start()
	p2.start()
	p1.join()
	p2.join()
	if(not ext):
		detectaDesviacion()

def moverMotorAtras(tmp=4,ext=False):
	print("Moviendo hacia atras")
	p1 = Process(target=motorIzq, args=(False,tmp,))
	p2 = Process(target=motorDer, args=(False,tmp,))
	p1.start()
	p2.start()
	p1.join()
	p2.join()
	if(not ext):
		detectaDesviacion()

def moverMotorIzq(sentido, tmp=4):
	print("Moviendo motor izq", sentido)
	motorIzq(sentido, tmp)

def moverMotorDer(sentido, tmp=4):
	print("Movimiento motor der", sentido)
	motorDer(sentido, tmp)

def horientarIzquierda():
	moverMotorIzq(True,4)
	moverMotorDer(False,3.55)
	moverMotorAtras(1.4,True) 
	print("Horientando hacia la izquierda")
	detectaDesviacion()

def horientarDerecha():
	moverMotorDer(True,4)
	moverMotorIzq(False,3.3)
	moverMotorAtras(1.35,True)
	print("Horientando hacia la derecha")
	detectaDesviacion()
	
if __name__ == '__main__':
	#moverMotorAdelante()
	#moverMotorAtras()
	#horientarIzquierda()
	#horientarDerecha()
	#horientarDerecha()
	detectaDesviacion()
