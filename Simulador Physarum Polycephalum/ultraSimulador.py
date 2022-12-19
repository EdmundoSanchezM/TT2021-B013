from MooreUltra import MooreUltra
import pygame, sys
import numpy as np
import time
import pylab
import math
import tkinter
import tkinter.filedialog
import tkinter.simpledialog
from tkinter import colorchooser
import matplotlib
matplotlib.use("Agg")
import matplotlib.animation as animation
import matplotlib.backends.backend_agg as agg
from random import randint
from tkinter import *
from PIL import ImageColor
from boton import Button
from boton import setTexto
from boton import buttons_draw 
from imagenImp import loadPixelArt, saveImagen
from graficas import Graficas
from screeninfo import get_monitors
from Moore import Moore
from Neumann import Neumann
import tkinter as tk
import pandas as pd
global pauseExect,aux,gameState,mins,val,generacion,count4,count5,count7,count8,textoBoton,boxactual,graficaActual,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8
textoBoton =''
def Simulador (celulas,regla,vecindad):
    global pauseExect,aux,gameState,mins,val,generacion,count4,count5,count7,count8,textoBoton,boxactual,cont,graficaActual,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8 
    screenHeigt=[]
    screenWidth=[]
    for m in get_monitors():
        screenHeigt.append(int(m.height))
        screenWidth.append(int(m.width))
    
    print("Usando la vecindad de ",vecindad)
            
    TotalLargo=math.ceil(screenHeigt[0]*0.6944)

    Q0 = "#002f68"  # Campo libre
    Q1 = "#4268c6"  # Nutriente no encontrado
    Q2 = "#c70039" # Repelente
    Q3 = "#000000"  # Punto inicial
    Q4 = "#ECEC0A"  # Gel en concentracion
    Q5 = "#348300" # Gel con compuesto
    Q6 = "#f1fce1" # Nutriente hallado
    Q7 = "#5A6051"  # Expansion del Physarum
    Q8 = "#97C363"  # Gel sin compuesto
    Q9 = "#002f68" #q0+algo para la regla 2
    
    
    window = Tk()
    PixelesXlado=TotalLargo
    height,width = PixelesXlado, PixelesXlado
    
    nxC, nyC = celulas, celulas
    dimCW = width/celulas
    dimCH = height/celulas
    
    pygame.init()

    screen = pygame.display.set_mode([height, width], pygame.DOUBLEBUF)

    
    myfont = pygame.font.SysFont("monospace", 30)

    bg = 0, 47, 104
    screen.fill(bg)
    gameState = np.zeros((nxC, nyC))

    pauseExect = True
    running = True
    
    mins = np.zeros((nxC, nyC))
    cont = 0
    val = np.zeros((nxC, nyC))
    generacion = 0
    aux = np.copy(gameState)
    graficaActual=0
    boxactual=0
    #contadores

    count4 = 0 #Q4
    count5 = 0 #Q5
    count7 = 0 #Q7
    count8 = 0 #Q8

    pygame.display.update()
    
    def pausar():
        global pauseExect
        pauseExect = not pauseExect
        
    def clear():
        global pauseExect,aux,gameState,mins,val,generacion,count4,count5,count7,count8,boxactual,graficaActual,cont
        aux = np.zeros((nxC, nyC))
        gameState = np.zeros((nxC, nyC))
        mins = np.zeros((nxC, nyC))
        val = np.zeros((nxC, nyC))
        aux=margen()
        generacion = 0
        cont = 0
        boxactual=0
        graficaActual=0
        count4 = 0 #Q4
        count5 = 0 #Q5
        count7 = 0 #Q7
        count8 = 0 #Q8
        
    def abrir():
        global aux,mins
        window.withdraw() 
        filename = tkinter.filedialog.askopenfilename()
        extencion=filename.split(".")[-1]
        print("abriendo, ",extencion)
        try:
            if(extencion=='png'):
                aux,mins=loadImage(filename)
            elif (extencion=='txt'):
                aux,mins=load(filename,celulas)
            else: 
                print('Extencion no reconocida')
        except:
            print('No se selecciono un archivo')
        
    def guardar():
        window.withdraw()
        txt = tkinter.simpledialog.askstring(title="Save",prompt="What will  be the name of your text?:")
        save(txt,gameState)
        
    def desplegarHelp():
        window.withdraw()
        mensaje="""
0) Campo libre
1) Nutriente no encontrado
2) Repelente
3) Punto inicial
4) Gel en concentracion
5) Gel con compuesto
6) Nutriente hallado
7) Expansion del Physarum
8) Gel sin compuesto
        """
        tkinter.messagebox.showinfo(message=mensaje, title="Estados")

    def margen():
        aux = np.copy(gameState)
        for y in range(0, nyC):
            for x in range(0, nxC):
                if(y==0 or y==nyC-1 or x==0 or x==nxC-1):
                    aux[x, y] = 2
        return aux 

    def save(filename,gameState):
        # print("abriendo: ",filename)
        # f = open('save/'+str(vecindad)+'/'+str(filename)+'_'+str(celulas)+'.txt','w')
        # aux = np.copy(gameState)
        # for y in range(0, nxC):
        #     for x in range(0, nyC):
        #         f.write(str(x)+","+str(y)+","+str(aux[x, y])+","+str(mins[x, y])+"\n")
        # f.close
        aux = np.copy(gameState)
        DF = pd.DataFrame(aux)
        DF.to_csv('filename.csv', index=False,  header=False )
        
    def getNuberLines(filename):
        count = 0
        with open(filename,encoding="utf8") as f:
            lines = f.readlines()
            for line in lines:
                count +=1
        return int(math.sqrt(count))
    

    def loadImage(filename):
        clon = loadPixelArt(filename,nxC,nyC)
        clonMins = np.zeros((nxC, nyC))
        return clon,clonMins
    
    def load(filename,celulas):
        clon = np.zeros((nxC, nyC))
        clonMins = np.zeros((nxC, nyC))
        numauxi=getNuberLines(filename)
        with open(filename) as f:
            lines = f.readlines()
            
            if numauxi==celulas:
                for line in lines:
                    auxi=line.split(',')
                    x = int(auxi[0])
                    y = int(auxi[1])
                    tipo= auxi[2]
                    mini= auxi[3]
                    clon[x][y]=tipo
                    clonMins[x][y]=mini
            else:
                clon=saveImagen(filename,int(numauxi),int(celulas))
        return clon,clonMins
    
    while running:
        aux=margen()#Pone el margen de repelentes al rededor        
        
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                window.withdraw()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pauseExect = not pauseExect
                if event.key == pygame.K_c:
                    aux = np.zeros((nxC, nyC))
                    gameState = np.zeros((nxC, nyC))
                    mins = np.zeros((nxC, nyC))
                    val = np.zeros((nxC, nyC))
                    aux=margen()
                    generacion = 0
                    count4 = 0 #Q4
                    count5 = 0 #Q5
                    count7 = 0 #Q7
                    count8 = 0 #Q8
                    
                if event.key == pygame.K_a:
                    abrir()

                if event.key == pygame.K_g:
                    window.withdraw()
                    txt = tkinter.simpledialog.askstring(title="Save",prompt="Ingresa el nombre de tu archivo, se le agregara la extencion y las celulas por lado")
                    save(txt,gameState)
                    
    
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
                
        if not pauseExect:
            generacion +=1
        #Creacion de la instancia para las vecindades
        if vecindad == 'neumann':
            comportamiento = Neumann(nxC,nyC,pauseExect,gameState,mins,aux,regla,val,cont,count4,count5,count7,count8, dimCW,dimCH,screen,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,False,generacion)
        elif vecindad == 'moore':
            comportamiento = MooreUltra(nxC,nyC,pauseExect,gameState,mins,aux,regla,val,cont,dimCW,dimCH,screen,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,generacion,True)
        
        
        aux,mins,val= comportamiento.movimiento()
                        
        gameState = np.copy(aux)
        
        #textos
        texto= "Generacion: "+str(generacion)
        label = myfont.render(texto, 1, (255,255,255))
        screen.blit(label, (17, 15))
        
        #checkbox
        
        #actualizar animacion
        
        pygame.display.update()

    pygame.quit()
    
if __name__ == "__main__":
    Simulador(200,1,'moore')
