import datetime
from definiciones import CORREO
import subprocess
from base_de_datos.funciones_bd import  add_alarma, add_prevencion

def reportar_alarma(tipo_alarma, ip):
    fecha = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    if ip!='':
        mensaje = fecha +" :: "+ tipo_alarma +" :: " + ip 
    else:
        mensaje = fecha +" :: "+ tipo_alarma 
    p1 =subprocess.Popen("cat mensaje >>/var/log/hips/alarmas.log", stdout=subprocess.PIPE, shell=True)
    output, err = p1.communicate() 
    try:
        add_alarma(fecha,mensaje)
        subject = '"Reporte de Alarma"'
        msg_correo = "echo " + '"ALARMA: ' + mensaje + '"' + " | mail -s " + subject + CORREO
        p1 =subprocess.Popen(msg_correo, stdout=subprocess.PIPE, shell=True)
        output, err = p1.communicate() 	
       
    except:
        print("\n\n\nError. No se pudo agregar el alarma a la tabla\n\n\n")


def reportar_prevencion(situacion, decision_tomada, ip):
    fecha = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    if ip!='':
        mensaje = fecha +" :: "+ situacion +" :: " + decision_tomada + " :: " + ip
    else:
        mensaje = fecha +" :: "+ situacion +" :: " + decision_tomada 

    p1 =subprocess.Popen("cat mensaje >>/var/log/hips/prevencion.log", stdout=subprocess.PIPE, shell=True)
    output, err = p1.communicate() 
    try:
        add_prevencion(fecha,mensaje)	
        subject = '"Reporte de Prevención"'
        msg_correo = "echo " + '"PREVENCION: ' + mensaje + '"' + " | mail -s " + subject + CORREO
        p1 =subprocess.Popen(msg_correo, stdout=subprocess.PIPE, shell=True)
        output, err = p1.communicate() 	
    except:
        print("\n\n\nError. No se pudo agregar a la tabla\n\n\n")
        