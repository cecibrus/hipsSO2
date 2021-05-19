import os            #libreria de funciones del sistema operativo --> https://docs.python.org/3/library/os.html
import sys
import cmd
import shutil
import subprocess
import datetime

#pyscopg2 es un adaptador --> https://pypi.org/project/psycopg2/

# Comandos: cat /var/log/messages | grep -i
#           lsof  -p  pid | grep  libpcap
#           ps -aux
#           md5sum --> para sacar

#Alarmas mandar por correo? Poner en la interfaz web?

#Para todos en caso de que haya algun problema se debe registrar en el log: alarmas.log y si se toman medidas prevencion en prevencion.log

#direcciones que se usan
direccionLogAlarma='/var/log/hips/alarmas.log'
direccionLogPrevencion='/var/log/hips/prevencion.log'

#deficion de funciones extra

#Funcion registroLog que es una version general para escribir en los logs. 
#Se le pasa como parametro el archivo en el que hay que escribir, y el mensaje de alarma/prevencion
#Abre el archivo, escribe el registro y luego lo cierra
def registroLog(registro, archivo):
    fecha=datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    mensaje= fecha + registro + '\n'
    f=open(archivo, 'a')
    f.write(mensaje)
    f.close()


def compara_md5(archivo, hash):
    comando= 'md5sum' + archivo
    retorno=subprocess.Popen(comando)
    if retorno !=hash:
        #alerta en el log 
        registroLog('El hash no es igual', direccionLogAlarma)



#Verificar archivos binarios de sistema y en particular modificaciones realizadas en el archivo /etc/passwd o /etc/shadow.
#subprocess.Popen-->para correr los comandos del sistema
compara_md5('/etc/passwd',6797575) #-----El hash que es el segundo parametro se saca de la base de datos

#Chequear si hay sniffers o si el equipo ha entrado en modo promiscuo. No
#deben controlar solamente los registros de auditorías, sino también deben
#controlar que no existan herramientas conocidas de aplicaciones de captura de
#paquetes en ejecución, como tcpdump, ethereal, wireshark entre otros. Para el
#módulo de prevención estas herramientas deben ser bloqueadas o eliminadas
#del sistema, además de todas las consideraciones vistas en clases.

#Estos son algunos de los comandos para empezar esas verificaciones
#           cat /var/log/messages | grep -i
#           lsof  -p  pid | grep  libpcap


#Verificar el tamaño de la cola de mails del equipo. El módulo de prevención
#puede implicar bloquear IPs o usuarios generadores de correo masivo.



# Verificar directorio /tmp; que no hayan procesos con nombres extraños o scripts
#ubicados en el mismo. Puede ser tomada como medida de prevención la
#eliminación del archivo o mudarlo a una carpeta de cuarentena.

#Cómo hacer para verificar scripts???

# Examinar archivos que estén ejecutándose como cron.

#tienen que estar en /etc/cron? ver como verificar desde ahi. Como saber si hay nuevos?