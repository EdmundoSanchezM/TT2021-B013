import numpy as np
import os
import json
import pandas as pd
from matplotlib import pyplot as plt
import signal
from matplotlib.colors import ListedColormap
from Caminante import Caminante
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


		
def getGyroYaw():#Obtenemos el valor yaw del giroscopio con tipo string
	f = open(os.path.join(__location__, "GyroYawdata.txt"))
	lines = f.readlines()
	return lines[0].strip(),lines[1]

def getPIDFile():#Obtenemos el pid del proceso principal
	with open(os.path.join(__location__, "pidMain.txt")) as f:
		pid = f.read()
		return pid
		
def deletePIDFile():
	os.remove(os.path.join(__location__, 'pidMain.txt'))
	
def setPIDFile(pidN):#Obtenemos es pid del proceso principal
	f = open(os.path.join(__location__, 'pidMain.txt'), "w")
	f.write(str(pidN))
	f.close()

def getPIDFileGyro():#Obtenemos el pid del proceso gyro
	with open(os.path.join(__location__, "pidGyro.txt")) as f:
		pid = f.read()
		return pid
		
def deletePIDFileGyro():
	os.remove(os.path.join(__location__, 'pidGyro.txt'))
	
def setPIDFileGyro(pidN):#Obtenemos es pid del proceso gyro
	f = open(os.path.join(__location__, 'pidGyro.txt'), "w")
	f.write(str(pidN))
	f.close()	

def setCoorPas(x,y):
	arrA = ["coorPas1.txt","coorPas2.txt","coorPas3.txt","coorPas4.txt"]
	xpasA = ""
	ypasA = ""
	for i,nombre in enumerate(arrA):
		with open(os.path.join(__location__, nombre), 'r') as f:
			l = f.readlines()
			xs = l[0].replace('x=', '')
			xactA = int(xs.replace('\n', ''))
			yactA = int(l[1].replace('y=', ''))
		if(i==0):
			f = open(os.path.join(__location__, nombre), "w")
			f.write("x="+str(x)+"\n"+"y="+str(y))
			f.close()
			xpasA = xactA
			ypasA = yactA
		else:
			f = open(os.path.join(__location__, nombre), "w")
			f.write("x="+str(xpasA)+"\n"+"y="+str(ypasA))
			f.close()	
			xpasA = xactA
			ypasA = yactA
			
def compareCoorPasCoor(y,x):
	arrA = ["coorPas1.txt","coorPas2.txt","coorPas3.txt","coorPas4.txt"]
	xpasC = ""
	ypasC = ""
	for nombre in arrA:
		with open(os.path.join(__location__, nombre), 'r') as f:
			l = f.readlines()
			xs = l[0].replace('x=', '')
			xpasC = int(xs.replace('\n', ''))
			ypasC = int(l[1].replace('y=', ''))
		if( x == xpasC and y == ypasC ):
			return True
	return False
	
def getPosFile(name):
	filename = ""
	if(name == "Becas"):
		filename = "CoordLugares/Becas.txt"
	elif(name == "SubDireccion"):
		filename = "CoordLugares/SubDireccion.txt"
	elif(name == "Direccion"):
		filename = "CoordLugares/Direccion.txt"
	elif(name == "SEducativos"):
		filename = "CoordLugares/SEducativos.txt"
	elif(name == "SalaReunion"):
		filename = "CoordLugares/SalaReunion.txt"
	elif(name == "SAdministrativa"):
		filename = "CoordLugares/SubAdministrativa.txt"
	elif(name == "CHumano"):
		filename = "CoordLugares/CapitalHumano.txt"
	elif(name == "GTecnica"):
		filename = "CoordLugares/GestionTecnica.txt"
	elif(name == "TestA"):
		filename = "CoordLugares/TestA.txt"
	elif(name == "TestB"):
		filename = "CoordLugares/TestB.txt"
	elif(name == "TestC"):
		filename = "CoordLugares/TestC.txt"
	elif(name == "TestAS"):
		filename = "CoordLugares/TestAS2.txt"
	elif(name == "Robot"):
		objCaminante = getFilePosCaminante()
		return objCaminante.pos_x,objCaminante.pos_y,objCaminante.orientacion
	with open(os.path.join(__location__, filename), 'r') as f:
		l = f.readlines()
		xs = l[0].replace('x=', '')
		x = int(xs.replace('\n', ''))
		y = int(l[1].replace('y=', ''))
		salida = l[2].replace('salida=', '')
		return x,y,salida

