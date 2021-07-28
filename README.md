# hipsSO2
## Sistema de prevención de intrusos - Trabajo Práctico Sistemas Operativos 2
#### Hecho por Belén Mareco y Cecilia Brusquetti

## MANUAL HIPS-SO2 2021
HIPS es un sistema de prevención de instrusos desarrollado en Python. IPS host based o basados en host (HIPS); basado principalmente en los registros de auditoría que generan las estaciones de trabajo o servidores.

#### Funcionamiento:
1.Verifica los archivos binarios del sistema
2.Verifica los usuarios que se encuentran conectados en el sistema
3.Verifica si alguna interfaz se encuentra en modo promiscuo y/o hay algún proceso de captura de paquetes ejecutándose.
4.Examina los archivos logs: s
5.Verifica el tamaño de la cola de emails.
6.Verifica los procesos que se están ejecutando en el sistema
7.Verifica el directorio /tmp en buscar de scripts. 
8.Controla posibles ataques DNS 
9.Verifica los archivos que se ejecutan como cron
10.Verifica los intentos de accesos no válidos

#### Requerimientos
Para el correcto funcionamiento del sistema se necesitan instalar ciertas herramientas. Para la instalación de estas herramientas en CENTOS 8 es necesario utilizar el comando : yum install.
Los requerimientos del sistema son los siguientes:
Python3: El sistema está desarrollado con el lenguaje Python por lo que requiere de su instalación. Para instalarlo ejecute el comando:  sudo yum install python3   y  sudo yum install python3-devel	

GCC:  Se debe instalar gcc para poder ejecutar los scripts de python. Para instalarlo ejecute el comando : sudo yum install gcc
 
PHP: La interfaz web fue desarrollada con PHP, por lo que requiere de su instalación, ejecute el comando: sudo yum install php
PIP3: Para contar con las librerías de Python, es necesario instalar pip3: sudo yum install pip3 o sudo yum install python3-pip

Psutil: Para ejecutar los comandos de Python: 
pip3 install psutil

PostgreSQL:El sistema utiliza este gestor de bases de datos, por lo que es necesario su instalación.Instalamos de la siguiente manera:
sudo yum install postgresql-client
sudo yum install postgresql-devel

#### Configuración de PostgreSQL
El sistema utiliza por default al usuario postgres para la administración de nuestra base de datos. Por lo que si desea crear un nuevo usuario es necesario que ejecute los siguientes comandos:
Primeramente ingresamos a la cuenta de postgres y luego creamos la base de datos que utilizaremos
su - postgres					
psql
#CREATE DATABASE hips;
#CREATE USER nombre_usuario WITH PASSWORD ‘contraseña’;
#GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nombre_usuario;
Una vez creada la base de datos, el usuario y de otorgarles los privilegios sobre la base de datos, podemos salir de PostgreSQL y de la cuenta de postgres con los siguientes comandos:
\q
Exit
 
 
 
 
#### Configuración del archivo pg_hba.conf
El método de autenticación que utiliza PostgreSQL es ident, lo que causa algunos inconvenientes para el buen funcionamiento del sistema. Por lo que requiere de una configuración manual previamente.
Para hacerlo debemos editar el archivo pg_hba.conf, primeramente nos ubicamos en la ubicación de donde se encuentra este archivo y posteriormente abrimos el archivo con el editor de archivos VI con el comando :
cd /var/lib/pgsql/data/
vi pg_hba.conf
Modificamos en la siguiente línea por la línea guiada por la flecha de la ilustración siguiente:
 local all all ident  ---> local all all md5
O local all all peer  ---> local all all md5
También en la siguiente línea realizamos el mismo procedimiento:
host all all 127.0.0.1/32 ident ---> host all all 127.0.0.1/32 md5
O  host all all 127.0.0.1/32 peer ---> host all all 127.0.0.1/32 md5
 
El último paso consiste en agregar nuestra IP en la línea siguiente:
 host all all nuestra_ip md5
Finalmente guardamos nuestro archivo y reiniciamos el servidor de postgres.
sudo service postgresql restart
 
 
 
#### Configuración de directorios
Se debe modificar los permisos del archivo definiciones.py ubicada en la carpeta hips. Desde el usuario root cambiar los permisos con el siguiente comando:
Chmod 00 definiciones.py
Interfaz gráfica
Ubicamos el directorio a la ubicación del directorio de su servidor web.
Iniciamos nuestro servidor (el sistema utiliza Apache): sudo service httpd start
Corremos nuestro programa en nuestra sistema con el siguiente comando:
php -S localhost:4000 , donde utilizamos el puerto 4000
 
#### Configuración terminada
Finalmente, la configuración previa del sistema ya está terminada y lista para su utilización
