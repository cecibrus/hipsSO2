from base_de_datos.definiciones import BD_CONEXION
import psycopg2
from psycopg2 import extras
from psycopg2 import sql

# Agregar informacion de nuevo usuario
def add_usuario_registro():
    print("Agregar un nuevo usuario")
    print("[nombre_usuario]: ")
    nombre_usuario = input()
    print("[ubicacion_permitida]: ")
    ip_permitida = input()
    print("[dias_permitidos]: (Formato: x-x-x-x-x...)")
    dias_permitidos = input()  
    print("[rango_horario_permitido]  (Formato: xx:xx-xx:xx): ")
    rango_horario_permitido = input() 
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



# Obtener lista usuario_informacion
def obtener_lista_usuario_registro():
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cursor.execute("SELECT * FROM usuario_registro;")
    lista_usuario_bd = cursor.fetchall()
    dbConnection.close()
    return lista_usuario_bd
    
    
# Resetear usuario_informacion
def reset_usuario_registro():
    dbConnection = psycopg2.connect(BD_CONEXION)
    dbConnection.execute("DELETE FROM usuario_registro")
    dbConnection.commit()
    dbConnection.close()  


#CRON
# Listar cron
def obtener_lista_cron():
    dbConnection = psycopg2.connect(BD_CONEXION)
    cursor = dbConnection.cursor()
    cursor.execute("SELECT * FROM cron;")
    lista_cron = cursor.fetchall()
    dbConnection.close()
    return lista_cron

# Agregar cron a la lista blanca de crontabs
def add_cron():
    print("Crontab con restriccion: (si o no)")
    restriccion = input()
    print("Configuración de tiempo: (solo para comandos con restricciones)")
    print("[m h dom mon dow]: ")
    config_cron = input()
    print("[user]: ")
    usuario_cron = input()
    print("[comand]:")
    comando = input()  
    if restriccion == 'si':
        if len(config_cron)>0 and len(usuario_cron)>0 and len(comando)>0:
            ban =1
    elif len(restriccion)>0 and len(usuario_cron)>0 and len(comando)>0 :
        ban = 1 
    else:
        print("No agregado")
    if ban == 1:
        tupla = (str(restriccion),str(config_cron),str(usuario_cron),str(comando))
        insert_data='INSERT INTO cron(restriccion, config_cron, usuario_cron, comando) VALUES({},{},{},{}) returning id_cron;'
        dbConnection = psycopg2.connect(BD_CONEXION)
        cursor = dbConnection.cursor()
        cursor.execute(sql.SQL(insert_data.format(tupla[0], tupla[1], tupla[2], tupla[3])))
        dbConnection.commit()
        dbConnection.close()

def delete_crontab(usuario):
    dbConnection = psycopg2.connect(BD_CONEXION)
    dbConnection.execute("DELETE FROM cron")
    dbConnection.commit()
    dbConnection.close()  
