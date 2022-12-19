from Movimientos import *
import time
import copy
import os,signal
import Archivo
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def KillProcessCaminante(pid):#Funcionando
	try:
		os.kill(pid, signal.SIGKILL) 
		Archivo.deletePIDFile()
		print("Process Successfully terminated")
	except:
		print("Error Encountered while running script")

def moore(data,pos_y, pos_x): #data[y][x]
	nw = data[pos_y-1][pos_x-1]
	n = data[pos_y-1][pos_x]
	ne = data[pos_y-1][pos_x+1]
	w = data[pos_y][pos_x-1]
	e = data[pos_y][pos_x+1]
	sw = data[pos_y+1][pos_x-1]
	s = data[pos_y+1][pos_x]
	se = data[pos_y+1][pos_x+1]
	print(nw,n,ne)
	print(w,data[pos_y][pos_x],e)
	print(sw,s,se)
	return [[nw,n,ne],[w,data[pos_y][pos_x],e],[sw,s,se]]

def testQuitarNull():
	objCaminantePass = Archivo.getFilePosCaminantePass()
	return objCaminantePass.orientacion
	
def test(objT,fin):
	valX = objT.pos_x
	valY = objT.pos_y 
	if(fin == "W"):
		boolCoorPassNU = Archivo.compareCoorPasCoor(valY-1,valX-1)
		boolCoorPassD = Archivo.compareCoorPasCoor(valY,valX-1)
		boolCoorPassND = Archivo.compareCoorPasCoor(valY+1,valX-1)
		if(boolCoorPassNU or boolCoorPassD or boolCoorPassND):
			return True#Ya pasamos por ahi
		return False#No pasamos por ahi	
	elif(fin == "E"):
		boolCoorPassNU = Archivo.compareCoorPasCoor(valY-1,valX+1)
		boolCoorPassD = Archivo.compareCoorPasCoor(valY,valX+1)
		boolCoorPassND = Archivo.compareCoorPasCoor(valY+1,valX+1)
		if(boolCoorPassNU or boolCoorPassD or boolCoorPassND):
			return True#Ya pasamos por ahi
		return False#No pasamos por ahi
	elif(fin == "N"):
		boolCoorPassNW = Archivo.compareCoorPasCoor(valY-1,valX-1)
		boolCoorPassD = Archivo.compareCoorPasCoor(valY-1,valX)
		boolCoorPassNE = Archivo.compareCoorPasCoor(valY-1,valX+1)
		if(boolCoorPassNW or boolCoorPassD or boolCoorPassNE):
			return True#Ya pasamos por ahi
		return False#No pasamos por ahi
	else:
		boolCoorPassNW = Archivo.compareCoorPasCoor(valY+1,valX-1)
		boolCoorPassD = Archivo.compareCoorPasCoor(valY+1,valX)
		boolCoorPassNE = Archivo.compareCoorPasCoor(valY+1,valX+1)
		if(boolCoorPassNW or boolCoorPassD or boolCoorPassNE):
			return True#Ya pasamos por ahi
		return False#No pasamos por ahi

def orientarRobot(obj, fin):
	if(fin == "W"):
		if(obj.orientacion == "N"):
			horientarIzquierda()
		elif(obj.orientacion == "S"):
			horientarDerecha()
		elif(obj.orientacion == "E"):
			horientarIzquierda()
			horientarIzquierda()
	elif(fin == "E"):
		if(obj.orientacion == "N"):
			horientarDerecha()
		elif(obj.orientacion == "S"):
			horientarIzquierda()
		elif(obj.orientacion == "W"):
			horientarIzquierda()
			horientarIzquierda()
	elif(fin == "N"):
		if(obj.orientacion == "E"):
			horientarIzquierda()
		elif(obj.orientacion == "W"):
			horientarDerecha()
		elif(obj.orientacion == "S"):
			horientarIzquierda()
			horientarIzquierda()
	else:
		if(obj.orientacion == "E"):
			horientarDerecha()
		elif(obj.orientacion == "W"):
			horientarIzquierda()
		elif(obj.orientacion == "N"):
			horientarIzquierda()
			horientarIzquierda()
	obj.orientacion = fin

