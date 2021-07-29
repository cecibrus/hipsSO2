import sys
sys.path.insert(0, '/root/hips')
from definiciones import CORREO
from datetime import datetime
import subprocess
sys.path.insert(0, '/root/hips/base_de_datos')
from funciones_bd import  add_alarma_bd, add_prevencion_bd
sys.path.insert(0, '/root/hips/correo')
from funciones_correo import enviar_correo

def reportar_alarma(tipo_alarma, ip):
    hoy = datetime.now()
    fecha = hoy.strftime("%Y/%m/%d %H:%M:%S")
    mensaje = ""
    lista_ip = []
    if(type(ip) is not list):
            lista_ip.append(ip)
    else:
        lista_ip = ip

    if lista_ip!=[]:
        mensaje = str(fecha) +" :: "+ str(tipo_alarma) +" :: " + " ".join(lista_ip)
    else:
        mensaje = str(fecha) + " :: " + str(tipo_alarma) 

    msj = "echo " + mensaje + " >> /var/log/hips/alarmas.log"
    p1 =subprocess.Popen(msj, stdout=subprocess.PIPE, shell=True)
    output, err = p1.communicate() 
    try:
        add_alarma_bd(fecha,mensaje)
        subject = "Reporte de Alarma"
        enviar_correo(CORREO, subject, mensaje)
    except:
        print("\n\n\nError. No se pudo agregar el alarma a la tabla\n\n\n")


def reportar_prevencion(situacion, decision_tomada, ip):
    fecha = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    mensaje= ""
    lista_ip = []
    if(type(ip) is not list):
        lista_ip.append(ip)
    else:
        lista_ip = ip

    if lista_ip!=[]:
        mensaje = str(fecha) +" :: "+ str(situacion) +" :: " + str(decision_tomada) + " :: " + " ".join(lista_ip)
    else:
        mensaje = str(fecha) +" :: "+ str(situacion) +" :: " + str(decision_tomada)

    msj = "echo " + str(mensaje) + " >> /var/log/hips/prevencion.log"

    p1 =subprocess.Popen(msj, stdout=subprocess.PIPE, shell=True)
    output, err = p1.communicate() 
    try:
        add_prevencion_bd(fecha,mensaje)	
        subject = '"Reporte de Prevención"'
        enviar_correo(CORREO, subject, mensaje)
    except:
        print("\n\n\nError. No se pudo agregar a la tabla\n\n\n")
        
