
from pickle import TRUE
from simulador import Simulador
from Entropia import entropiaGrafica
import tkinter 
from tkinter.ttk import Combobox
from tkinter import Tk, Frame, Label,messagebox
from PIL import ImageTk, Image
import threading
from tkinter import *

def start():
    #------------------------------CREAR VENTANA---------------------------------
    root = tkinter.Tk()
    root.wm_title("Autómata del Physarum Polycephalum")
    framet = tkinter.Frame(root)
    frameVecindad = tkinter.Frame(root)
    frameMainInformacion = tkinter.Frame(root)
    frameStart = tkinter.Frame(root)
    frameEnd = tkinter.Frame(root)
    #------------------------------FUNCIONES---------------------------------
    global arregloInicial
    tamEspacio = tkinter.StringVar()
    arregloInicial = []
    
    def seleccion(event):
        img_png = tkinter.PhotoImage(file = 'img/'+str(combo.get())+'.png')
        label_img = tkinter.Label(frameVecindad, image = img_png)
        label_img.grid(row = 2, column = 0)
        tkinter.mainloop()
        

        
    def mensaje():
        mensaje="""
1) Comportamiento normal
2) Separación de una célula en los repelentes
        """
        tkinter.messagebox.showinfo(message=mensaje, title="Reglas")
        
    def mensajeEntro(): 
        mensaje="""La gráfica de la entropía puede tardar, no cerrar el programa"""
        tkinter.messagebox.showinfo(message=mensaje, title="Reglas")
        
    def infoNueva():
        novi = Toplevel()
        canvas = Canvas(novi, width = 870, height = 600)
        canvas.pack(fill="both", expand=True)
        gif1 = PhotoImage(file = 'img/info1.png')
                                    #image not visual
        canvas.create_image(0, 0, image = gif1, anchor = NW)
        #assigned the gif1 to the canvas object
        canvas.gif1 = gif1

    def iniciar():
        global arregloInicial
        
        entro=''
        celulas=0
        try:
            celulas=int(entradaEspacio.get())
            regla=int(combo2.get()) 
            entro=combo3.get()
        except:
            tkinter.messagebox.showinfo(message="Ingrese correctamente los datos", title="Validación")
            return
        
        if entro=='Si':
            entro=True
        elif entro=='No':
            entro=False
        pasa=0
        
        if entro!='':
            if celulas >1:
                if(regla>0 and regla <3):
                    pasa=1
                    if combo.get()=="Neumann":
                        Simulador(celulas,regla,'neumann',entro)
                    elif combo.get()=="Moore":
                        Simulador(celulas,regla,'moore',entro)
                    else:
                        tkinter.messagebox.showinfo(message="Elija una vecindad", title="Validación")
                else:
                    tkinter.messagebox.showinfo(message="No existe esa regla", title="Validación")
            else:
                    tkinter.messagebox.showinfo(message="No se puede trabajar con esa cantidad de células", title="Validación")
        else:
            tkinter.messagebox.showinfo(message="Seleccionar si desea entropía o no", title="Validación")
        
        if pasa and entro:
            print(entro)
            if combo.get()=="Neumann":
                entropiaGrafica('neumann',celulas,celulas)
            elif combo.get()=="Moore":
                entropiaGrafica('moore',celulas,celulas)
        
    #------------------------------CREAR INTERFAZ---------------------------------

    titulo = tkinter.Label(framet, text="Autómata del Physarum Polycephalum",font=("times new roman", 24))
    titulo.pack(side="top")
    
     #------------------------------VECINDAD---------------------------------
    tittleCondicionUsuario = tkinter.Label(frameVecindad, text = "Vecindad" ,font=("times new roman", 18))
    tittleCondicionUsuario.grid(row = 0, column = 0,columnspan=2)
    
    combo = tkinter.ttk.Combobox(frameVecindad,state="readonly",values=["Moore", "Neumann"])
    combo.bind("<<ComboboxSelected>>", seleccion)
    combo.grid(row = 1, column = 0)
    


#------------------------------CONDICION INICIAL USUARIO---------------------------------
    tittleCondicionUsuario = tkinter.Label(frameMainInformacion, text = "Condiciones iniciales" ,font=("times new roman", 18))
    tittleCondicionUsuario.grid(row = 0, column = 0,columnspan=2)

    tamanioEspacio = tkinter.Label(frameMainInformacion, text = "Número de celdas por lado: " , font=("times new roman", 14))
    tamanioEspacio.grid(row=1, column=0)
    entradaEspacio = tkinter.Entry(frameMainInformacion,font=("times new roman", 14), textvariable = tamEspacio)
    entradaEspacio.grid(row=1, column=1)

    tamanioRegla = tkinter.Label(frameMainInformacion, text = "Regla: " , font=("times new roman", 14))
    tamanioRegla.grid(row=2, column=0)
    combo2 = tkinter.ttk.Combobox(frameMainInformacion,state="readonly",values=["1", "2"])
    combo2.bind("<<ComboboxSelected>>")
    combo2.grid(row = 2, column = 1)
    buttonHelp = tkinter.Button(frameMainInformacion, text = "Reglas", command=mensaje ,font=("times new roman", 14))
    buttonHelp.grid(row=2, column=2)
    
    pregunta = tkinter.Label(frameMainInformacion, text = "Mostrar entropia?" , font=("times new roman", 14))
    pregunta.grid(row=3, column=0)
    
    
    combo3 = tkinter.ttk.Combobox(frameMainInformacion,state="readonly",values=["Si", "No"])
    combo3.bind("<<ComboboxSelected>>")
    combo3.grid(row = 3, column = 1)
    buttonEntro = tkinter.Button(frameMainInformacion, text = "Info", command=mensajeEntro ,font=("times new roman", 14))
    buttonEntro.grid(row=3, column=2)


    #------------------------------BOTON MAESTRO---------------------------------

    buttonStart = tkinter.Button(frameStart, text = "Start", command=iniciar ,font=("times new roman", 14))
    buttonStart.grid(row=0, column=0)
    
    buttonUs = tkinter.Button(frameEnd, text = "Sobre nosotros", command=infoNueva ,font=("times new roman", 14))
    buttonUs.grid(row=0, column=0)
    

    framet.grid(row=0,column=0,columnspan=2)
    frameVecindad.grid(row=1,column=0)
    frameMainInformacion.grid(row=2,column=0)
    frameStart.grid(row=3,column=0)
    frameEnd.grid(row=4,column=1)

    tkinter.mainloop()
    

if __name__ == '__main__':
    start()
