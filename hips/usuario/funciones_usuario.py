import os
import string
import subprocess




def eliminar_usuario(nombre_usuario):
    if nombre_usuario != 'root' :
        os.system("sudo userdel -r sammy")

                
# Cambiar contrasena de usuario por una aleatoria y enviar por correo
def cambiar_contrasena(nombre_usuario):
    c = "openssl rand -base64 15"
    p1 = subprocess.Popen(c, shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    contrasena, err = p1.communicate() 
    cmd = 'sudo usermod -p `perl -e "print crypt("'+contrasena+'","Q4")"` '+nombre_usuario
    os.system(cmd)

# Cierra la sesion de un usuario
def cerrar_sesion(nombre_usuario):
    cmd = "pkill -KILL -u " + str(nombre_usuario)
    os.system(cmd)

    
# Bloquear un usuario por usermod
def bloquear_usuario(nombre_usuario):
    if nombre_usuario != "root": # No se permite bloquear al usuario root              
        cmd="sudo usermod -L " + str(nombre_usuario)
        os.system(cmd)