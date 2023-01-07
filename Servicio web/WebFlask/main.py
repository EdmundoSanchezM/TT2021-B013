from flask import Flask
from flask_mail import Mail
from flask import request, render_template, url_for, redirect, session, jsonify
from scripts.correos import *
from scripts.db import *
import bcrypt
import os
import subprocess
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature, BadSignature
import time

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'XXXXXXXXXXXXXXXX'  # Ponerxxx
db_path = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'Proyecto.db')

# configuracion de email
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'josuemendezrendon@yahoo.com.mx'
app.config['MAIL_PASSWORD'] = "XXXXXXXXXXXXX"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

setMovimiento("False")
setPaquete("False")
# serializer para Token
sToken = URLSafeTimedSerializer(app.config['SECRET_KEY'])

nombreLugares = ["Becas", "Capital Humano", "Dirección", "Gestión Tecnica", "Salas de reuniones",
                 "Servicios Educativos", "Subdirección Administrativa", "Subdirección Academica"]

def convertirNombreLugar(nuevoInicio):
    formatLanzador = nuevoInicio
    if(nuevoInicio == "Subdirección Academica"):
        formatLanzador = "SubDireccion"
    elif(nuevoInicio == "Dirección"):
        formatLanzador = "Direccion"
    elif(nuevoInicio == "Servicios Educativos"):
        formatLanzador = "SEducativos"
    elif(nuevoInicio == "Salas de reuniones"):
        formatLanzador = "SalaReunion"
    elif(nuevoInicio == "Subdirección Administrativa"):
        formatLanzador = "SAdministrativa"
    elif(nuevoInicio == "Capital Humano"):
        formatLanzador = "CHumano"
    elif(nuevoInicio == "Gestión Tecnica"):
        formatLanzador = "GTecnica"
    return formatLanzador
# ------------------------------ >   Menu incial  < ------------------------------

"""
    Ruta "/". Pagina de inicio
"""


@app.route('/', methods=['POST', 'GET'])
def inicio():
    session.clear()
    return render_template('Home_Inicio.html')


"""
    Ruta que carga el login del proyecto
"""


@app.route('/login', methods=['POST', 'GET'])
def login():
    session.clear()
    if request.method == 'POST':
        userD = request.get_json()
        email = userD['email']
        psw = userD['contrasenia']
        conexion = conecta_db(db_path)
        persona = valida_login(conexion, email)
        close_db(conexion)
        if(not persona):
            return jsonify({"mensaje": """Usuario no registrado"""
                            }, 409)
        elif(bcrypt.checkpw(psw.encode('utf8'), persona[5])):
            msgTipoUsuario = ""
            if(persona[6] == 1):  # Administrador
                session["idTipoUsr"] = 1
                session["nom"] = persona[1]
                session["email"] = email
                msgTipoUsuario = "Admin"
                return jsonify({"mensaje": msgTipoUsuario
                                }, 200)
            elif(persona[6] == 0):  # No validado
                if(persona[7] == "No"):
                    msgTipoUsuario = "No validado"
                    return jsonify({"mensaje": msgTipoUsuario
                                    }, 200)
                elif(persona[7] == "Si"):  # Usuario normal
                    session["idTipoUsr"] = 0
                    session["nom"] = persona[1]
                    session["email"] = email
                    msgTipoUsuario = "UsrNormal"
                    return jsonify({"mensaje": msgTipoUsuario
                                    }, 200)
        else:
            return jsonify({"mensaje": """Contraseña incorrecta"""
                            }, 403)
    else:
        return render_template('Home_Login.html')


"""
    Ruta que sirve para dar de alta usuarios # La idea es que un usuario Administrado pueda validar a este usuario
    , i.e, el usuario no tendra acceso a la pagina hasta que un usuario que si tenga accesso lo valide.
"""


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    session.clear()
    if request.method == 'POST':
        userD = request.get_json()
        nom = userD['nombre']
        apep = userD['appaterno']
        apem = userD['apmaterno']
        telefono = userD['cel']
        psw = userD['contra'].encode('utf-8')
        salt = bcrypt.gensalt()
        psw_hashed = bcrypt.hashpw(psw, salt)
        email = userD['email']
        conexion = conecta_db(db_path)
        respuesta = alta_usur(conexion, email, nom, apep,
                              apem, telefono, psw_hashed, 0)
        close_db(conexion)
        return jsonify(respuesta)
    elif request.method == 'GET':
        return render_template('Home_Registro.html')
# ---------------------------------------------------------------------------------

