import sys
sys.path.insert(0, '/root/hips/reportes')
from reportes.reporte_alarmas_prevencion import reportar_alarma
import os
import subprocess
sys.path.insert(0, '/root/hips/base_de_datos')
from base_de_datos.funciones_bd import add_hash_archivo
import hashlib


#Compara el hash de ka base de datos con el de
def analisis_hash(nombre_archivo, hash_esperado):
    md5_hash = hashlib.md5()
    archivo = None

    # Ver si no hay hash en la base de datos para ese archivo, en ese caso se crea
    if hash_esperado == "":
        reportar_alarma(" No hay hash para " + nombre_archivo)
        add_hash_archivo(nombre_archivo, hash_esperado)

    # se prueba abrir el archivo
    try:
        archivo = open(nombre_archivo, "rb")
        data = archivo.read()
    except:
        reportar_alarma("EL archivo no existe o no se puede abrir.")
    finally:
        if archivo is not None:
            archivo.close()

    # comparando los hashes
    if archivo is not None:
        md5_hash.update(data)
        datos_hasheados = md5_hash.hexdigest()

        if datos_hasheados == hash_esperado:
            # no hay cambios
            print("No hay cambios")
        else:
            # cambio el hash entonces se envia una alerta y correo
            reportar_alarma("El hash del archivo" + nombre_archivo + "ha cambiado.")