def orientarRobotLogico(obj,vecindad):
	newObj = copy.copy(obj)
	print("Logico")
	if(obj.orientacion == "N"):
		if( obj.fin_x <= obj.pos_x ): #Fin a la izq
			newObj.orientacion = "W"
			straight = goStraight(vecindad, newObj)
			diagonal = goDiagonal(vecindad, newObj)
			if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
				return "W"
		if(obj.fin_x > obj.pos_x):#Fin a la der
			newObj.orientacion = "E"
			straight = goStraight(vecindad, newObj)
			diagonal = goDiagonal(vecindad, newObj)
			if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
				return "E"
		newObj.orientacion = "E"
		straight = goStraight(vecindad, newObj)
		diagonal = goDiagonal(vecindad, newObj)
		if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
			return "E"
		newObj.orientacion = "W"
		straight = goStraight(vecindad, newObj)
		diagonal = goDiagonal(vecindad, newObj)
		if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
			return "W"
		return "S"
	elif(obj.orientacion == "S"):
		if( obj.fin_x <= obj.pos_x ): #Fin a la izq
			newObj.orientacion = "W"
			straight = goStraight(vecindad, newObj)
			diagonal = goDiagonal(vecindad, newObj)
			if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
				return "W"
		if(obj.fin_x > obj.pos_x):#Fin a la der
			newObj.orientacion = "E"
			straight = goStraight(vecindad, newObj)
			diagonal = goDiagonal(vecindad, newObj)
			if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
				return "E"
		newObj.orientacion = "E"
		straight = goStraight(vecindad, newObj)
		diagonal = goDiagonal(vecindad, newObj)
		if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
			return "E"
		newObj.orientacion = "W"
		straight = goStraight(vecindad, newObj)
		diagonal = goDiagonal(vecindad, newObj)
		if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
			return "W"
		return "N"
	elif(obj.orientacion == "E"):
		if( obj.fin_y <= obj.pos_y ): #Fin a la izq
			newObj.orientacion = "N"
			straight = goStraight(vecindad, newObj)
			diagonal = goDiagonal(vecindad, newObj)
			if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
				return "N"
		if( obj.fin_y > obj.pos_y ):#Fin a la der
			newObj.orientacion = "S"
			straight = goStraight(vecindad, newObj)
			diagonal = goDiagonal(vecindad, newObj)
			if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
				return "S"
		newObj.orientacion = "N"
		straight = goStraight(vecindad, newObj)
		diagonal = goDiagonal(vecindad, newObj)
		if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
			return "N"
		newObj.orientacion = "S"
		straight = goStraight(vecindad, newObj)
		diagonal = goDiagonal(vecindad, newObj)
		if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
			return "S"
		return "W"
	elif(obj.orientacion == "W"):
		if( obj.fin_y <= obj.pos_y ): #Fin a la izq
			newObj.orientacion = "N"
			straight = goStraight(vecindad, newObj)
			diagonal = goDiagonal(vecindad, newObj)
			if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
				return "N"
		if( obj.fin_y > obj.pos_y ):#Fin a la der
			newObj.orientacion = "S"
			straight = goStraight(vecindad, newObj)
			diagonal = goDiagonal(vecindad, newObj)
			if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
				return "S"
		newObj.orientacion = "N"
		straight = goStraight(vecindad, newObj)
		diagonal = goDiagonal(vecindad, newObj)
		if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
			return "N"
		newObj.orientacion = "S"
		straight = goStraight(vecindad, newObj)
		diagonal = goDiagonal(vecindad, newObj)
		if((straight or diagonal) and (not test(newObj,newObj.orientacion))):
			return "S"
		return "E"
	
			