# -------------------- >  Opción usuario normal y administrador  < --------------------


@app.route('/envioReciboPaquetes', methods=['GET'])
def envioReciboPaquetes():
    try:
        usr = session["idTipoUsr"]
        if(usr == 0 or usr == 1):  # No Validado o valido
            # Ubicacion del robot
            conexion = conecta_db(db_path)
            desactivar = ""
            posRobot = getPosRobot()
            cpnombreLugares = nombreLugares.copy()
            if(getMovimiento() == "True"):  # Se esta moviendo
                posRobot = "El robot esta siendo ocupado por el usuario con correo: {}, en este momento no se puede enviar paquetes o modificar la ubicación. Regresar o recargar la pagina en unos cuantos minutos".format(
                    getUsrOcupante())
                desactivar = "disabled"
            elif(getPaquete() == "True"):  # Tiene paquete
                posRobot = "El robot tiene un paquete por ser recogido, en este momento no se puede enviar paquetes o modificar la ubicación. Regresar o recargar la pagina en unos cuantos minutos"
                desactivar = "disabled"
            else:
                cpnombreLugares.remove(posRobot)
            respuesta = consultaTipoUsuarios(
                conexion, "Si")  # Obteniendo no validos
            if(usr == 0):
                return render_template('UsrNormal_EnviaRecibePaq.html', correo=session["email"], nombrecito=session["nom"], locacion=posRobot, ubicacionWOposR=cpnombreLugares, desactivar=desactivar, personas=respuesta)
            if(usr == 1):
                return render_template('Admin_EnviaRecibePaq.html', correo=session["email"], nombrecito=session["nom"], locacion=posRobot, ubicacionWOposR=cpnombreLugares, desactivar=desactivar, personas=respuesta)
    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Mover robot de un punto a otro sin enviar paquete
"""


@app.route('/moverRobotNuevoPunto', methods=['POST'])
def moverRobotNuevoPunto():
    try:
        usr = session["idTipoUsr"]
        if(usr == 0 or usr == 1):  # No Validado o valido
            if(getMovimiento() == "True" or getPaquete() == "True"):  # Se esta moviendo
                return jsonify({"nuevaUbicacion": """False""", }, 200)
            setMovimiento("True")
            arrInfo = request.get_json()
            nuevoInicio = arrInfo['nombreNuevaUbic']
            setUsrOcupante(session["email"])
            conexion = conecta_db(db_path)
            resultBitacora = insertaBitacora(
                conexion, 'Uso del robot: nueva ubicación inicial', session["email"], session["email"])
            if(resultBitacora[1] != 200):
                return resultBitacora
            #########Empieza viaje#########
            nombreLugares = ["Becas", "Capital Humano", "Dirección", "Gestión Tecnica", "Salas de reuniones",
                 "Servicios Educativos", "Subdirección Administrativa", "Subdirección Academica"]
            formatLanzador = nuevoInicio
            iniciarViaje = subprocess.Popen(['python3', os.path.join("/home/pi/Desktop/Robot", "lanzador.py")] + [convertirNombreLugar(nuevoInicio),"0"])
            time.sleep(5)
            while True:
                if(getUseRobot() == "1"):
                    break
            ###############################
            setPosRobot(nuevoInicio)
            setMovimiento("False")
            return jsonify({"nuevaUbicacion": ""+nuevoInicio + ""}, 200)
            
    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Mover robot de un punto a otro con paquete
"""