def setUbicFinal(ubic):
	f = open(os.path.join(__location__, "UbicFinal.txt"), "w")
	f.write(ubic)
	f.close()
		
def getUbicFinal():
	with open(os.path.join(__location__, "UbicFinal.txt"), 'r') as f:
		l = f.readlines()
		ubicacion = l[0].replace('\n', '')
		return str(ubicacion)
		
def getPosition(array, value):
	position = np.where(array==value)
	y = position[0][0]
	x = position[1][0]
	return x,y


def getMapPrueba(nprueba):
	data_file = None
	if(nprueba==0):
		data_file = np.genfromtxt(os.path.join(__location__, 'ESCOM_Prueba1.csv'), delimiter=',').T
	elif(nprueba==1):
		data_file = np.genfromtxt(os.path.join(__location__, 'ESCOM_Prueba2.csv'), delimiter=',').T
	elif(nprueba==2):
		data_file = np.genfromtxt(os.path.join(__location__, 'ESCOM_Obstaculo_P2.csv'), delimiter=',').T
	colors = ["#002f68", "#4268c6", "#c70039", "#000000", 
          "#ECEC0A", "#348300", "#f1fce1", "#5A6051", "#97C363","#002f68"]  # use hex colors here, if desired.
	cmap = ListedColormap(colors)
	plt.imshow(data_file, vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation='nearest')#Forma visual, sera eliminado posteriormente
	plt.show()
	return data_file 
def getMapRuta():
	data_file = np.genfromtxt(os.path.join(__location__, 'ESCOM_Ruta_creada.csv'), delimiter=',')
	return data_file.T #arreglo ordenado

def getMapESCOM():
	data_file = np.genfromtxt(os.path.join(__location__, 'ESCOM_base.csv'), delimiter=',')
	return data_file.T #arreglo ordenado

def getMapESCOMObstaculo():
	data_file = np.genfromtxt(os.path.join(__location__, 'ESCOM_Obstaculo.csv'), delimiter=',')
	return data_file.T #arreglo ordenado

def getMapIPN():
	data_file = np.genfromtxt(os.path.join(__location__, 'IPN.csv'), delimiter=',')
	return data_file.T

def saveMap(data):#Salvando mapa despues de colocar puntos rojos
	os.remove(os.path.join(__location__, 'ESCOM_Obstaculo.csv'))
	aux = np.copy(data.T)
	DF = pd.DataFrame(aux)
	DF.to_csv(os.path.join(__location__, 'ESCOM_Obstaculo.csv'), index=False,  header=False )
	colors = ["#002f68", "#4268c6", "#c70039", "#000000", 
          "#ECEC0A", "#348300", "#f1fce1", "#5A6051", "#97C363","#002f68"]  # use hex colors here, if desired.
	cmap = ListedColormap(colors)

	plt.imshow(data, vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation='nearest')#Forma visual, sera eliminado posteriormente
	plt.show()
	
def saveRoute(data):#Salvando mapa despues de calcular ruta
	aux = np.copy(data.T)
	DF = pd.DataFrame(aux)
	DF.to_csv(os.path.join(__location__, 'ESCOM_Ruta_creada.csv'), index=False,  header=False )
	colors = ["#002f68", "#4268c6", "#c70039", "#000000", 
          "#ECEC0A", "#348300", "#f1fce1", "#5A6051", "#97C363","#002f68"]  # use hex colors here, if desired.
	cmap = ListedColormap(colors)

	plt.imshow(data, vmin=0, vmax=len(cmap.colors), cmap=cmap, interpolation='nearest')#Forma visual, sera eliminado posteriormente
	plt.show()

def getFilePosCaminante():
	with open(os.path.join(__location__, "caminante.txt")) as f:
		data = json.dumps(json.loads(f.read()))
		j = json.loads(data)
		u = Caminante(**j)
		if(u.orientacion == None):
			u.orientacion = getFilePosCaminantePass().orientacion
		return u
		
def getFilePosCaminantePass():
	with open(os.path.join(__location__, "caminantePass.txt")) as f:
		data = json.dumps(json.loads(f.read()))
		j = json.loads(data)
		u = Caminante(**j)
		return u
		
def caminanteEnd():
	x,y,salida=getPosFile(getUbicFinal())
	xR,yR,salidaR=getPosFile("Robot")
	if(x==xR and y==yR and salida==salidaR):
		return True
	return False

if __name__ == '__main__':#Sirve 100% para una sola ruta, i.e, de punto a a punto b, no de punto a a varios puntos
	#logicaPonerROjo(11)
	getPosFile("Robot")#corremos Archivo.py como el principal
#	simularmatar()
