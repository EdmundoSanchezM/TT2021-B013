from distutils.log import warn
import math
import numpy as np
import warnings
warnings.filterwarnings("ignore")
class Graficas():
    def __init__(self,ax,Q4,Q5,Q7,Q8):
        self.ax = ax
        self.Q4 = Q4
        self.Q5 = Q5
        self.Q7 = Q7
        self.Q8 = Q8
        
    def crecimientoLog(self,i):
        graph_data = open('data.txt','r').read()
        lines = graph_data.split('\n')
        listgene = []
        list4 = []
        list5 = []
        list7 = []
        list8 = []

        for line in lines:
            if len(line) > 1:
                num0, num1, num2, num3, num4 = line.split(',')
                listgene.append(int(num0))
                
                try:
                    list4.append(np.log2(int(num1)))  
                    list5.append(np.log2(int(num2)))  
                    list7.append(np.log2(int(num3)))  
                    list8.append(np.log2(int(num4)))
                except:
                    print()
                
                
        self.ax.clear()
        self.ax.plot(listgene, list4,self.Q4)
        self.ax.plot(listgene, list5,self.Q5)
        self.ax.plot(listgene, list7,self.Q7)
        self.ax.plot(listgene, list8,self.Q8)
        self.ax.set_xlabel('Generación') 
        self.ax.set_ylabel('Población') 
        self.ax.set_title("Crecimiento estados log2")
        
    def crecimiento(self,i):
        graph_data = open('data.txt','r').read()
        lines = graph_data.split('\n')
        listgene = []
        list4 = []
        list5 = []
        list7 = []
        list8 = []

        for line in lines:
            if len(line) > 1:
                num0, num1, num2, num3, num4 = line.split(',')
                listgene.append(int(num0))
                list4.append(int(num1))  
                list5.append(int(num2))  
                list7.append(int(num3))  
                list8.append(int(num4))

        self.ax.clear()
        self.ax.plot(listgene, list4,self.Q4)
        self.ax.plot(listgene, list5,self.Q5)
        self.ax.plot(listgene, list7,self.Q7)
        self.ax.plot(listgene, list8,self.Q8)
        self.ax.set_xlabel('Generación') 
        self.ax.set_ylabel('Población') 
        self.ax.set_title("Crecimiento estados")

    