@app.route('/envioPaquete', methods=['POST'])
def envioPaquete():
    try:
        usr = session["idTipoUsr"]
        if(usr == 0 or usr == 1):  # No Validado o valido
            if(getMovimiento() == "True"  or getPaquete() == "True"):  # Se esta moviendo
                return jsonify({"nuevaUbicacion": """False""", }, 200)
            setMovimiento("True")
            arrInfo = request.get_json()
            nuevoInicio = arrInfo['nombreNuevaUbic']
            setUsrOcupante(session["email"])
            setUsrDestino(arrInfo['emailDestinatario'])
            conexion = conecta_db(db_path)
            respuesta, persona = validaRecuperarContra( conexion, arrInfo['emailDestinatario'])
            ##########Abrir caja##########
            abrirCaja = subprocess.Popen(['python3', os.path.join("/home/pi/Desktop/Robot", "abrirCaja.py")])
            time.sleep(5)
            while True:
                if(getUseRobot() == "1"):
                    break
            ##############################
            setPaquete("True")
            time.sleep(30)
            if respuesta:
                asunto = "Paquete en camino"
                correo = crearCorreoAvisoPaq(app.config.get("MAIL_USERNAME"), arrInfo['emailDestinatario'],
                                              asunto, persona[1]+" "+persona[2]+" "+persona[3], session["email"], arrInfo['nombreNuevaUbic'])
                mail.send(correo)
                resultBitacora = insertaBitacora(conexion, 'Uso del robot: envio de paquete', session["email"], arrInfo['emailDestinatario'])
                if(resultBitacora[1] != 200):
                    return resultBitacora
            ##########Cerrar caja##########
            cerrarCaja = subprocess.Popen(['python3', os.path.join("/home/pi/Desktop/Robot", "cerrarCaja.py")])
            time.sleep(5)
            while True:
                if(getUseRobot() == "1"):
                    break
            ##############################
            #########Empieza viaje#########
            nombreLugares = ["Becas", "Capital Humano", "Dirección", "Gestión Tecnica", "Salas de reuniones",
                 "Servicios Educativos", "Subdirección Administrativa", "Subdirección Academica"]
            formatLanzador = nuevoInicio
            iniciarViaje = subprocess.Popen(['python3', os.path.join("/home/pi/Desktop/Robot", "lanzador.py")] + [convertirNombreLugar(nuevoInicio),"0"])
            time.sleep(5)
            while True:
                if(getUseRobot() == "1"):
                    break
            ###############################
            #Fin viaje
            setPosRobot(nuevoInicio)
            setMovimiento("False")
            #Enviando correo para abrir caja
            asunto = "El paquete a llegado a su destino"
            correo = crearCorreoAvisoPaqLlegado(app.config.get("MAIL_USERNAME"), arrInfo['emailDestinatario'],
                                              asunto, persona[1]+" "+persona[2]+" "+persona[3], session["email"], arrInfo['nombreNuevaUbic'])
            mail.send(correo)
            return jsonify({"nuevaUbicacion": ""+nuevoInicio + ""}, 200)
    except Exception as e:
        print(e)
        return redirect(url_for("login"))

"""
    Recibir paquete
"""

@app.route('/recibirPaquete', methods=['POST','GET'])
def recibirPaquete():
    try:
        usr = session["idTipoUsr"]
        if(usr == 0 or usr == 1):  # No Validado o valido
            if request.method == 'POST':
                    ##########Abrir caja##########
                    abrirCaja = subprocess.Popen(['python3', os.path.join("/home/pi/Desktop/Robot", "abrirCaja.py")])
                    time.sleep(5)
                    while True:
                        if(getUseRobot() == "1"):
                            break
                    ##############################
                    respuesta = {"mensaje": "Caja abierta"}, 200
                    return jsonify(respuesta)
            elif request.method == 'GET':
                if(session["email"] == getUsrDestino()):
                    if(usr == 0):
                        return render_template('UsrNormal_RecibirPaquete.html',nombrecito=session["nom"])
                    else:
                        return render_template('Admin_RecibirPaquete.html',nombrecito=session["nom"])
                else:
                    return redirect(url_for("envioReciboPaquetes"))
    except Exception as e:
        print(e)
        return redirect(url_for("login"))

"""
    Confirmar entrega
"""

@app.route('/confirmarEntrega', methods=['POST'])
def confirmarEntrega():
    try:
        usr = session["idTipoUsr"]
        if(usr == 0 or usr == 1):  # No Validado o valido
            if request.method == 'POST':
                    conexion = conecta_db(db_path)
                    respuesta, persona = validaRecuperarContra( conexion, getUsrOcupante())
                    if respuesta:
                        asunto = "El paquete a sido entregado"
                        correo = crearCorreoAvisoPaqEntregado(app.config.get("MAIL_USERNAME"), getUsrOcupante(),
                                                    asunto, persona[1]+" "+persona[2]+" "+persona[3], getUsrDestino())
                        mail.send(correo)
                        resultBitacora = insertaBitacora(conexion, 'Uso del robot: paquete recogido', getUsrOcupante(),  getUsrDestino())
                        if(resultBitacora[1] != 200):
                            return resultBitacora
                    ##########Cerrar caja##########
                    cerrarCaja = subprocess.Popen(['python3', os.path.join("/home/pi/Desktop/Robot", "cerrarCaja.py")])
                    time.sleep(5)
                    while True:
                        if(getUseRobot() == "1"):
                            break
                    ##############################
                    setUsrDestino("uwu")
                    setUsrOcupante("uwu")
                    setPaquete("False")
                    respuesta = {"mensaje": "Paquete entregado"}, 200
                    return jsonify(respuesta)
    except Exception as e:
        print(e)
        return redirect(url_for("login"))

