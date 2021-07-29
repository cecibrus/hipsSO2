import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import subprocess
sys.path.insert(0, '/root/hips/base_de_datos')
from funciones_bd import obtener_parametros_correo_bd
sys.path.insert(0, '/root/hips/reportes')
from reportes.reporte_alarmas_prevencion import reportar_alarma, reportar_prevencion
sys.path.insert(0, '/root/hips')
from definiciones import MAX_COLA_CORREOS


def enviar_correo(receptor, subject, body):
    lista = obtener_parametros_correo_bd ("admin")
    correo = lista[2]
    passwd = lista[3]

    mensaje = MIMEMultipart()
    # Establecemos los parametros 
    mensaje['From'] = correo
    mensaje['To'] = receptor
    mensaje['Subject'] = subject

    mensaje.attach(MIMEText(body, 'plain'))
    # Establecemos el servidor
    servidor = smtplib.SMTP('smtp.gmail.com: 587')
    servidor.starttls()

    servidor.login(correo, passwd)
    servidor.send_message(mensaje)

    del mensaje
    servidor.quit()


def reject_email(correo):
    cmd = "echo " + correo + "> /etc/postfix/access"
    p1 =subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, err = p1.communicate()


def verificar_cola():
    p =subprocess.Popen("mailq", stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    cola= output.decode("utf-8").splitlines()
    if len(cola)>MAX_COLA_CORREOS:
        #se detiene el servicio de correo 
        p =subprocess.Popen("service postfix stop", stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        #reportar_alarma("Se supero el limite de la cola de correos")
        #reportar_prevencion("Se supero el limite de la cola de correos", "Se detuvo el servicio de correo")
