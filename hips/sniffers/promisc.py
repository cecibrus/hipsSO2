# cat /var/log/messages | grep -i promisc --- para ver cuales son las interfaces que entraron en modo promiscuo
import sys
sys.path.insert(0, '/root/hips/reportes')
from reportes.reporte_alarmas_prevencion import reportar_alarma, reportar_prevencion
import os
import subprocess
from base_de_datos.funciones_bd import obtener_lista_negra_sniffers
sys.path.insert(0, '/root/hips/proceso')
from proceso.funciones_procesos import kill_proc


def interfaces_promiscuas():
    p=subprocess.Popen("cat /var/log/messages  | grep -i promisc", stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    for line in output:
        reportar_alarma(line + "ha entrado en modo promiscuo")

def buscar_sniffers():
    lista_negra=obtener_lista_negra_sniffers
    for line in lista_negra:
        ps=subprocess.Popen("sudo ps -AF | awk '{print $11}' | grep " + str(line), stdout=subprocess.PIPE, shell=True)
        outputs,errs=ps.communicate
        for proceso in outputs:
            reportar_alarma('Aplicacion sniffer detectada:' + str(line))
            reportar_prevencion('Se detuvo la aplicacion'+ str(proceso) + 'y se envio el archivo a cuarentena')
            kill_proc(proceso)


def analizar_sniffers():
    interfaces_promiscuas()
    buscar_sniffers()