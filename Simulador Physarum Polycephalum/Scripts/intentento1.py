import pygame
import numpy as np
import time,threading
from random import randint

width, height = 1000, 1000
nxC, nyC = 500, 500
dimCW = width/nxC
dimCH = height/nyC

pygame.init()

screen = pygame.display.set_mode([height, width])

bg = 0, 47, 104
screen.fill(bg)

gameState = np.zeros((nxC, nyC))


pauseExect = True
running = True

Q0 = 0, 47, 104  # Campo libre
Q1 = 66, 104, 198  # Nutriente no encontrado
Q2 = 199, 0, 57  # Repelente
Q3 = 0, 0, 0  # Punto inicial
Q4 = 236, 236, 10  # Gel en concentracion
Q5 = 52, 131, 0  # Gel con compuesto
Q6 = 241, 252, 225  # Nutriente hallado
Q7 = 90, 96, 81  # Expansion del Physarum
Q8 = 151, 195, 99  # Gel sin compuesto
mins = np.zeros((nxC, nyC))
cont = 0
val = np.zeros((nxC, nyC))
incre = 0

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
    elif(estado == n_neigh[5] and mins[x-1][y+1] == 6):
        return True
    elif(estado == n_neigh[3]and mins[x-1][y] == 7):
        return True
    elif(estado == n_neigh[0] and mins[x-1][y-1] == 8):
        return True
    elif(estado == n_neigh[1] and mins[x][y-1] == 1):
        return True
    elif(estado == n_neigh[2]and mins[x+1][y-1] == 2):
        return True
    elif(estado == n_neigh[4] and mins[x+1][y] == 3):
        return True
    elif(estado == n_neigh[7] and mins[x+1][y+1] == 4):
        return True
    return False

def Margen():
    aux = np.copy(gameState)
    for y in range(0, nxC):
        for x in range(0, nyC):
            if(y==0 or y==nyC-1 or x==0 or x==nxC-1):
                aux[x, y] = 2
    return aux

def dibujar(num):
    cont=0
    for x in range(num, num+100):
        for y in range(0, nyC):
            if not pauseExect:
                n_neigh = np.array([gameState[(x-1) % nxC, (y-1) % nyC], 
                                    gameState[(x) % nxC, (y-1) % nyC], 
                                    gameState[(x+1) % nxC, (y-1) % nyC], 
                                    gameState[(x-1) % nxC, (y) % nyC], 
                                    gameState[(x+1) % nxC, (y) % nyC], 
                                    gameState[(x-1) % nxC, (y+1) % nyC], 
                                    gameState[(x) % nxC, (y+1) % nyC], 
                                    gameState[(x+1) % nxC, (y+1) % nyC]])
                
                # Q0
                if gameState[x, y] == 0:
                    if( mins[x,y] == 0 and ((randomOffset()+1)<7) and (getMoore(n_neigh,4) != 0 or getMoore(n_neigh,3) != 0 or getMoore(n_neigh,6) != 0) ):
                        aux[x, y] = 7
                        cont+=1
                        val[x, y] = cont
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
                            #metida de dedo
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
                    
            poly = [((x)*dimCW, y*dimCH),
                    ((x+1)*dimCW, y*dimCH),
                    ((x+1)*dimCW, (y+1)*dimCH),
                    ((x)*dimCW, (y+1)*dimCH)]

            if(aux[x, y] == 0):
                pygame.draw.polygon(screen, (Q0), poly, 0)
            elif(aux[x, y] == 1):
                pygame.draw.polygon(screen, (Q1), poly, 0)
            elif(aux[x, y] == 2):
                pygame.draw.polygon(screen, (Q2), poly, 0)
            elif(aux[x, y] == 3):
                pygame.draw.polygon(screen, (Q3), poly, 0)
            elif(aux[x, y] == 4):
                pygame.draw.polygon(screen, (Q4), poly, 0)
            elif(aux[x, y] == 5):
                pygame.draw.polygon(screen, (Q5), poly, 0)
            elif(aux[x, y] == 6):
                pygame.draw.polygon(screen, (Q6), poly, 0)
            elif(aux[x, y] == 7):
                pygame.draw.polygon(screen, (Q7), poly, 0)
            elif(aux[x, y] == 8):
                pygame.draw.polygon(screen, (Q8), poly, 0)

while running:
    aux = np.copy(gameState)
    aux=Margen()
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
            if mouseClick[0] == 1:
                aux[celX, celY] = 3
            elif mouseClick[1] == 1:
                aux[celX, celY] = 1
            else:
                aux[celX, celY] = 2
    screen.fill(bg)
    #print(val)
    
    hilo1 = threading.Thread(name='chequear', 
                         target=dibujar,
                         args=(0,))
    hilo2 = threading.Thread(name='chequear', 
                         target=dibujar,
                         args=(100,))
    hilo3 = threading.Thread(name='chequear', 
                             target=dibujar,
                             args=(200,))

    hilo4 = threading.Thread(name='chequear', 
                             target=dibujar,
                             args=(300,))

    hilo5 = threading.Thread(name='chequear', 
                             target=dibujar,
                             args=(400,))

    hilo1.start()
    hilo2.start()
    hilo3.start()
    hilo4.start()
    hilo5.start()
    
    hilo1.join()
    hilo2.join()
    hilo3.join()
    hilo4.join()
    hilo5.join()
    
    print(incre)
    gameState = np.copy(aux)
    pygame.display.flip()

pygame.quit()
