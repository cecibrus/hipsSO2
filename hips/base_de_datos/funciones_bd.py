import sys
sys.path.insert(0, '/root/hips')
from definiciones import BD_CONEXION
sys.path.insert(0, '/root/hips/base_de_datos')
from creacion_bd import hashes_i
import psycopg2
from psycopg2 import extras
from psycopg2 import sql



# - - - - -  usuario_registro  - - - - - -

def add_usuario_registro_bd(lista_usuario):
    # Agregar informacion de nuevo usuario
    nombre_usuario = lista_usuario[0]
    ip_permitida = lista_usuario[1]
    dias_permitidos = lista_usuario[2]
    rango_horario_permitido = lista_usuario[3]
    if len(nombre_usuario)>0 and len(ip_permitida)>0 and len(dias_permitidos)>0 and len(rango_horario_permitido)>0 :
        tupla = (str(nombre_usuario),str(ip_permitida),str(dias_permitidos),str(rango_horario_permitido))
        insert_data='INSERT INTO usuario_registro(nombre_usuario, ip_permitida, dias_permitidos, rango_horario_permitido) VALUES({},{},{},{}) returning nombre_usuario;'
        dbConnection = psycopg2.connect(BD_CONEXION)
        cursor = dbConnection.cursor()
        cursor.execute(sql.SQL(insert_data.format(tupla[0], tupla[1], tupla[2], tupla[3])))
        dbConnection.commit()
        dbConnection.close()
    else:
        print("Error. No se pudo agregar")

def obtener_lista_usuario_registro_bd():                                   
    # Obtener lista usuario_informacion
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cursor.execute("SELECT * FROM usuario_registro;")
    lista_usuario_bd = cursor.fetchall()
    psycopg2.connect(BD_CONEXION).close()
    return lista_usuario_bd
    
def reset_usuario_registro_bd():
    # Resetear usuario_informacion
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    dbConnection = psycopg2.connect(BD_CONEXION)
    dbConnection.execute("DELETE FROM usuario_registro")
    dbConnection.commit()
    dbConnection.close()  



# - - - - -  cron  - - - - - -

def obtener_lista_cron_bd():
    # Listar cron
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cursor.execute("SELECT * FROM cron;")
    lista_cron = cursor.fetchall()
    dbConnection.close()
    return lista_cron

def add_cron_bd(lista_cron):
    # Agregar cron a la lista blanca de crontabs
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    restriccion = lista_cron[0]
    config_cron = lista_cron[1]
    comando = lista_cron[2]
    if restriccion == 'si':
        if len(config_cron)>0 and len(comando)>0:
            ban =1
    elif len(restriccion)>0 and len(comando)>0 :
        ban = 1 
    else:
        print("No agregado")
    if ban == 1:
        tupla = (str(restriccion),str(config_cron), str(comando))
        insert_data='INSERT INTO cron(restriccion, config_cron, comando) VALUES({},{},{}) returning id_cron;'
        dbConnection = psycopg2.connect(BD_CONEXION)
        cursor = dbConnection.cursor()
        cursor.execute(sql.SQL(insert_data.format(tupla[0], tupla[1], tupla[2])))
        cursor.commit()
        cursor.close()

def delete_crontab_bd():
    # elimina crontab de la tabla cron
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    dbConnection = psycopg2.connect(BD_CONEXION)
    dbConnection.execute("DELETE FROM cron")
    dbConnection.commit()
    dbConnection.close()  



# - - - - -  reportes  - - - - - -

def add_alarma_bd(fecha,mensaje):
    # agrega un alarma a la tabla alarma
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    if len(mensaje)>0 and len(fecha)>0:
        print("Add alarma bd entro")
        dbConnection = psycopg2.connect(BD_CONEXION)
        cursor = dbConnection.cursor()
        insert_data='INSERT INTO alarma(fecha, mensaje) VALUES({},{});'
        cursor.execute(sql.SQL(insert_data.format("'" + fecha + "'","'" + mensaje + "'")))
        print(cursor.fetchall())
        dbConnection.commit()
        dbConnection.close()

def add_prevencion_bd(fecha, mensaje):
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    if len(fecha)>0 and len(mensaje)>0:
        dbConnection = psycopg2.connect(BD_CONEXION)
        cursor = dbConnection.cursor()
        insert_data='INSERT INTO prevencion(fecha, mensaje) VALUES({},{});'
        cursor.execute(sql.SQL(insert_data.format("'" + fecha + "'" , mensaje + "'")))
        dbConnection.commit()
        dbConnection.close()



# - - - - -  correo  - - - - - -
def obtener_parametros_correo_bd(usuario):
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cmd = "SELECT * FROM correo_config WHERE usuario_nombre = " +"'"+usuario + "'"+ ";" 
    cursor.execute(cmd)
    lista = cursor.fetchone()
    cursor.close()
    return lista 

def add_lista_negra_correo_bd(correo):
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cmd = 'INSERT INTO lista_negra_correo(correo) VALUES({});'
    cursor.execute(sql.SQL(cmd.format("'" + correo + "'" )))
    cursor.execute(cmd)
    cursor.close()

def obtener_lista_negra_correo_bd():
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cmd = "SELECT * FROM lista_negra_correo;" 
    cursor.execute(cmd)
    lista = cursor.fetchall()
    cursor.close()
    return lista


# - - - - -  procesos  - - - - - -
def obtener_lista_blanca_proc_bd():
    if (psycopg2.connect(BD_CONEXION)):
        psycopg2.connect(BD_CONEXION).close()
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cmd = "SELECT * FROM lista_blanca_proc;" 
    cursor.execute(cmd)
    lista = cursor.fetchall()
    cursor.close()
    return lista






# - - - - -  archivos  - - - - - -
def add_hash_archivo(nombre_archivo, hash):
    # Agregar informacion de nuevo hash
    if len(nombre_archivo)>0 and len(hash)>0:
        insert_data='INSERT INTO usuario_registro(nombre_usuario, ip_permitida, dias_permitidos, rango_horario_permitido) VALUES({},{},{},{}) returning nombre_usuario;'
        dbConnection = psycopg2.connect(BD_CONEXION)
        cursor = dbConnection.cursor()
        cursor.execute(sql.SQL(insert_data.format(nombre_archivo, hash)))
        dbConnection.commit()
        dbConnection.close()
    else:
        print("Error. No se pudo agregar hash a la BD")

def obtener_hash_archivo(nombre_archivo):                                   
    # Obtener lista usuario_informacion
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cursor.execute("SELECT hash FROM hashes_archivos;")
    lista_usuario_bd = cursor.fetchall()
    dbConnection.close()
    return lista_usuario_bd

def actualizar_hash(nombre_archivo, hash):
    # Obtener lista usuario_informacion
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cursor.execute(("UPDATE hash FROM hashes_archivos WHERE nombre_archivo={};").format(nombre_archivo))
    dbConnection.commit()
    dbConnection.close()


# - - - - - sniffers - - - - -
def add_sniffers():
    #se carga la lista negra con una lista predeterminada
    lista_negra_sniffers=['tcpdump','wireshark','kismet','cloudShark','ettercap','sysdig']
    insert_data='INSERT INTO sniffers(nombre) VALUES({}) returning nombre;'
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    for nombre in lista_negra_sniffers:
        cursor.execute(sql.SQL(insert_data.format(nombre)))
    dbConnection.commit()
    dbConnection.close()


def obtener_lista_negra_sniffers():
    #se busca la lista negra de procesos que son sniffers
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cursor.execute("SELECT nombre FROM sniffers;")
    lista_negra = cursor.fetchall()
    dbConnection.close()
    return lista_negra
