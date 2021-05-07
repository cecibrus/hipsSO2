import os            #libreria de funciones del sistema operativo --> https://docs.python.org/3/library/os.html
import sys
import cmd
import shutil
import subprocess

#pyscopg2 es un adaptador --> https://pypi.org/project/psycopg2/

# Comandos: cat /var/log/messages | grep -i
#           lsof  -p  pid | grep  libpcap
#           ps -aux
#           md5sum --> para sacar

#Alarmas mandar por correo? Poner en la interfaz web?

#Para todos en caso de que haya algun problema se debe registrar en el log: alarmas.log y si se toman medidas prevencion en prevencion.log

#Verificar archivos binarios de sistema y en particular modificaciones realizadas en el archivo /etc/passwd o /etc/shadow.
#subprocess.Popen-->para correr los comandos del sistema
retorno=subprocess.Popen('md5sum /etc/passwd') 
#aca se hace la comparacion
retorno=subprocess.Popen('md5sum /etc/shadow') 
#comparacion de nuevo

#Verificar los usuarios que están conectados. Y desde que origen.


#Chequear si hay sniffers o si el equipo ha entrado en modo promiscuo. No
#deben controlar solamente los registros de auditorías, sino también deben
#controlar que no existan herramientas conocidas de aplicaciones de captura de
#paquetes en ejecución, como tcpdump, ethereal, wireshark entre otros. Para el
#módulo de prevención estas herramientas deben ser bloqueadas o eliminadas
#del sistema, además de todas las consideraciones vistas en clases.


#Examinar los archivos log: Se deben buscar patrones de acceso indebidos en las
#bitácoras del sistema. A partir de lo detectado, deberán bloquear IPs o cambiar
#contraseña de usuario o directamente bloquear un usuario, incluso puede
#requerir bajar temporalmente el servicio de correo.
#    1. Failed Password y Authentication Failure en el /var/log /secure y
#    /var/log/messages
#    2. Errores de carga de páginas desde un mismo IP, como se estuvieren
#    buscando un sitio desconocido. /var/log/httpd/access.log
#    3. Envío de mails masivos desde una misma cuenta, se puede verificar la
#    cola de mails, así como el registro del mail /var/log/maillog
#    4. Entre otros...

#Verificar el tamaño de la cola de mails del equipo. El módulo de prevención
#puede implicar bloquear IPs o usuarios generadores de correo masivo.

#Los procesos que consumen un porcentaje elevado de memoria. Se puede
#matar el proceso que está consumiendo mucho recurso, bajo algún criterio
#como tiempo de consumo excesivo.

# Verificar directorio /tmp; que no hayan procesos con nombres extraños o scripts
#ubicados en el mismo. Puede ser tomada como medida de prevención la
#eliminación del archivo o mudarlo a una carpeta de cuarentena.

# Controlar ataque de DDOS, para esto el profesor proveerá una muestra de un
#registro log con ataques de DDOS para que sea procesada la información. En
#este caso al servicio de DNS. Acá puede significar bloquear un IP o incluso bajar
#un servicio.

# Examinar archivos que estén ejecutándose como cron.

# Verificar intentos de accesos no válidos. Ya sea desde un mismo usuario
#intentos repetitivos o desde un IP intentos de accesos con múltiples usuarios.