# ---------------------------------------------------------------------------------

# -------------------- >  Menu usuario valido  < --------------------


"""
    Ver la camara que esta integrada en el robot
"""


@app.route('/verCamara', methods=['POST', 'GET'])
def verCamara():
    try:
        usr = session["idTipoUsr"]
        if(usr == 0 or usr == 1):  # No Validado o valido
            if(usr == 0):  # Validar si esta involucrado
                return render_template('UsrNormal_verCamara.html', nombrecito=session["nom"])
            if(usr == 1):
                return render_template('Admin_verCamara.html', nombrecito=session["nom"])
    except Exception as e:
        return redirect(url_for("login"))


"""
    Ver cuentas no validadas para poder validarlas o eliminarlas
"""


@app.route('/verCuentasNoValidadas', methods=['POST', 'GET'])
def verCuentasNoValidadas():
    try:
        usr = session["idTipoUsr"]
        if(usr != 1):
            return redirect(url_for("login"))
        else:
            conexion = conecta_db(db_path)
            respuesta = consultaTipoUsuarios(
                conexion, "No")  # Obteniendo no validos
        return render_template('Admin_VerNoValido.html', filas=respuesta, nombrecito=session["nom"])

    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Usuarios validos pueden validar cuentas no validas
"""


@app.route('/validarCuenta', methods=['POST'])
def validarCuenta():
    try:
        usr = session["idTipoUsr"]
        if(usr != 1):
            return redirect(url_for("login"))
        else:
            userD = request.get_json()
            usr = userD['email']
            conexion = conecta_db(db_path)
            resultBitacora = insertaBitacora(
                conexion, 'Validación', session["email"], usr)
            if(resultBitacora[1] == 200):
                respuesta = validarCuentaDB(conexion, usr)
            else:
                return resultBitacora
            return jsonify(respuesta)
    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Usuarios validos pueden eliminar cuentas no validadas
"""


@app.route('/borrarCuentaNoValida', methods=['POST', 'GET'])
def borrarCuentaNoValida():
    try:
        usr = session["idTipoUsr"]
        if(usr != 1):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                userD = request.get_json()
                usr = userD['email']
                conexion = conecta_db(db_path)
                resultBitacora = insertaBitacora(
                    conexion, 'Cuenta no valida eliminada', session["email"], usr)
                if(resultBitacora[1] == 200):
                    respuesta = eliminaCuentaNovalida(conexion, usr)
                else:
                    return resultBitacora
                close_db(conexion)
                return jsonify(respuesta)

    except Exception as e:
        return redirect(url_for("login"))


"""
    Ver datos de la cuenta validado, los datos modificables: telefono y contraseñas
"""


@app.route('/verDatosCuenta', methods=['POST', 'GET'])
def verDatosCuenta():
    try:
        usr = session["idTipoUsr"]
        if(usr != 1 and usr != 0):
            return redirect(url_for("login"))
        else:
            usrE = session["email"]
            conexion = conecta_db(db_path)
            respuesta = consultaUsuario(conexion, usrE)
            if(usr == 1):
                return render_template('Admin_modificar.html', filas=respuesta, nombrecito=session["nom"])
            elif(usr == 0):
                return render_template('UsrNormal_modificar.html', filas=respuesta, nombrecito=session["nom"])
    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Modificar datos
"""


@app.route('/modificarCuenta', methods=['POST', 'GET'])
def modificarCuenta():
    try:
        usr = session["idTipoUsr"]
        if(usr != 1 and usr != 0):
            return redirect(url_for("login"))
        else:
            if request.method == 'POST':
                userD = request.get_json()
                conexion = conecta_db(db_path)
                psw = userD['psw']
                cel = userD['cel']
                ema = userD['ema']
                respuesta = ""
                if(len(psw) > 0):
                    salt = bcrypt.gensalt()
                    new_psw_hashed = bcrypt.hashpw(psw.encode('utf-8'), salt)
                    respuesta = modificaCuenta(
                        conexion, new_psw_hashed, cel, ema)
                else:
                    respuesta = modificaCuenta(conexion, psw, cel, ema)
                if(respuesta[1] == 200):
                    resultBitacora = insertaBitacora(
                        conexion, 'Cuenta modificada', ema, ema)
                    if(resultBitacora[1] == 200):
                        return jsonify(respuesta)
                    else:
                        return resultBitacora
                close_db(conexion)
                return jsonify(respuesta)
    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Eliminar cuenta
"""


