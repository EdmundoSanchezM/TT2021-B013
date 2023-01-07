import sqlite3
import requests


def conecta_db(name):
    return sqlite3.connect(name)


def close_db(conexion):
    conexion.close()


def crea_tbs(conexion):
    cursor_tb = conexion.cursor()
    cursor_tb.execute(
        """
				create table if not exists tipoUsr(
					idTipoUsr integer not null primary key,
					descrip text not null
				)
			"""
    )
    cursor_tb.execute(
        """
				create table if not exists usuarios(
					email text not null primary key,
					nombre text not null,
					apaterno text not null,
					amaterno text not null,
					telefono integer not null,
					password text not null,
					idTipoUsr integer not null,
                    Validado text not null,
					foreign key(idTipoUsr) references tipoUsr(idTipoUsr)
				)
			"""
    )
    cursor_tb.execute(
        """
				create table if not exists report_sistema(
					idRepor integer not null primary key,
					Actividad text not null,
					email_responsableA text not null,
                    email_afectadoA text not null,
					fecha timestamp default (datetime('now','localtime'))
				)
			"""
    )
    # Ingresamos los tipos de usuario que tendra el sistema
    IngresaTipoUsuario(conexion, "0", [0, 'Usuario Basico'])
    IngresaTipoUsuario(conexion, "1", [1, 'Administrador'])


def IngresaTipoUsuario(conexion, valor, list_data):
    cursor_tb = conexion.cursor()
    respuesta = cursor_tb.execute(
        "select * from tipoUsr where idTipoUsr = {}".format(valor))
    existencia = respuesta.fetchone()
    if existencia == None:
        sentencia = "INSERT INTO tipoUsr VALUES (?,?)"
        cursor_tb.execute(sentencia, list_data)
        conexion.commit()


def valida_email(conexion, email):
    cursor_tb = conexion.cursor()
    sentencia = "select * from usuarios where email=?"
    respuesta = cursor_tb.execute(sentencia, (email,))
    existencia = respuesta.fetchone()
    if existencia != None:
        return 1
    else:
        return 0


def alta_usur(conexion, email, nom, apep, apem, telefono, psw, tipo):
    msj = ""
    correo = valida_email(conexion, email)
    if(correo == 0):
        cursor_tb = conexion.cursor()
        sentencia = "insert into usuarios values(?,?,?,?,?,?,?,?)"
        e_setencia = cursor_tb.execute(
            sentencia, (email, nom, apep, apem, telefono, psw, tipo, "No"))
        conexion.commit()
        if e_setencia.rowcount < 1:
            msj = {"mensaje": "Ocurrio un error al intentar crear la cuenta"}, 500
        else:
            msj = {"mensaje": """Cuenta creada existosamente. 
			Favor de contactar a un usuario con acceso para validar su cuenta"""
                   }, 200
    elif(correo == 1):
        msj = {"mensaje": "Ya existe un usuario con ese correo"}, 409
    return msj


def valida_login(conexion, correo):
    cursor_tb = conexion.cursor()
    sentencia = "select * from usuarios where email=?"
    e_setencia = cursor_tb.execute(sentencia, (correo,))
    for fila in e_setencia:
        return fila
    return False


def validarCuentaDB(conexion, email):
    msj = ""
    cursor_tb = conexion.cursor()
    sentencia = "select * from usuarios where email=?"
    respuesta = cursor_tb.execute(sentencia, (email,))
    existencia = respuesta.fetchone()
    if existencia != None:
        sentencia = 'update usuarios set Validado="Si" where email=?'
        e_setencia = cursor_tb.execute(sentencia, (email,))
        conexion.commit()
        if e_setencia.rowcount < 1:
            msj = {"mensaje": "Ocurrio un error al intentar validar la cuenta"}, 500
        else:
            msj = {"mensaje": "Cuenta validada exitosamente"}, 200
    else:
        msj = {"mensaje": "No se encontro el usuario a validar su cuenta"}, 409
    return msj


def consultaTipoUsuarios(conexion, tipo):
    cursor_tb = conexion.cursor()
    if(tipo == "No"):
        sentencia = 'select * from usuarios where Validado="No"'
    elif(tipo == "Si"):
        sentencia = 'select * from usuarios where Validado="Si"'
    resultado = cursor_tb.execute(sentencia)
    return resultado


def eliminaCuentaNovalida(conexion, usr):
    msj = ""
    cursor_tb = conexion.cursor()
    sentencia = "select * from usuarios where email=?"
    respuesta = cursor_tb.execute(sentencia, (usr,))
    existencia = respuesta.fetchone()
    if existencia != None:
        sentencia = "delete from usuarios where email=?"
        e_setencia = cursor_tb.execute(sentencia, (usr,))
        conexion.commit()
        if e_setencia.rowcount < 1:
            msj = {"mensaje": "Ocurrio un error al intentar validar la cuenta"}, 500
        else:
            msj = {"mensaje": "Cuenta eliminada exitosamente"}, 200
    else:
        msj = {"mensaje": "No se encontro el usuario para eliminar su cuenta"}, 409
    return msj