def goStraight(vecindad, obj):
	if(obj.orientacion == "N"):
		if(vecindad[0][1] == 5 or vecindad[0][1] == 8):
			return True
		else:
			return False
	elif(obj.orientacion == "S"):
		if(vecindad[2][1] == 5 or vecindad[2][1] == 8):
			return True
		else:
			return False
	elif(obj.orientacion == "W"):
		if(vecindad[1][0] == 5 or vecindad[1][0] == 8):
			return True
		else:
			return False
	elif(obj.orientacion == "E"):
		if(vecindad[1][2] == 5 or vecindad[1][2] == 8):
			return True
		else:
			return False

def cambiarXYCaminante(obj,direc):
	if(obj.orientacion == "N"):
		obj.pos_y = obj.pos_y - 1
		if(direc == "Izq"):
			obj.pos_x = obj.pos_x - 1
			orientarRobot(obj,"W")
			moverMotorAdelante()
			orientarRobot(obj,"N")
			moverMotorAdelante()
		elif(direc == "Der"):
			obj.pos_x = obj.pos_x + 1
			orientarRobot(obj,"E")
			moverMotorAdelante()
			orientarRobot(obj,"N")
			moverMotorAdelante()
	elif(obj.orientacion == "S"):
		obj.pos_y = obj.pos_y + 1
		if(direc == "Izq"):
			obj.pos_x = obj.pos_x + 1
			orientarRobot(obj,"E")
			moverMotorAdelante()
			orientarRobot(obj,"S")
			moverMotorAdelante()
		elif(direc == "Der"):
			obj.pos_x = obj.pos_x - 1
			orientarRobot(obj,"W")
			moverMotorAdelante()
			orientarRobot(obj,"S")
			moverMotorAdelante()
	elif(obj.orientacion == "W"):
		obj.pos_x = obj.pos_x - 1
		if(direc == "Izq"):
			obj.pos_y = obj.pos_y + 1
			orientarRobot(obj,"S")
			moverMotorAdelante()
			orientarRobot(obj,"W")
			moverMotorAdelante()
		elif(direc == "Der"):
			obj.pos_y = obj.pos_y - 1
			orientarRobot(obj,"N")
			moverMotorAdelante()
			orientarRobot(obj,"W")
			moverMotorAdelante()
	elif(obj.orientacion == "E"):
		obj.pos_x = obj.pos_x + 1
		if(direc == "Izq"):
			obj.pos_y = obj.pos_y - 1
			orientarRobot(obj,"N")
			moverMotorAdelante()
			orientarRobot(obj,"E")
			moverMotorAdelante()
		elif(direc == "Der"):
			obj.pos_y = obj.pos_y + 1
			orientarRobot(obj,"S")
			moverMotorAdelante()
			orientarRobot(obj,"E")
			moverMotorAdelante()
	Archivo.setCoorPas(obj.pos_x,obj.pos_y)

def goDiagonal(vecindad, obj):#Daremos prioridad a la esquina mas cerca del punto final o con mas dependecias
	existe = False
	if(obj.orientacion == "N"):	
		if((vecindad[0][0] == 5 or vecindad[0][0] == 8)):
			if(obj.fin_x <= obj.pos_x):
				return "Izq"
			else:
				existe = "Izq"
		if((vecindad[0][2] == 5 or vecindad[0][2] == 8)):
			if(obj.fin_x >= obj.pos_x):
				return "Der"
			else:
				existe = "Der"
		return existe
	elif(obj.orientacion == "S"):
		if((vecindad[2][0] == 5 or vecindad[2][0] == 8)):
			if(obj.fin_x <= obj.pos_x):
				return "Der"
			else:
				existe = "Der"
		if((vecindad[2][2] == 5 or vecindad[2][2] == 8)):
			if(obj.fin_x >= obj.pos_x):
				return "Izq"
			else:
				existe = "Izq"
		return existe
	elif(obj.orientacion == "W"):
		if((vecindad[0][0] == 5 or vecindad[0][0] == 8)):
			if(obj.fin_y <= obj.pos_y):
				return "Der"
			else:
				existe = "Der"
		if((vecindad[2][0] == 5 or vecindad[2][0] == 8)):
			if(obj.fin_y >= obj.pos_y):
				return "Izq"
			else:
				existe = "Izq"
		return existe
	elif(obj.orientacion == "E"):
		if((vecindad[0][2] == 5 or vecindad[0][2] == 8)):
			if(obj.fin_y <= obj.pos_y):
				return "Izq"
			else:
				existe = "Izq"
		if((vecindad[2][2] == 5 or vecindad[2][2] == 8)):
			if(obj.fin_y >= obj.pos_y):
				return "Der"
			else:
				existe = "Der"
		return existe