@app.route('/deleteAccount', methods=['POST', 'GET'])
def deleteAccount():
    try:
        usr = session["idTipoUsr"]
        if(usr != 1 and usr != 0):
            return redirect(url_for("login"))
        else:
            respuesta = ""
            if request.method == 'GET':
                if(usr == 0):
                    return render_template('UsrNormal_EliminarCuenta.html', nombrecito=session["nom"], correo=session["email"])
                elif(usr == 1):
                    return render_template('Admin_EliminarCuenta.html', nombrecito=session["nom"], correo=session["email"])
            elif request.method == 'POST':
                usr = session["email"]
                conexion = conecta_db(db_path)
                resultBitacora = insertaBitacora(
                    conexion, 'Cuenta validada eliminada', usr, usr)
                if(resultBitacora[1] == 200):
                    respuesta = eliminarUsuario(conexion, usr)
                else:
                    return resultBitacora
                return jsonify(respuesta)
    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Bitacora
"""


@app.route('/verBitacora', methods=['POST', 'GET'])
def verBitacora():
    try:
        usr = session["idTipoUsr"]
        if(usr == 0):
            conexion = conecta_db(db_path)
            bitacoras = consultaBitacoraUsrNormal(conexion, session["email"])
            return render_template('UsrNormal_Bitacora.html', nombrecito=session["nom"], tablita=bitacoras)
        elif(usr == 1):
            conexion = conecta_db(db_path)
            bitacoras = consultaBitacora(conexion)
            return render_template('Admin_BitacoraValidacion.html', nombrecito=session["nom"], tablita=bitacoras)
        else:
            return redirect(url_for("login"))
    except Exception as e:
        print(e)
        return redirect(url_for("login"))


"""
    Recuperar contraseña
"""


@app.route('/recuparContra', methods=['POST', 'GET'])
def recuparContra():
    session.clear()
    if request.method == 'POST':
        userD = request.get_json()
        email = userD['email']
        conexion = conecta_db(db_path)
        respuesta, persona = validaRecuperarContra(conexion, email)
        if respuesta:
            asunto = "Recuperar contraseña"
            # creando token
            token = sToken.dumps(email, salt='password-recovery')
            tokenlink = "http://148.204.56.179/recuparContra/"+token
            correo = crearCorreoRecContra(app.config.get("MAIL_USERNAME"),
                                          email, asunto, persona[1]+" "+persona[2]+" "+persona[3], tokenlink)
            mail.send(correo)
            print("correo enviado")
        close_db(conexion)
        return jsonify({"mensaje": """Correo mandado"""
                        }, 200)
    elif request.method == 'GET':
        return render_template('Home_RecuperarContraForm.html')


@app.route('/recuparContra/<token>', methods=['GET'])
def recuparContraToken(token):
    session.clear()
    try:
        email = sToken.loads(token, salt='password-recovery', max_age=300)
        return render_template('Home_RecuperarContraTokenR.html', data=[
            {
                'usrToken': token,
            }])
    except SignatureExpired:
        return render_template('Home_RecuperarContraTokenExp.html')
    except BadTimeSignature:
        return render_template('Home_RecuperarContraTokenBadToken.html')
    except BadSignature:
        return render_template('Home_RecuperarContraTokenBadToken.html')


@app.route('/modificarContra', methods=['POST'])
def modificaContra():
    session.clear()
    if request.method == 'POST':
        userD = request.get_json()
        conexion = conecta_db(db_path)
        psw = userD['pass']
        ema = sToken.loads(
            userD['token'], salt='password-recovery', max_age=300)
        respuesta = ""
        resultBitacora = insertaBitacora(
            conexion, 'Cambio de contraseña', ema, ema)
        if(resultBitacora[1] == 200):
            if(len(psw) > 0):
                salt = bcrypt.gensalt()
                new_psw_hashed = bcrypt.hashpw(psw.encode('utf-8'), salt)
                respuesta = modificarContra(
                    conexion, new_psw_hashed, ema)
                close_db(conexion)
        else:
            return resultBitacora
        return jsonify(respuesta)


@app.errorhandler(404)
def error404(error):
    return render_template("404.html")


if __name__ == '__main__':
    conexion = conecta_db(db_path)
    crea_tbs(conexion)
    close_db(conexion)
    app.run(debug=True)
