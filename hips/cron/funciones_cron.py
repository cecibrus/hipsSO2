import os
import subprocess

def eliminar_cron(usuario):
    cmd = "sudo crontab -r -u" + usuario 
    os.system(cmd)

def listar_crontabs_en_ejecucion():
    cmd = "ls /var/spool/cron/*"
    p1 = subprocess.Popen(cmd, shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    crontabs, err = p1.communicate() 
    lista = crontabs.split('\n')
    return lista


