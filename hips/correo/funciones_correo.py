import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import subprocess
sys.path.insert(0, '/root/hips/base_de_datos')
from funciones_bd import obtener_mail_configuracion


def enviar_correo(receptor, subject, body):
    lista = obtener_mail_configuracion ("admin")
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
    servidor.sendmail(mensaje)

    del mensaje
    servidor.quit()

def reject_email(correo):
    cmd = "echo " + correo + "> /etc/postfix/access"
    p1 =subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, err = p1.communicate()

