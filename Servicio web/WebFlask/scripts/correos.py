from flask_mail import Message
from flask import render_template
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def crearCorreoRecContra(remitente, destinatario, asunto,nombreUser,tokenlink):
    mensaje = Message(asunto, sender=remitente, recipients=[destinatario])
    mensaje.body = "testing"
    mensaje.html = render_template('Correo_RecuperarContra.html', data=[
        {
            'nombreUser': nombreUser,
            'verificationTokenLink': tokenlink
        }]
    )
    return mensaje

def crearCorreoAvisoPaq(remitente, destinatario, asunto, nombreUser, correoEnvia,ubicacionLlegada):
    mensaje = Message(asunto, sender=remitente, recipients=[destinatario])
    mensaje.body = "testing"
    mensaje.html = render_template('Correo_AvisoPaqEnvio.html', data=[
        {
            'nombreUser': nombreUser,
            'correoEnvia': correoEnvia,
            'ubicacionLlegada': ubicacionLlegada,
        }]
    )
    return mensaje

def crearCorreoAvisoPaqLlegado(remitente, destinatario, asunto, nombreUser, correoEnvia,ubicacionLlegada):
    mensaje = Message(asunto, sender=remitente, recipients=[destinatario])
    mensaje.body = "testing"
    mensaje.html = render_template('Correo_AvisoPaqLlegado.html', data=[
        {
            'nombreUser': nombreUser,
            'correoEnvia': correoEnvia,
            'ubicacionLlegada': ubicacionLlegada,
        }]
    )
    return mensaje

def crearCorreoAvisoPaqEntregado(remitente, destinatario, asunto, nombreUser, correoRecibe):
    mensaje = Message(asunto, sender=remitente, recipients=[destinatario])
    mensaje.body = "testing"
    mensaje.html = render_template('Correo_AvisoPaqEntregado.html', data=[
        {
            'nombreUser': nombreUser,
            'correoRecibe': correoRecibe,
        }]
    )
    return mensaje

def setPosRobot(posicion):
	f = open(os.path.join(__location__, 'posRobot.txt'), "w",encoding='utf-8')
	f.write(str(posicion))
	f.close()

def getPosRobot():
	with open(os.path.join(__location__, "posRobot.txt"),encoding='utf-8') as f:
		pos = f.read()
		return str(pos)

def getUseRobot():
	with open(os.path.join("/home/edmundojsm/Escritorio/tt/Robot", "useRobot.txt"),encoding='utf-8') as f:
		pos = f.read()
		return str(pos)

def setUsrDestino(usr):
	f = open(os.path.join(__location__, 'usrDestino.txt'), "w",encoding='utf-8')
	f.write(str(usr))
	f.close()

def getUsrDestino():
	with open(os.path.join(__location__, "usrDestino.txt"),encoding='utf-8') as f:
		usr = f.read()
		return str(usr)

def setUsrOcupante(usr):
	f = open(os.path.join(__location__, 'usrOcupante.txt'), "w",encoding='utf-8')
	f.write(str(usr))
	f.close()

def getUsrOcupante():
	with open(os.path.join(__location__, "usrOcupante.txt"),encoding='utf-8') as f:
		usr = f.read()
		return str(usr)

def setPaquete(usr):
	f = open(os.path.join(__location__, 'paquete.txt'), "w",encoding='utf-8')
	f.write(str(usr))
	f.close()

def getPaquete():
	with open(os.path.join(__location__, "paquete.txt"),encoding='utf-8') as f:
		usr = f.read()
		return str(usr)

def setMovimiento(usr):
	f = open(os.path.join(__location__, 'movimiento.txt'), "w",encoding='utf-8')
	f.write(str(usr))
	f.close()

def getMovimiento():
	with open(os.path.join(__location__, "movimiento.txt"),encoding='utf-8') as f:
		usr = f.read()
		return str(usr)

def testos():
    print(os.environ["ENMOVIMIENTO"])
