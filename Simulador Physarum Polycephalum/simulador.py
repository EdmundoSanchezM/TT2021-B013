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
from imagenImp import saveImagen
from graficas import Graficas
from screeninfo import get_monitors
from Moore import Moore
from Neumann import Neumann
import tkinter as tk
global pauseExect,aux,gameState,mins,val,generacion,count4,count5,count7,count8,textoBoton,delay,boxactual,graficaActual,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8
textoBoton =''
def Simulador (celulas,regla,vecindad,entro):
    global pauseExect,aux,gameState,mins,val,generacion,count4,count5,count7,count8,textoBoton,delay,boxactual,cont,graficaActual,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8 
    screenHeigt=[]
    screenWidth=[]
    for m in get_monitors():
        screenHeigt.append(int(m.height))
        screenWidth.append(int(m.width))
    
    print("Usando la vecindad de ",vecindad)
            
    TotalLargo=math.ceil(screenHeigt[0]*0.6944)
    grafica=math.ceil(TotalLargo*0.60)
    ladoGrafica=math.ceil(grafica/100)

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
    
    fig = pylab.figure(figsize=[ladoGrafica, ladoGrafica-1],dpi=100,)
    ax = fig.add_subplot()
    ax.clear()
    #Grafica de crecimiento de estados
    ani = animation.FuncAnimation(fig, Graficas(ax,Q4,Q5,Q7,Q8).crecimiento,interval=1)
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    
    window = Tk()
    PixelesXlado=TotalLargo
    height,width = PixelesXlado, PixelesXlado
    
    nxC, nyC = celulas, celulas
    dimCW = width/celulas
    dimCH = height/celulas
    
    pygame.init()

    screen = pygame.display.set_mode([height+grafica, width], pygame.DOUBLEBUF)

    size = canvas.get_width_height()
    gui_font = pygame.font.Font(None,30)
    
    ladoExtra=int(math.ceil(PixelesXlado*0.2))
    otroExtra=int(math.ceil(PixelesXlado*0.05))
    
    button0 = Button('Sig grafica',200,30,(PixelesXlado+ladoExtra,PixelesXlado-(otroExtra*7.9)),5,gui_font,screen)
    
    button1 = Button('Iniciar/Pausar',200,30,(PixelesXlado+ladoExtra,PixelesXlado-(otroExtra*6)),5,gui_font,screen)
    button2 = Button('Reiniciar',200,30,(PixelesXlado+ladoExtra,PixelesXlado-(otroExtra*5)),5,gui_font,screen)
    button3 = Button('Abrir',200,30,(PixelesXlado+ladoExtra,PixelesXlado-(otroExtra*4)),5,gui_font,screen)
    button4 = Button('Guardar',200,30,(PixelesXlado+ladoExtra,PixelesXlado-(otroExtra*3)),5,gui_font,screen)
    buttonColor = Button('Color',60,30,(PixelesXlado+ladoExtra+140,PixelesXlado-(otroExtra*2)),5,gui_font,screen)
    button5 = Button('+',40,40,(PixelesXlado+ladoExtra +190,PixelesXlado-(otroExtra*7)),5,gui_font,screen)
    button6 = Button('-',40,40,(PixelesXlado+ladoExtra -30,PixelesXlado-(otroExtra*7)),5,gui_font,screen)
    
    buttonEstado0 = Button('0',30,30,(PixelesXlado+ladoExtra -80,PixelesXlado-(otroExtra*1)),5,gui_font,screen)
    buttonEstado1 = Button('1',30,30,(PixelesXlado+ladoExtra -40,PixelesXlado-(otroExtra*1)),5,gui_font,screen)
    buttonEstado2 = Button('2',30,30,(PixelesXlado+ladoExtra +00,PixelesXlado-(otroExtra*1)),5,gui_font,screen)
    buttonEstado3 = Button('3',30,30,(PixelesXlado+ladoExtra +40,PixelesXlado-(otroExtra*1)),5,gui_font,screen)
    buttonEstado4 = Button('4',30,30,(PixelesXlado+ladoExtra +80,PixelesXlado-(otroExtra*1)),5,gui_font,screen)
    buttonEstado5 = Button('5',30,30,(PixelesXlado+ladoExtra +120,PixelesXlado-(otroExtra*1)),5,gui_font,screen)
    buttonEstado6 = Button('6',30,30,(PixelesXlado+ladoExtra +160,PixelesXlado-(otroExtra*1)),5,gui_font,screen)
    buttonEstado7 = Button('7',30,30,(PixelesXlado+ladoExtra +200,PixelesXlado-(otroExtra*1)),5,gui_font,screen)
    buttonEstado8 = Button('8',30,30,(PixelesXlado+ladoExtra +240,PixelesXlado-(otroExtra*1)),5,gui_font,screen)
    
    buttonHelp = Button('?',30,30,(height+grafica-30, width-30),5,gui_font,screen)
    buttons= [button0,button1,button2,button3,button4,button5,button6,buttonColor,buttonEstado0,buttonEstado1,buttonEstado2,buttonEstado3,buttonEstado4,buttonEstado5,buttonEstado6,buttonEstado7,buttonEstado8,buttonHelp]
    
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
    delay=0
    graficaActual=0
    boxactual=0
    #contadores

    count4 = 0 #Q4
    count5 = 0 #Q5
    count7 = 0 #Q7
    count8 = 0 #Q8

    listgene= []
    list4=[]
    list5=[]
    list7=[]
    list8=[]
    buttons_draw(buttons)
    pygame.display.update()

    file= open('data.txt','w')
    file.write(str(generacion)+','+str(count4)+','+str(count5)+','+str(count7)+','+str(count8)+'\n')
    file.close()
    
    file= open('entropia/EntroInfo.txt','w')
    file.write('')
    file.close()
    
    def pausar():
        global pauseExect
        pauseExect = not pauseExect
        
    def clear():
        global pauseExect,aux,gameState,mins,val,generacion,count4,count5,count7,count8,delay,boxactual,graficaActual,cont
        aux = np.zeros((nxC, nyC))
        gameState = np.zeros((nxC, nyC))
        mins = np.zeros((nxC, nyC))
        val = np.zeros((nxC, nyC))
        aux=margen()
        generacion = 0
        delay=0
        cont = 0
        boxactual=0
        graficaActual=0
        file= open('data.txt','w')
        file.write('')
        file.close() 
        file= open('entropia/EntroInfo.txt','w')
        file.write('')
        file.close()
        count4 = 0 #Q4
        count5 = 0 #Q5
        count7 = 0 #Q7
        count8 = 0 #Q8
        
    def abrir():
        global aux,mins
        window.withdraw() 
        filename = tkinter.filedialog.askopenfilename()
        try:
            aux,mins=load(filename,celulas)
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
        f = open('save/'+str(vecindad)+'/'+str(filename)+'_'+str(celulas)+'.txt','w')
        aux = np.copy(gameState)
        for y in range(0, nxC):
            for x in range(0, nyC):
                f.write(str(x)+","+str(y)+","+str(aux[x, y])+","+str(mins[x, y])+"\n")
        f.close

    def getNuberLines(filename):
        count = 0
        with open(filename,encoding="utf8") as f:
            lines = f.readlines()
            for line in lines:
                count +=1
        return int(math.sqrt(count))
    

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
    
    def escogerColor(boxactual):
        global Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8
        window.withdraw()
        if boxactual==0:
            coloraux=Q0
            Q0 = colorchooser.askcolor()[1]
            if(Q0==None):
                Q0=coloraux
        if boxactual==1:
            coloraux=Q1
            Q1 = colorchooser.askcolor()[1]
            if(Q1==None):
                Q1=coloraux
        if boxactual==2:
            coloraux=Q2
            Q2 = colorchooser.askcolor()[1]
            if(Q2==None):
                Q2=coloraux
        if boxactual==3:
            coloraux=Q3
            Q3 = colorchooser.askcolor()[1]
            if(Q3==None):
                Q3=coloraux
        if boxactual==4:
            coloraux=Q4
            Q4 = colorchooser.askcolor()[1]
            if(Q4==None):
                Q4=coloraux
        if boxactual==5:
            coloraux=Q5
            Q5 = colorchooser.askcolor()[1]
            if(Q5==None):
                Q5=coloraux
        if boxactual==6:
            coloraux=Q6
            Q6 = colorchooser.askcolor()[1]
            if(Q6==None):
                Q6=coloraux
        if boxactual==7:
            coloraux=Q7
            Q7 = colorchooser.askcolor()[1]
            if(Q7==None):
                Q7=coloraux
        if boxactual==8:
            coloraux=Q8
            Q8 = colorchooser.askcolor()[1]
            if(Q8==None):
                Q8=coloraux

    while running:
        aux=margen()#Pone el margen de repelentes al rededor
        button7 = Button('Estado ' + str(boxactual),120,30,(PixelesXlado+ladoExtra,PixelesXlado-(otroExtra*2)),5,gui_font,screen)
        buttons.append(button7)
        #Indica que acciones tomar con base a los botones
        textoBoton=setTexto()
        if(textoBoton=='Iniciar/Pausar'):
            pausar()
            textoBoton=''
        elif(textoBoton=='Reiniciar'):
            clear()
            textoBoton=''
        elif(textoBoton=='Abrir'):
            clear()
            abrir()
            textoBoton=''
        elif(textoBoton=='Guardar'):
            guardar()
            textoBoton=''
        elif(textoBoton=='Color'):
            escogerColor(boxactual)
            textoBoton=''
        elif(textoBoton=='+'):
            if(delay>=0 and delay<=9):
                delay+=1
            textoBoton=''
        elif(textoBoton=='-'):
            if(delay>0 and delay<=10):
                delay-=1
            textoBoton=''
        elif(textoBoton=='0'):
            boxactual=0
            textoBoton=''
        elif(textoBoton=='1'):
            boxactual=1
            textoBoton=''
        elif(textoBoton=='2'):
            boxactual=2
            textoBoton=''
        elif(textoBoton=='3'):
            boxactual=3
            textoBoton=''
        elif(textoBoton=='4'):
            boxactual=4
            textoBoton=''
        elif(textoBoton=='5'):
            boxactual=5
            textoBoton=''
        elif(textoBoton=='6'):
            boxactual=6
            textoBoton=''
        elif(textoBoton=='7'):
            boxactual=7
            textoBoton=''
        elif(textoBoton=='8'):
            boxactual=8
            textoBoton=''
        elif(textoBoton=='?'):
            desplegarHelp()
            textoBoton=''
        elif(textoBoton=='Sig grafica'):
            graficaActual+=1
            graficaActual=graficaActual%2
            textoBoton=''
        textoBoton=''
        
        
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                window.withdraw()
                running = False
                file= open('data.txt','w')
                file.write('')
                file.close()
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
                    window.withdraw() 
                    filename = tkinter.filedialog.askopenfilename()
                    aux=load(filename,celulas)

                if event.key == pygame.K_g:
                    window.withdraw()
                    txt = tkinter.simpledialog.askstring(title="Save",prompt="Ingresa el nombre de tu archivo, se le agregara la extencion y las celulas por lado")
                    save(txt,gameState)
                    
    
            mouseClick = pygame.mouse.get_pressed()
            if sum(mouseClick) > 0:
                posX, posY = pygame.mouse.get_pos()
                celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
                try:
                    aux[celX, celY]=boxactual
                except:
                    print("")
                
        if not pauseExect:
            listgene.append(generacion)
            list4.append(count4)
            list5.append(count5)
            list7.append(count7)
            list8.append(count8)

            file= open('data.txt','a')
            file.write(str(generacion)+','+str(count4)+','+str(count5)+','+str(count7)+','+str(count8)+'\n')
            file.close()

            generacion +=1
            count4 = 0 #Q4
            count5 = 0 #Q5
            count7 = 0 #Q7
            count8 = 0 #Q8
        #Creacion de la instancia para las vecindades
        if vecindad == 'neumann':
            comportamiento = Neumann(nxC,nyC,pauseExect,gameState,mins,aux,regla,val,cont,count4,count5,count7,count8, dimCW,dimCH,screen,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,entro,generacion)
        elif vecindad == 'moore':
            comportamiento = Moore(nxC,nyC,pauseExect,gameState,mins,aux,regla,val,cont,count4,count5,count7,count8, dimCW,dimCH,screen,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,entro,generacion)
            
        
        aux,count4,count5,count7,count8,cont,mins,val= comportamiento.movimiento()
                        
        gameState = np.copy(aux)
        
        time.sleep(delay/100)
        #textos
        texto= "Generacion: "+str(generacion)
        label = myfont.render(texto, 1, (255,255,255))
        screen.blit(label, (17, 15))
        
        textoDelay= "Delay: "+str(delay)
        labelDelay = myfont.render(textoDelay, 1, (255,255,255))
        screen.blit(labelDelay, (math.ceil(screenHeigt[0]*0.55),15))
        
        textoDelay= "  Delay  "
        labelDelay = myfont.render(textoDelay, 1, (255,255,255))
        screen.blit(labelDelay, (math.ceil(screenHeigt[0]*0.85),math.ceil(screenWidth[0]*0.2530)))
        
        #checkbox
        
        #actualizar animacion
        if graficaActual==0:
            ani = animation.FuncAnimation(fig, Graficas(ax,Q4,Q5,Q7,Q8).crecimiento,interval=1) 
        elif graficaActual==1:
            ani = animation.FuncAnimation(fig, Graficas(ax,Q4,Q5,Q7,Q8).crecimientoLog,interval=1)
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (PixelesXlado,0))
        
        buttons_draw(buttons)
        pygame.display.update()

    pygame.quit()
    file= open('data.txt','w')
    file.write('')
    file.close()
    
if __name__ == "__main__":
    Simulador(50,1,'moore','S')
