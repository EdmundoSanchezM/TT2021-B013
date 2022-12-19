#MAIN
import numpy as np
from random import randint
import os
import Caminante
from Archivo import setPIDFile, saveRoute, getMapESCOM,getPosFile,getMapRuta,getMapESCOMObstaculo,setUbicFinal
from MoverCaminante import iniciarCaminata
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def getPID():
	pid = os.getpid()
	print("PID main", pid)
	return pid

def Simulador (gameState,origen,destino):
    nxC, nyC =70, 70
    running = True
    mins = np.zeros((nxC, nyC))
    cont = 0
    val = np.zeros((nxC, nyC))
    incre = 0
    aux = np.copy(gameState)
    count5 = 0 #Q5
    count8 = 0 #Q8
    testuwu = np.copy(gameState)
    def randomOffset():
        return randint(0, ((7 + 1) - 0)) + 0

    def getMoore(n_neigh, crit):
        x = 0
        if(n_neigh[0] == crit):
            x +=1
        if(n_neigh[1] == crit):
            x +=1
        if(n_neigh[2] == crit):
            x +=1
        if(n_neigh[3] == crit):
            x +=1
        if(n_neigh[4] == crit):
            x +=1
        if(n_neigh[5] == crit):
            x +=1
        if(n_neigh[6] == crit):
            x +=1
        if(n_neigh[7] == crit):
            x +=1
        return x

    def MooreOffset(n_neigh, crit, orien):
        if(n_neigh[6] == crit and orien ==1):
            return True
        if(n_neigh[5] == crit and orien ==2):
            return True
        if(n_neigh[3] == crit and orien ==3):
            return True
        if(n_neigh[0] == crit and orien ==4):
            return True
        if(n_neigh[1] == crit and orien ==5):
            return True
        if(n_neigh[7] == crit and orien ==8):
            return True
        if(n_neigh[4] == crit and orien ==7):
            return True
        if(n_neigh[2] == crit and orien ==6):
            return True
        return False

    def depfun(estado, x, y, n_neigh):
        if(estado == n_neigh[6] and mins[x][y+1] == 5):
            return True
        if(estado == n_neigh[5] and mins[x-1][y+1] == 6):
            return True
        if(estado == n_neigh[3]and mins[x-1][y] == 7):
            return True
        if(estado == n_neigh[0] and mins[x-1][y-1] == 8):
            return True
        if(estado == n_neigh[1] and mins[x][y-1] == 1):
            return True
        if(estado == n_neigh[2]and mins[x+1][y-1] == 2):
            return True
        if(estado == n_neigh[4] and mins[x+1][y] == 3):
            return True
        if(estado == n_neigh[7] and mins[x+1][y+1] == 4):
            return True
        return False

    while running:
        testuwu = np.copy(gameState)
        incre +=1
        count5 = 0 #Q5
        count8 = 0 #Q8
        for x in range(0,nxC):
            for y in range(0,nyC):
                if(gameState[x][y] == 3):
                    val[x][y] = incre+1
        for x in range(0, nxC):
            for y in range(0, nyC):
                n_neigh = np.array([gameState[(x-1) % nxC, (y-1) % nyC], 
                                    gameState[(x) % nxC, (y-1) % nyC], 
                                    gameState[(x+1) % nxC, (y-1) % nyC], 
                                    gameState[(x-1) % nxC, (y) % nyC], 
                                    gameState[(x+1) % nxC, (y) % nyC], 
                                    gameState[(x-1) % nxC, (y+1) % nyC], 
                                    gameState[(x) % nxC, (y+1) % nyC], 
                                    gameState[(x+1) % nxC, (y+1) % nyC]])

                if gameState[x, y] == 5:
                    count5 +=1
                if gameState[x, y] == 8:
                    count8 +=1
                # Q0
                if gameState[x, y] == 0:
                    if( mins[x,y] == 0 and ((randomOffset()+1)<7) and (getMoore(n_neigh,4) != 0 or getMoore(n_neigh,3) != 0 or getMoore(n_neigh,6) != 0) ):
                        aux[x, y] = 7
                        cont+=1
                        val[x, y] = cont
                    
                    if(getMoore(n_neigh,2) != 0):
                        aux[x, y] = 9
                # Q1
                elif gameState[x, y] == 1:
                    if(getMoore(n_neigh,5) != 0 or getMoore(n_neigh,6)!=0):
                        aux[x, y] = 6
                # Q2 periodico, Q3 periodico, Q4
                elif gameState[x, y] == 4: #Caso 0
                    if (getMoore(n_neigh,0) == 0 and getMoore(n_neigh,7) == 0):
                        d1 = val[x,y+1]
                        d2 = val[x-1,y+1]
                        d3 = val[x-1,y]
                        d4 = val[x-1,y-1]
                        d5 = val[x,y-1]
                        d6 = val[x+1,y-1]
                        d7 = val[x+1,y]
                        d8 = val[x+1,y+1]
                        tempo = []
                        if( 3 == n_neigh[6] or 5 == n_neigh[6] or 6 == n_neigh[6]):
                            tempo.insert(0,d1)
                        if( 3 == n_neigh[5] or 5 == n_neigh[5] or 6 == n_neigh[5]):
                            tempo.insert(0,d2)
                        if( 3 == n_neigh[3] or 5 == n_neigh[3] or 6 == n_neigh[3]):
                            tempo.insert(0,d3)
                        if( 3 == n_neigh[0] or 5 == n_neigh[0] or 6 == n_neigh[0] ):
                            tempo.insert(0,d4)
                        if( 3 == n_neigh[1] or 5 == n_neigh[1] or 6 == n_neigh[1]):
                                tempo.insert(0,d5)
                        if( 3 == n_neigh[2] or 5 == n_neigh[2] or 6 == n_neigh[2]):
                            tempo.insert(0,d6)
                        if( 3 == n_neigh[4] or 5 == n_neigh[4] or 6 == n_neigh[4]):
                                tempo.insert(0,d7)
                        if( 3 == n_neigh[7] or 5 == n_neigh[7] or 6 == n_neigh[7] ):
                            tempo.insert(0,d8)
                        linp = np.array(tempo)
                        peq = 0
                        if linp.size != 0:
                            peq = np.min(linp)
                        if(d1 == peq and ( MooreOffset(n_neigh,3,1) or MooreOffset(n_neigh,5,1) or MooreOffset(n_neigh,6,1))):
                            aux[x,y] = 5
                            mins[x,y] = 1
                        elif(d2 == peq and ( MooreOffset(n_neigh,3,2) or MooreOffset(n_neigh,5,2) or MooreOffset(n_neigh,6,2))):
                            aux[x,y] = 5
                            mins[x,y] = 2
                        elif(d3 == peq and ( MooreOffset(n_neigh,3,3) or MooreOffset(n_neigh,5,3) or MooreOffset(n_neigh,6,3))):
                            aux[x,y] = 5
                            mins[x,y] = 3
                        elif(d4 == peq and ( MooreOffset(n_neigh,3,4) or MooreOffset(n_neigh,5,4) or MooreOffset(n_neigh,6,4))):
                            aux[x,y] = 5
                            mins[x,y] = 4  
                        elif(d5 == peq and ( MooreOffset(n_neigh,3,5) or MooreOffset(n_neigh,5,5) or MooreOffset(n_neigh,6,5))):
                            aux[x,y] = 5
                            mins[x,y] = 5
                        elif(d6 == peq and ( MooreOffset(n_neigh,3,6) or MooreOffset(n_neigh,5,6) or MooreOffset(n_neigh,6,6))):
                            aux[x,y] = 5
                            mins[x,y] = 6
                        elif(d7 == peq and ( MooreOffset(n_neigh,3,7) or MooreOffset(n_neigh,5,7) or MooreOffset(n_neigh,6,7))):
                            aux[x,y] = 5
                            mins[x,y] = 7
                        elif(d8 == peq and ( MooreOffset(n_neigh,3,8) or MooreOffset(n_neigh,5,8) or MooreOffset(n_neigh,6,8))):
                            aux[x,y] = 5
                            mins[x,y] = 8                            
                # Q5
                elif gameState[x, y] == 5:
                    if(not depfun(8,x,y,n_neigh) and  not depfun(5,x,y,n_neigh) and getMoore(n_neigh,6) == 0 and getMoore(n_neigh,4) == 0 and getMoore(n_neigh,1) == 0 and getMoore(n_neigh,3) == 0 ):
                        aux[x, y] = 0
                        mins[x, y] = 0
                    else:
                        aux[x, y] = 8
                # Q6 periodico, Q7
                elif gameState[x, y] == 7:
                    if( getMoore(n_neigh,5) > 0 or getMoore(n_neigh,6) > 0 or getMoore(n_neigh,3) > 0 or getMoore(n_neigh,4) > 0):
                        aux[x, y] = 4                            
                elif gameState[x, y] == 8:
                    aux[x, y] = 5
        gameState = np.copy(aux)
        if(len(np.where(gameState==6)[0]) != 0 and len(np.where(gameState==4)[0]) == 0 and len(np.where(gameState==7)[0]) == 0 ):
            temporalgs = np.copy(gameState)
            temporalgs[temporalgs == 5] = 77
            temporalgs[temporalgs == 8] = 5
            temporalgs[temporalgs == 77] = 8
            comparison = testuwu == temporalgs
            equal_arrays = comparison.all()
            if(equal_arrays):
                saveRoute(gameState)
                data = getMapRuta()
                iniPos_x, iniPos_y, salida = getPosFile(origen)
                finPos_x, finPos_y, entrada = getPosFile(destino)
                caminador = Caminante.Caminante(salida, iniPos_x, iniPos_y,finPos_x,finPos_y)
                print(data[finPos_y][finPos_x])
                print(caminador.orientacion)
                if(iniciarCaminata(caminador, data, entrada)):
                    print("Fin del caminante: \nDatos del caminante")
                    print("Orientacion final",caminador.orientacion)
                    print("Coordenada x final",caminador.pos_x)
                    print("Coordenada y final",caminador.pos_y)
                break
              
def lanzadorR(lugarI, lugarF, tipo):
	setPIDFile(getPID())
	setUbicFinal(lugarF)
	data = None
	print(tipo)
	if(tipo == 0):#Usa el mapa basico
		data = getMapESCOM()
	elif(tipo == 1):#Usa el mapa con obstaculo
		data = getMapESCOMObstaculo()
	origen = lugarI
	destino = lugarF
	iniPos_x, iniPos_y, salida = getPosFile(origen)
	print(destino)
	finPos_x, finPos_y, entrada = getPosFile(destino)
	data[finPos_y][finPos_x] = 1 #fin
	data[iniPos_y][iniPos_x] = 3 #inicio
	gameState = data
	saveRoute(gameState)
	Simulador(gameState,origen,destino)
