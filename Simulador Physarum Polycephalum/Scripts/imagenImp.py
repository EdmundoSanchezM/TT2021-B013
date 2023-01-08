from PIL import Image
import numpy as np
#Solamente funciona para el estado 0(Libre) y estado 2(Repelente)
#Si se quiere hacer que funcione para otros estados modificar los rgb
#En el final del archivo esta los codigos rgb
def createImagen(name,org,dest):
    im= Image.new('RGB', (org, org))
    clon = []
    color=(0, 47, 104)
    with open(name) as f:
        lines = f.readlines()
        for line in lines:
            auxi=line.split(',')
            x = int(auxi[0])
            y = int(auxi[1])
            tipo= int(float(auxi[2]))             
            if tipo == 0:
                color = (0, 47, 104)  # Campo libre
            elif tipo == 2: 
                color = (199, 0, 57)  # Repelente
            clon.append(color)
    
    im.putdata(clon)
    im.save('img/img.png')
    img = Image.open('img/img.png')
    new_img = img.resize((dest,dest))
    transposed  = new_img.transpose(Image.ROTATE_90)
    transposed.save('img/nuevoTam.png','png')

def readImagen(dest):
    im = Image.open('img/nuevoTam.png') # Can be many different formats.
    pix = im.load()
    filename =open('img/text.txt', 'w')
    tipo=0
    for x in range(dest-1):
        for y in range(dest-1):
            if(pix[x,y][0]<10 and pix[x,y][1]<57 and pix[x,y][1]>37 and pix[x,y][2]<114 and pix[x,y][2]>94):
                tipo=0
            elif (pix[x,y][0]<209 and pix[x,y][0]>109 and pix[x,y][1]<10 and pix[x,y][2]<67 and pix[x,y][2]>47):  
                tipo=2
            filename.write(str(x)+","+str(y)+","+str(tipo)+"\n")

    filename.close()
    
    clon = np.zeros((dest, dest)) 
    with open("img/text.txt") as f:
        lines = f.readlines()
        for line in lines:
            auxi=line.split(',')
            y = int(auxi[0])
            x = int(auxi[1])
            tipo= int(float(auxi[2]))
            #print(tipo)
            clon[x][y]=tipo
    return clon

def loadPixelArt(archivo,pixelesx,pixelesy):
    im = Image.open(archivo) # Can be many different formats.
    pix = im.load()
    filename =open('img/pixelArt.txt', 'w')
    tipo=0
    for x in range(pixelesx-1):
        for y in range(pixelesy-1):
            if(pix[x,y][0]==255  and pix[x,y][1]==255  and pix[x,y][2]==255):
                tipo=0                
            elif (pix[x,y][0]==196  and pix[x,y][1]==4  and pix[x,y][2]==36):  
                tipo=2
            elif (pix[x,y][0]==0  and pix[x,y][1]==0  and pix[x,y][2]==0):  
                tipo=3
            elif (pix[x,y][0]==69  and pix[x,y][1]==39  and pix[x,y][2]==160):  
                tipo=1
                
            filename.write(str(y)+","+str(x)+","+str(tipo)+"\n")

    filename.close()
    
    clon = np.zeros((pixelesx, pixelesy)) 
    with open("img/pixelArt.txt") as f:
        lines = f.readlines()
        for line in lines:
            auxi=line.split(',')
            y = int(auxi[0])
            x = int(auxi[1])
            tipo= int(float(auxi[2]))
            clon[x][y]=tipo
    return clon
        
    
def saveImagen(name,org,dest):
    createImagen(name,org,dest)
    return readImagen(dest)

            #print(tipo)
            # if tipo == 0:
            #     color = (0, 47, 104)  # Campo libre
            # elif tipo == 1:  
            #     color = (66, 104, 198)  # Nutriente no encontrado
            # elif tipo == 2: 
            #     color = (199, 0, 57)  # Repelente
            # elif tipo == 3: 
            #     color = (0, 0, 0)  # Punto inicial
            # elif tipo == 4: 
            #     color = (236, 236, 10)   # Gel en concentracion
            # elif tipo == 5: 
            #     color = (52, 131, 0)  # Gel con compuesto
            # elif tipo == 6: 
            #     color = (241, 252, 225)  # Nutriente hallado
            # elif tipo == 7: 
            #     color = (90, 96, 81) # Expansion del Physarum
            # elif tipo == 8: 
            #     color = (151, 195, 99)  # Gel sin compuesto