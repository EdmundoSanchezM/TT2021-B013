from tkinter import messagebox
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from tkinter import *
from PIL import ImageTk, Image
import os

def graficar():
    fig,ax = plt.subplots()
    graph_data = open('entropia/EntroReal.txt','r').read()
    lines = graph_data.split('\n')
    listEntro=[]
    listgene=[]
    for line in lines:
        if len(line) > 1:
            num0, num1= line.split(',')
            listgene.append(int(num0))
            listEntro.append(float(num1))

    ax.plot(listgene, listEntro,'#ECEC0A')
    ax.set_xlabel('Generacion') 
    ax.set_ylabel('Valor') 
    ax.set_title("Entropia")
    plt.savefig("mygraph.png")
    root = Toplevel()
    img = ImageTk.PhotoImage(Image.open("mygraph.png"))
    panel = Label(root, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    root.mainloop()
    
def entropiaGrafica(tipo,nxC,nyC):
        print("Leyendo vecindades")
        file = open('entropia/EntroReal.txt','w')
        file.write('')
        file.close()
        file = open('entropia/EntroFrecuencia.txt','w')
        file.write('')
        file.close()
        graph_data = open('entropia/EntroInfo.txt','r').read()
        lines = graph_data.split('\n')
        listData=[]
        contador=1
        listgene=[]
        listgene.append(contador)
        contador=0
        for line in lines:
            if line == '---------':
                print('Calculando generacion '+str(contador))
                getFrecuencia(listData,tipo)
                entropiaReal(contador,nxC,nyC)
                contador+=1
                listgene.append(contador)
                listData=[]
                file = open('entropia/EntroFrecuencia.txt','w')
                file.write('')
                file.close()
            else:
                if(line!=''):
                    listData.append(float(line))
        graficar()
        
            
def entropiaReal(generacion,nxC,nyC):
    file = open('entropia/EntroReal.txt','a')
    aux=0
    with open('entropia/EntroFrecuencia.txt') as f:
        for line in f:
            num=int(line)
            if num!=0:
                aux+=(num/(nxC*nyC))*math.log10(num/(nxC*nyC))
    aux=aux*-1
    file.write(str(generacion)+","+str(aux)+'\n')
    file.close()
    
def getFrecuencia(lista,tipo):
    file = open('entropia/EntroFrecuencia.txt','a')
    if(tipo=='moore'):
        number=9
    elif(tipo=='neumann'):
        number=5
    for i in range(2**number):
        aux=0
        for j in range(len(lista)):
            if i==lista[j]:
                lista[j]
                aux+=1
        file.write(str(aux)+'\n')
    file.close()