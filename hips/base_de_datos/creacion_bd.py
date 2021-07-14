#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=<salt>
import os
from os import system
import psycopg2
from psycopg2 import sql
from definiciones import BD_CONEXION


def inicializar_bd():
    # Crea la base de datos
    try:
        dbConnection = psycopg2.connect(BD_CONEXION)
        cursor = dbConnection.cursor()
        try:    
            # CREACION DE LAS TABLAS
            usuario_registro_t = "CREATE TABLE IF NOT EXISTS usuario_registro(nombre_usuario character varying(25) NOT NULL, ip_permitida character varying(16) NOT NULL, dias_permitidos character varying(16) NOT NULL, rango_horario_permitido character varying(15) NOT NULL, PRIMARY KEY (nombre_usuario));"
            cron_t = "CREATE TABLE IF NOT EXISTS cron(id_cron integer NOT NULL, restriccion character varying(3) NOT NULL, config_cron character varying(20), comando character varying(60) NOT NULL, PRIMARY KEY(id_cron));"
            alarma_t = "CREATE TABLE IF NOT EXISTS alarma(id_alarma integer NOT NULL, fecha DATE NOT NULL, mensaje character varying(30) NOT NULL, PRIMARY KEY(id_alarma));"
            prevencion_t= "CREATE TABLE IF NOT EXISTS prevencion(id_prevencion integer NOT NULL, fecha DATE NOT NULL, mensaje character varying(30) NOT NULL, PRIMARY KEY(id_prevencion));"

            # EJECUCION DE LOS COMANDOS PARA CREAR TABLAS
            cursor.execute(usuario_registro_t)
            cursor.execute(cron_t)
            cursor.execute(alarma_t)
            cursor.execute(prevencion_t)

            # VALORES POR DEFAULT
            usuario_registrado = ['root','localhost','0-1-2-3-4-5-6','00:00-23:00']
            cron = [('si', '* * * * root', 'echo date >> pruebacron.txt'),('no','','echo hola >> pruebacron2.txt')]
            
            # CADENAS DE INSERT
            usuario_registro_i='INSERT INTO usuario_registro(nombre_usuario, ip_permitida, dias_permitidos, rango_horario_permitido) VALUES({},{},{},{}) returning nombre_usuario;'
            cron_i='INSERT INTO cron(restriccion, config_cron, comando) VALUES({},{},{}) returning id_cron;'

            # INSERT EN LAS TABLAS
            # usuario_registro
            cursor.execute(sql.SQL(usuario_registro_t.format(usuario_registrado[0], usuario_registrado[1], usuario_registrado[2], usuario_registrado[3])))
            # cron 
            for dato in cron_i:
                cursor.execute(sql.SQL(cron.format(cron[0], cron[1], cron[2])))
           
            dbConnection.commit()

        except psycopg2.DatabaseError as b:
            os.system("echo Error. No se pudo crear la tabla")
    except psycopg2.DatabaseError as e:
        os.system("echo e")
    finally:
        if dbConnection:
            cursor.close()
            dbConnection.close()
   
 
 