def finalizarCaminante(vecindad, obj,orientacionSalFinal):#Optimizable
	if(obj.orientacion == "N"):
		if(vecindad[0][0] == 6):
			cambiarXYCaminante(obj, "Izq")
		elif(vecindad[0][1] == 6):
			moverMotorAdelante()
			cambiarXYCaminante(obj, "straight")
		elif(vecindad[0][2] == 6):
			cambiarXYCaminante(obj, "Der")
		else:
			orientarRobot(obj,"S")
			finalizarCaminante(vecindad, obj,orientacionSalFinal)
	elif(obj.orientacion == "S"):
		if(vecindad[2][0] == 6):
			cambiarXYCaminante(obj, "Der")
		elif(vecindad[2][1] == 6):
			moverMotorAdelante()
			cambiarXYCaminante(obj, "straight")
		elif(vecindad[2][2] == 6):
			cambiarXYCaminante(obj, "Izq")
		else:
			orientarRobot(obj,"W")
			finalizarCaminante(vecindad, obj,orientacionSalFinal)
	elif(obj.orientacion == "W"):
		if(vecindad[0][0] == 6):
			cambiarXYCaminante(obj, "Der")
		elif(vecindad[1][0] == 6):
			moverMotorAdelante()
			cambiarXYCaminante(obj, "straight")
		elif(vecindad[2][0] == 6):
			cambiarXYCaminante(obj, "Izq")
		else:
			orientarRobot(obj,"E")
			finalizarCaminante(vecindad, obj,orientacionSalFinal)
	elif(obj.orientacion == "E"):
		if(vecindad[0][2] == 6):
			cambiarXYCaminante(obj, "Izq")
		elif(vecindad[1][2] == 6):
			moverMotorAdelante()
			cambiarXYCaminante(obj, "straight")
		elif(vecindad[2][2] == 6):
			cambiarXYCaminante(obj, "Der")
		else:
			orientarRobot(obj,"W")
			finalizarCaminante(vecindad, obj,orientacionSalFinal)
	orientarRobot(obj,orientacionSalFinal)

def iniciarCaminata(obj, mapa, orientacionSalFinal):
	print(orientacionSalFinal)
	while True:
		vecindad = moore(mapa,obj.pos_y,obj.pos_x)
		if(obj.orientacion == None):
			obj.orientacion = testQuitarNull()
		print(obj.orientacion)
		if(6 in vecindad[0] or 6 in vecindad[1] or 6 in vecindad[2]):
			print(orientacionSalFinal)
			finalizarCaminante(vecindad, obj, orientacionSalFinal)
			print(obj.toJSON())
			moore(mapa,obj.pos_y,obj.pos_x)
			break
		straight = goStraight(vecindad, obj)
		diagonal = goDiagonal(vecindad, obj)
		if(straight):
			moverMotorAdelante()
			cambiarXYCaminante(obj,"straight")
		else:
			if(diagonal):
				cambiarXYCaminante(obj,diagonal)
				print("diagonal directa")
			else:
				orientacion = orientarRobotLogico(obj,vecindad)
				print(orientacion)
				orientarRobot(obj,orientacion)
		print(obj.toJSON())
		time.sleep(0.5)#dar tiempo a sensores. Modificar por mas tiempo si es necesario 5s
		print("#####################################")
	return True
 
