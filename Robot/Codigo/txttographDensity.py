from matplotlib import pyplot as plt
import os
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
    
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
fig,ax = plt.subplots()
graph_data = open(os.path.join(__location__, 'data.txt'),'r').read()
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
ax.plot(listgene, list4,Q4)
ax.plot(listgene, list5,Q5)
ax.plot(listgene, list7,Q7)
ax.plot(listgene, list8,Q8)
ax.set_xlabel('Generación') 
ax.set_ylabel('Población') 
ax.set_title("Crecimiento estados")
plt.show()