def consultaUsuario(conexion, usr):
    cursor_tb = conexion.cursor()
    sentencia = "select * from usuarios where email=?"
    return cursor_tb.execute(sentencia, (usr,))


def modificaCuenta(conexion, psw, cel, ema):
    msj = ""
    cursor_tb = conexion.cursor()
    sentencia = "select * from usuarios where email=?"
    respuesta = cursor_tb.execute(sentencia, (ema,))
    existencia = respuesta.fetchone()
    if existencia != None:
        if(len(psw) != 0):
            sentencia = "update usuarios set telefono=?, password = ? where email=?"
            e_setencia = cursor_tb.execute(sentencia, (cel, psw, ema))
            conexion.commit()
            if e_setencia.rowcount < 1:
                msj = {
                    "mensaje": "Ocurrio un error al intentar validar la cuenta"}, 500
            else:
                msj = {
                    "mensaje": "Cuenta con correo: {} modificada exitosamente".format(ema)}, 200
        else:
            sentencia = "update usuarios set telefono=? where email=?"
            e_setencia = cursor_tb.execute(sentencia, (cel, ema))
            conexion.commit()
            if e_setencia.rowcount < 1:
                msj = {
                    "mensaje": "Ocurrio un error al intentar validar la cuenta"}, 500
            else:
                msj = {
                    "mensaje": "Cuenta con correo: {} modificada exitosamente".format(ema)}, 200
    else:
        msj = {"mensaje": "No se encontro el usuario para eliminar su cuenta"}, 409
    return msj


def eliminarUsuario(conexion, usr):
    msj = ""
    cursor_tb = conexion.cursor()
    sentencia = "select * from usuarios where email=?"
    respuesta = cursor_tb.execute(sentencia, (usr,))
    existencia = respuesta.fetchone()
    if existencia != None:
        sentencia = "delete from usuarios where email=?"
        e_setencia = cursor_tb.execute(sentencia, (usr,))
        conexion.commit()
        if e_setencia.rowcount < 1:
            msj = {"mensaje": "Ocurrio un error al intentar validar la cuenta"}, 500
        else:
            msj = {
                "mensaje": "Cuenta con correo: {} eliminada exitosamente".format(usr)}, 200
    else:
        msj = {"mensaje": "No se encontro el usuario para eliminar su cuenta"}, 409
    return msj


def insertaBitacora(conexion, Actividad, responsable, afectado):
    msj = ""
    cursor_tb = conexion.cursor()
    respuesta = cursor_tb.execute("select max(idRepor) from report_sistema")
    idReg = respuesta.fetchone()[0]
    if(idReg == None):
        idRegistro = 1
    else:
        idRegistro = int(idReg)
        idRegistro = idRegistro+1
    sentencia = "insert into report_sistema(idRepor,Actividad,email_responsableA,email_afectadoA) values(?,?,?,?)"
    e_setencia = cursor_tb.execute(
        sentencia, (idRegistro, Actividad, responsable, afectado))
    conexion.commit()
    if e_setencia.rowcount < 1:
        msj = {"mensaje": "Error al insertar en bitacora"}, 500
    else:
        msj = {"mensaje": "Movimiento guardo en la bitacora"}, 200
    return msj


def consultaBitacora(conexion):
    cursor_tb = conexion.cursor()
    respuesta = cursor_tb.execute(
        "select * from report_sistema order by idRepor")
    return respuesta


def consultaBitacoraUsrNormal(conexion, correo):
    cursor_tb = conexion.cursor()
    sentencia = "select * from report_sistema where (email_responsableA=? or email_afectadoA=? ) order by idRepor"
    respuesta = cursor_tb.execute(sentencia, (correo, correo,))
    return respuesta


def validaRecuperarContra(conexion, email):
    correo = valida_email(conexion, email)
    if(correo == 1):  # mandar correo
        return True, valida_login(conexion, email)
    return False, 0


def modificarContra(conexion, psw, ema):
    msj = ""
    cursor_tb = conexion.cursor()
    sentencia = "select * from usuarios where email=?"
    respuesta = cursor_tb.execute(sentencia, (ema,))
    existencia = respuesta.fetchone()
    if existencia != None:
        sentencia = "update usuarios set password = ? where email=?"
        e_setencia = cursor_tb.execute(sentencia, ( psw, ema))
        conexion.commit()
        if e_setencia.rowcount < 1:
            msj = {
                "mensaje": "Ocurrio un error al intentar validar la cuenta"}, 500
        else:
            msj = {
                "mensaje": "Contraseña modificada correctamente"}, 200
    else:
        msj = {"mensaje": "No se encontro el usuario para modificar la cuenta"}, 409
    return msj

def obtenerUsuariosValidos(conexion):
    cursor_tb = conexion.cursor()
    sentencia = "select * from usuarios where = ?"
    respuesta = cursor_tb.execute(sentencia, (correo, correo,))
    return respuesta