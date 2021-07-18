import os
import string
import subprocess



# Funciones para el usuario
def eliminar_usuario(nombre_usuario):
    # Elimina un usuario del sistema
    if nombre_usuario != 'root' :
        os.system("sudo userdel -r sammy")

def cambiar_contrasena(nombre_usuario):
    # Cambia la contrasena de  un usuario por una aleatoria 
    c = "openssl rand -base64 15"
    p1 = subprocess.Popen(c, shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    contrasena, err = p1.communicate() 
    cmd = 'sudo usermod -p `perl -e "print crypt("'+contrasena+'","Q4")"` '+nombre_usuario
    os.system(cmd)

def cerrar_sesion(nombre_usuario):
    # Cierra la sesion de un usuario
    cmd = "pkill -KILL -u " + str(nombre_usuario)
    os.system(cmd)

def bloquear_usuario(nombre_usuario):
    # Bloquear un usuario por usermod
    if nombre_usuario != "root": # No se permite bloquear al usuario root              
        cmd="sudo usermod -L " + str(nombre_usuario)
        os.system(cmd)

def encontrar_ip(nombre_usuario):
    # Retorna el ip de un usuario a traves del nombre de usuario
    cmd = "who | awk '{print($1,$5)}' | sed 's/(//g' | sed 's/)//g'"  
    p1 = subprocess.Popen(cmd, shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    conectados, err = p1.communicate() 
    lista = conectados.split('\n')
    ip = []
    for usuarios in lista:
        usuario = usuarios.split(' ')
        if usuario[0] == nombre_usuario:
            ip.append(usuario[1])
    return ip
