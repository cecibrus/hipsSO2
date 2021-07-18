import sys
from datetime import datetime
sys.path.insert(0, '/root/hips')
from definiciones import CORREO
import subprocess
sys.path.insert(0, '/root/hips/base_de_datos')
from funciones_bd import  add_alarma_bd, add_prevencion_bd

def reportar_alarma(tipo_alarma, ip):
    hoy = datetime.now()
    fecha = hoy.strftime("%Y/%m/%d %H:%M:%S")
    if ip!=[]:
        mensaje = str(fecha) +" :: "+ tipo_alarma +" :: " + " ".join(ip)
    else:
        mensaje = str(fecha) + " :: " + tipo_alarma 
    msj = "echo " + mensaje + ">> /var/log/hips/alarmas.log"
    p1 =subprocess.Popen(msj, stdout=subprocess.PIPE, shell=True)
    output, err = p1.communicate() 
    try:
        #add_alarma_bd(fecha,mensaje)
        subject = "Reporte de Alarma"
        msg_correo = "echo " + '"ALARMA: ' + mensaje + '"' + " | mail -s " + '"' + subject + '" ' + CORREO
        p1 =subprocess.Popen(msg_correo, stdout=subprocess.PIPE, shell=True)
        output, err = p1.communicate() 	   
    except:
        print("\n\n\nError. No se pudo agregar el alarma a la tabla\n\n\n")


def reportar_prevencion(situacion, decision_tomada, ip):
    fecha = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    if ip!=[]:
        mensaje = str(fecha) +" :: "+ situacion +" :: " + decision_tomada + " :: " + " ".join(ip)
    else:
        mensaje = str(fecha) +" :: "+ situacion +" :: " + decision_tomada 
    msj = "echo " + mensaje + ">> /var/log/hips/prevencion.log"

    p1 =subprocess.Popen(msj, stdout=subprocess.PIPE, shell=True)
    output, err = p1.communicate() 
    try:
        add_prevencion_bd(fecha,mensaje)	
        subject = '"Reporte de Prevención"'
        msg_correo = "echo " + '"PREVENCION: ' + mensaje + '"' + " | mail -s " + subject + CORREO
        p1 =subprocess.Popen(msg_correo, stdout=subprocess.PIPE, shell=True)
        output, err = p1.communicate() 	
    except:
        print("\n\n\nError. No se pudo agregar a la tabla\n\n\n")
        
