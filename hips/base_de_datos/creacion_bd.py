#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=<salt>
import os
from os import system
import psycopg2
from psycopg2 import sql
from base_de_datos.definiciones import BD_CONEXION


def inicializar_bd():
    # Crea la base de datos
    #conexion = sqlite3.connect(BD_PATH)
    # Modificamos el permiso de la BD para que solo el usuario root tenga acceso
    #delegator.run("sudo chmod 700 " + BD_PATH)
    #se hace la conexión a la BD postgresql
    try:
        dbConnection = psycopg2.connect(BD_CONEXION)
        cursor = dbConnection.cursor()
        os.system("echo Conexión exitosa.")
        try:
            sqlCreateTable= "CREATE TABLE IF NOT EXISTS usuario_registro(nombre_usuario character varying(25) NOT NULL, ip_permitida character varying(16) NOT NULL, dias_permitidos character varying(16) NOT NULL, rango_horario_permitido character varying(15) NOT NULL, PRIMARY KEY (nombre_usuario));"
            cursor.execute(sqlCreateTable)
            os.system("echo Se pudo crear la tabla.")
            cursor.execute("SELECT * FROM usuario_registro;")
            
            insert_data='INSERT INTO usuario_registro(nombre_usuario, ip_permitida, dias_permitidos, rango_horario_permitido) VALUES({},{},{},{}) returning nombre_usuario;'
            usuario_registrado = "'root','localhost','0-1-2-3-4-5-6','00:00-23:00'"
            usuario_registrado = usuario_registrado.strip()
            usuario_registrado = usuario_registrado.split(",")

            cursor.execute(sql.SQL(insert_data.format(usuario_registrado[0], usuario_registrado[1], usuario_registrado[2], usuario_registrado[3])))
            cursor.execute("SELECT * FROM usuario_registro;")
            os.system("echo Se pudo agregar a la tabla.")
            dbConnection.commit()
        except psycopg2.DatabaseError as b:
            os.system("echo Error. No se pudo crear la tabla")
    except psycopg2.DatabaseError as e:
        os.system("echo e")
    finally:
        if dbConnection:
            cursor.close()
            dbConnection.close()
   
 