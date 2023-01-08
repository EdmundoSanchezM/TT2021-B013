from random import randint
import numpy as np
import pygame
class Neumann:
    def __init__(self,nxC,nyC,pauseExect,gameState,mins,aux,regla,val,cont,count4,count5,count7,count8,dimCW,dimCH,screen,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,entropiaGrafica,generacion):
        self.nxC=nxC
        self.nyC=nyC
        self.pauseExect=pauseExect
        self.gameState=gameState
        self.mins=mins
        self.aux=aux
        self.regla=regla
        self.val=val
        self.cont=cont
        self.count4=count4
        self.count5=count5
        self.count7=count7
        self.count8=count8
        self.dimCW=dimCW
        self.dimCH=dimCH
        self.screen=screen
        self.entropiaGrafica=entropiaGrafica
        self.generacion=generacion
        
        self.Q0 = Q0    # Campo libre
        self.Q1 = Q1    # Nutriente no encontrado
        self.Q2 = Q2    # Repelente
        self.Q3 = Q3    # Punto inicial
        self.Q4 = Q4    # Gel en concentracion
        self.Q5 = Q5    # Gel con compuesto
        self.Q6 = Q6    # Nutriente hallado
        self.Q7 = Q7    # Expansion del Physarum
        self.Q8 = Q8    # Gel sin compuesto
        self.Q9 = Q0    #q0+algo para la regla 2
        
        pass
    
    def randomOffset(self):
        return randint(0, ((7 + 1) - 0)) + 0

    def getNewman(self,n_neigh, crit): #Cambiar a moore despues xd
        x = 0
        if(n_neigh[3] == crit):
            x +=1
        if(n_neigh[1] == crit):
            x +=1
        if(n_neigh[0] == crit):
            x +=1
        if(n_neigh[2] == crit):
            x +=1
        return x
    
    def NewmanOffset(self,n_neigh, crit, orien):
        if(n_neigh[3] == crit and orien ==1):
            return True
        elif(n_neigh[1] == crit and orien ==2):
            return True
        elif(n_neigh[0] == crit and orien ==3):
            return True
        elif(n_neigh[2] == crit and orien ==4):
            return True
        return False



    def depfun(self,estado, x, y, n_neigh,mins):  # mide las dependecias
    # abajo,izq,derecha,arriba
        if(estado == n_neigh[3] and mins[x][y+1] == 3):
            return True
        elif(estado == n_neigh[1] and mins[x-1][y] == 4):
            return True
        elif(estado == n_neigh[0]and mins[x][y-1] == 1):
            return True
        elif(estado == n_neigh[2] and mins[x+1][y] == 2):
            return True
        return False
    
    def getNeibors(self,actual,n_neigh):
        auxi=[]
        for val in n_neigh:
            auxi.append(val)
        auxi.insert(2,actual)
        return auxi
    
    def calcularVecindadValor(self,arre,file):
        total=0
        x=0
        for x in range(len(arre)):
            if arre[x]!=0 and arre[x]!=2:
                total+=2**x      
        file.write(str(total)+'\n')
    
    def movimiento(self):
        file= open('entropia/EntroInfo.txt','a')
        for x in range(0, self.nxC):
            for y in range(0, self.nyC):
                if not self.pauseExect:
                    n_neigh = np.array([self.gameState[(x) % self.nxC, (y-1) % self.nyC],  
                                        self.gameState[(x-1) % self.nxC, (y) %self.nyC], 
                                        self.gameState[(x+1) % self.nxC, (y) % self.nyC], 
                                        self.gameState[(x) % self.nxC, (y+1) % self.nyC]])

                    if self.gameState[x, y] == 4:
                        self.count4 +=1
                    if self.gameState[x, y] == 5:
                        self.count5 +=1
                    if self.gameState[x, y] == 7:
                        self.count7 +=1
                    if self.gameState[x, y] == 8:
                        self.count8 +=1
                    if self.entropiaGrafica:
                        self.calcularVecindadValor(self.getNeibors(self.gameState[x, y],n_neigh),file)

                    # Q0
                    if self.gameState[x, y] == 0:
                        if( self.mins[x,y] == 0 and ((self.randomOffset()+1)<3) and (self.getNewman(n_neigh,4) != 0 or self.getNewman(n_neigh,3) != 0 or self.getNewman(n_neigh,6) != 0) ):
                            self.aux[x, y] = 7
                            self.cont+=1
                            self.val[x, y] = self.cont
                        if(int(self.regla)==2):
                            if(self.getNewman(n_neigh,2) != 0):
                                self.aux[x, y] = 9
                    # Q1
                    elif self.gameState[x, y] == 1:
                        if(self.getNewman(n_neigh,5) != 0 or self.getNewman(n_neigh,6)!=0):
                            self.aux[x, y] = 6
                    # Q2 periodico, Q3 periodico, Q4
                    elif self.gameState[x, y] == 4: #Caso 0
                        if (self.getNewman(n_neigh,0) == 0 and self.getNewman(n_neigh,7) == 0):
                            d1 = self.val[x,y+1]
                            d2 = self.val[x-1,y]
                            d3 = self.val[x,y-1]
                            d4 = self.val[x+1,y]
                            tempo = []
                            if( 3 == n_neigh[3] or 5 == n_neigh[3] or 6 == n_neigh[3]):
                                tempo.insert(0,d1)
                            if( 3 == n_neigh[1] or 5 == n_neigh[1] or 6 == n_neigh[1]):
                                tempo.insert(0,d2)
                            if( 3 == n_neigh[0] or 5 == n_neigh[0] or 6 == n_neigh[0]):
                                tempo.insert(0,d3)
                            if( 3 == n_neigh[2] or 5 == n_neigh[2] or 6 == n_neigh[2] ):
                                tempo.insert(0,d4)
                            linp = np.array(tempo)
                            peq = 0
                            if linp.size != 0:
                                peq = np.min(linp)
                            if(d1 == peq and ( self.NewmanOffset(n_neigh,3,1) or self.NewmanOffset(n_neigh,5,1) or self.NewmanOffset(n_neigh,6,1))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 1
                            elif(d2 == peq and ( self.NewmanOffset(n_neigh,3,2) or self.NewmanOffset(n_neigh,5,2) or self.NewmanOffset(n_neigh,6,2))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 2
                            elif(d3 == peq and ( self.NewmanOffset(n_neigh,3,3) or self.NewmanOffset(n_neigh,5,3) or self.NewmanOffset(n_neigh,6,3))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 3
                            elif(d4 == peq and ( self.NewmanOffset(n_neigh,3,4) or self.NewmanOffset(n_neigh,5,4) or self.NewmanOffset(n_neigh,6,4))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 4                            
                    # Q5
                    elif self.gameState[x, y] == 5:
                        if(not self.depfun(8,x,y,n_neigh,self.mins) and  not self.depfun(5,x,y,n_neigh,self.mins) and self.getNewman(n_neigh,6) == 0 and self.getNewman(n_neigh,4) == 0 and self.getNewman(n_neigh,1) == 0 and self.getNewman(n_neigh,3) == 0 ):
                            self.aux[x, y] = 0
                            self.mins[x, y] = 0
                        else:
                            self.aux[x, y] = 8
                    # Q6 periodico, Q7
                    elif self.gameState[x, y] == 7:
                        if( self.getNewman(n_neigh,5) > 0 or self.getNewman(n_neigh,6) > 0 or self.getNewman(n_neigh,3) > 0 or self.getNewman(n_neigh,4) > 0):
                            self.aux[x, y] = 4
                    elif self.gameState[x, y] == 8:
                        self.aux[x, y] = 5
                        
                poly = [((x)*self.dimCW, y*self.dimCH),
                        ((x+1)*self.dimCW, y*self.dimCH),
                        ((x+1)*self.dimCW, (y+1)*self.dimCH),
                        ((x)*self.dimCW, (y+1)*self.dimCH)]


                if(self.aux[x, y] == 0):
                    pygame.draw.polygon(self.screen, self.Q0, poly, 0)
                elif(self.aux[x, y] == 1):
                    pygame.draw.polygon(self.screen, self.Q1, poly, 0)
                elif(self.aux[x, y] == 2):
                    pygame.draw.polygon(self.screen, self.Q2, poly, 0)
                elif(self.aux[x, y] == 3):
                    pygame.draw.polygon(self.screen, self.Q3, poly, 0)
                elif(self.aux[x, y] == 4):
                    pygame.draw.polygon(self.screen, self.Q4, poly, 0)
                elif(self.aux[x, y] == 5):
                    pygame.draw.polygon(self.screen, self.Q5, poly, 0)
                elif(self.aux[x, y] == 6):
                    pygame.draw.polygon(self.screen, self.Q6, poly, 0)
                elif(self.aux[x, y] == 7):
                    pygame.draw.polygon(self.screen, self.Q7, poly, 0)
                elif(self.aux[x, y] == 8):
                    pygame.draw.polygon(self.screen, self.Q8, poly, 0)
                elif(self.aux[x, y] == 9):
                    pygame.draw.polygon(self.screen, self.Q9, poly, 0) 
        
        if(self.generacion>1 and not self.pauseExect and self.entropiaGrafica):
            file.write('---------\n')
            file.close()
        
        return self.aux,self.count4,self.count5,self.count7,self.count8,self.cont,self.mins,self.val