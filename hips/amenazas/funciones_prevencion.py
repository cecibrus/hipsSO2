import sys
sys.path.insert(0, '/root/hips/reportes')
import subprocess
import os
from reportes.reporte_alarmas_prevencion import reportar_prevencion

def cuarentena(archivo):
    #se cambian los permisos del archivo, se crea el directorio de cuarentena si no existe y se mueve el archivo
    os.chmod(archivo, 000)
    os.mkdir("/tmp/.cuarentena")
    subprocess.Popen("sudo mv "+ str(archivo) + "/tmp/.cuarentena")