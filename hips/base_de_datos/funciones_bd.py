import sys
sys.path.insert(0, '/root/hips')
from definiciones import BD_CONEXION
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
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cursor.execute("SELECT * FROM usuario_registro;")
    lista_usuario_bd = cursor.fetchall()
    dbConnection.close()
    return lista_usuario_bd
    
def reset_usuario_registro_bd():
    # Resetear usuario_informacion
    dbConnection = psycopg2.connect(BD_CONEXION)
    dbConnection.execute("DELETE FROM usuario_registro")
    dbConnection.commit()
    dbConnection.close()  



# - - - - -  cron  - - - - - -

def obtener_lista_cron_bd():
    # Listar cron
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cursor.execute("SELECT * FROM cron;")
    lista_cron = cursor.fetchall()
    dbConnection.close()
    return lista_cron

def add_cron_bd(lista_cron):
    # Agregar cron a la lista blanca de crontabs
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
    dbConnection = psycopg2.connect(BD_CONEXION)
    dbConnection.execute("DELETE FROM cron")
    dbConnection.commit()
    dbConnection.close()  



# - - - - -  alarma  - - - - - -

def add_alarma_bd(fecha,mensaje):
    # agrega un alarma a la tabla alarma
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
    if len(fecha)>0 and len(mensaje)>0:
        dbConnection = psycopg2.connect(BD_CONEXION)
        cursor = dbConnection.cursor()
        insert_data='INSERT INTO prevencion(fecha, mensaje) VALUES({},{});'
        cursor.execute(sql.SQL(insert_data.format("'" + fecha + "'" + mensaje + "'")))
        dbConnection.commit()
        dbConnection.close()
