from random import randint
import numpy as np
import pygame
import math
import Entropia
import threading
class MooreUltra:
    def __init__(self,nxC,nyC,pauseExect,gameState,mins,aux,regla,val,cont,dimCW,dimCH,screen,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,generacion,dibuja):
        self.nxC=nxC
        self.nyC=nyC
        self.pauseExect=pauseExect
        self.gameState=gameState
        self.mins=mins
        self.aux=aux
        self.regla=regla
        self.val=val
        self.cont=cont
        self.dimCW=dimCW
        self.dimCH=dimCH
        self.screen=screen
        self.generacion=generacion
        self.dibuja=dibuja
        
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
    
    

    def getMoore(self,n_neigh, crit):
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

    def MooreOffset(self,n_neigh, crit, orien):
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

    def depfun(self,estado, x, y, n_neigh,mins):
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
    
    def getNeibors(self,actual,n_neigh):
        auxi=[]
        for val in n_neigh:
            auxi.append(val)
        auxi.insert(4,actual)
        return auxi
    
    def calcularVecindadValor(self,arre,file):
        total=0
        x=0
        for x in range(len(arre)):
            if arre[x]!=0 and arre[x]!=2:
                total+=2**x      
        file.write(str(total)+'\n')
        
    def movimiento(self):
        for x in range(0,self.nxC):
                for y in range(0,self.nyC):
                    if(self.gameState[x][y] == 3):
                        self.val[x][y] = self.generacion+1
        for x in range(0, self.nxC):
            for y in range(0, self.nyC):
                if not self.pauseExect:
                    n_neigh = np.array([self.gameState[(x-1) % self.nxC, (y-1) % self.nyC], 
                                        self.gameState[(x) % self.nxC, (y-1) % self.nyC], 
                                        self.gameState[(x+1) % self.nxC, (y-1) % self.nyC], 
                                        self.gameState[(x-1) % self.nxC, (y) % self.nyC], 
                                        self.gameState[(x+1) % self.nxC, (y) % self.nyC], 
                                        self.gameState[(x-1) % self.nxC, (y+1) % self.nyC], 
                                        self.gameState[(x) % self.nxC, (y+1) % self.nyC], 
                                        self.gameState[(x+1) % self.nxC, (y+1) % self.nyC]])                    
                    
                    # Q0
                    if self.gameState[x, y] == 0:
                        if( self.mins[x,y] == 0 and ((self.randomOffset()+1)<7) and (self.getMoore(n_neigh,4) != 0 or self.getMoore(n_neigh,3) != 0 or self.getMoore(n_neigh,6) != 0) ):
                            self.aux[x, y] = 7
                            self.cont+=1
                            self.val[x, y] = self.cont
                        if(int(self.regla)==2):
                            if(self.getMoore(n_neigh,2) != 0):
                                self.aux[x, y] = 9
                    # Q1
                    elif self.gameState[x, y] == 1:
                        if(self.getMoore(n_neigh,5) != 0 or self.getMoore(n_neigh,6)!=0):
                            self.aux[x, y] = 6
                    # Q2 periodico, Q3 periodico, Q4
                    elif self.gameState[x, y] == 4: #Caso 0
                        if (self.getMoore(n_neigh,0) == 0 and self.getMoore(n_neigh,7) == 0):
                            d1 = self.val[x,y+1]
                            d2 = self.val[x-1,y+1]
                            d3 = self.val[x-1,y]
                            d4 = self.val[x-1,y-1]
                            d5 = self.val[x,y-1]
                            d6 = self.val[x+1,y-1]
                            d7 = self.val[x+1,y]
                            d8 = self.val[x+1,y+1]
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
                            if(d1 == peq and ( self.MooreOffset(n_neigh,3,1) or self.MooreOffset(n_neigh,5,1) or self.MooreOffset(n_neigh,6,1))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 1
                            elif(d2 == peq and ( self.MooreOffset(n_neigh,3,2) or self.MooreOffset(n_neigh,5,2) or self.MooreOffset(n_neigh,6,2))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 2
                            elif(d3 == peq and ( self.MooreOffset(n_neigh,3,3) or self.MooreOffset(n_neigh,5,3) or self.MooreOffset(n_neigh,6,3))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 3
                            elif(d4 == peq and ( self.MooreOffset(n_neigh,3,4) or self.MooreOffset(n_neigh,5,4) or self.MooreOffset(n_neigh,6,4))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 4  
                            elif(d5 == peq and ( self.MooreOffset(n_neigh,3,5) or self.MooreOffset(n_neigh,5,5) or self.MooreOffset(n_neigh,6,5))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 5
                            elif(d6 == peq and ( self.MooreOffset(n_neigh,3,6) or self.MooreOffset(n_neigh,5,6) or self.MooreOffset(n_neigh,6,6))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 6
                            elif(d7 == peq and ( self.MooreOffset(n_neigh,3,7) or self.MooreOffset(n_neigh,5,7) or self.MooreOffset(n_neigh,6,7))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 7
                            elif(d8 == peq and ( self.MooreOffset(n_neigh,3,8) or self.MooreOffset(n_neigh,5,8) or self.MooreOffset(n_neigh,6,8))):
                                self.aux[x,y] = 5
                                self.mins[x,y] = 8                            
                    # Q5
                    elif self.gameState[x, y] == 5:
                        if(not self.depfun(8,x,y,n_neigh,self.mins) and  not self.depfun(5,x,y,n_neigh,self.mins) and self.getMoore(n_neigh,6) == 0 and self.getMoore(n_neigh,4) == 0 and self.getMoore(n_neigh,1) == 0 and self.getMoore(n_neigh,3) == 0 ):
                            self.aux[x, y] = 0
                            self.mins[x, y] = 0
                        else:
                            self.aux[x, y] = 8
                    # Q6 periodico, Q7
                    elif self.gameState[x, y] == 7:
                        if( self.getMoore(n_neigh,5) > 0 or self.getMoore(n_neigh,6) > 0 or self.getMoore(n_neigh,3) > 0 or self.getMoore(n_neigh,4) > 0):
                            self.aux[x, y] = 4

                    elif self.gameState[x, y] == 8:
                        self.aux[x, y] = 5
                  
                if(self.dibuja):    
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
        
        return self.aux,self.mins,self.val