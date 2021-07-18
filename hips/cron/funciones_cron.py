import os
import subprocess

def eliminar_cron(usuario):
    cmd = "sudo crontab -r -u" + usuario 
    os.system(cmd)

def listar_arhivos_crontabs():
    cmd = "ls /var/spool/cron/*"
    p1 = subprocess.Popen(cmd, shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    crontabs, err = p1.communicate() 
    lista = crontabs.split('\n')
    result = []
    for cron in lista:
        aux = cron.split('cron/')
        if aux != [''] :
            result.append(aux[1])
    return result
