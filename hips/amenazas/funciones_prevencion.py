import sys
sys.path.insert(0, '/root/hips/reportes')
import subprocess
import os
from reportes.reporte_alarmas_prevencion import reportar_prevencion

def matar_proceso(proceso):
    pp=subprocess.Popen("pidof"+ str(proceso), stdout=subprocess.PIPE, shell=True)
    outputp, errp= pp.communicate()
    if outputp=='':
        try:
            os.kill(proceso)
        except:
            reportar_prevencion('No se pudo detener el proceso' + str(proceso))
    else:
        os.kill(outputp)


def cuarentena(archivo):
    #se cambian los permisos del archivo, se crea el directorio de cuarentena si no existe y se mueve el archivo
    os.chmod(archivo, 000)
    os.mkdir("/tmp/.cuarentena")
    subprocess.Popen("sudo mv "+ str(archivo) + "/tmp/.cuarentena")