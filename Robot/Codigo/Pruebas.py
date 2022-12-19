#MAIN
import numpy as np
from random import randint
import os,sys
import Caminante
from Archivo import setPIDFile,getPosFile,setUbicFinal,getMapPrueba
from MoverCaminante import iniciarCaminata
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def getPID():
	pid = os.getpid()
	print("PID main", pid)
	return pid

def Simulador(gameState,origen,destino,xd):
    iniPos_x, iniPos_y, salida = getPosFile(origen)
    finPos_x, finPos_y, entrada = getPosFile(destino)
    caminador = Caminante.Caminante(salida, iniPos_x, iniPos_y,finPos_x,finPos_y)
    print(caminador)
    if(iniciarCaminata(caminador, gameState, entrada,xd)):
        print("Fin del caminante: \nDatos del caminante")
        print("Orientacion final",caminador.orientacion)
        print("Coordenada x final",caminador.pos_x)
        print("Coordenada y final",caminador.pos_y)
              
def lanzadorR(lugarI, lugarF,nprueba,xd):
    setPIDFile(getPID())
    setUbicFinal(lugarF)
    #Prueebas
    origen = lugarI
    destino = lugarF
    data = getMapPrueba(nprueba)
    Simulador(data,origen,destino,xd)

print('cmd entry:', sys.argv)
#prueba1: de TestA a testB
lanzadorR("TestA","TestB",0,True)
#prueba2: de TestB a testC
#lanzadorR("TestA","TestC",1,True)
