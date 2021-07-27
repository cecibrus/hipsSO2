import sys
import subprocess
sys.path.insert(0, '/root/hips/base_de_datos')
from funciones_bd import obtener_lista_blanca_proc_bd
sys.path.insert(0, '/root/hips/reportes')
from reporte_alarmas_prevencion import reportar_alarma, reportar_prevencion
sys.path.insert(0, '/root/hips')
from definiciones import MAX_MEM, MAX_CPU
from funciones_procesos import obtener_procesos, kill_proc


def analiza_proceso():
    procesos_lista_blanca = obtener_lista_blanca_proc_bd()
    procesos = obtener_procesos()
    p1 = subprocess.Popen(" sudo ps aux | awk '{print($2,$11,$3,$4)}'", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    (procesos, err) = p1.communicate()
    procesos = procesos.split('\n')

    # %CPU 
    for proceso in procesos:
        proceso_legal = 0
        cpu = proceso[2]
        mem = proceso[3]
        recurso = ""
        for proceso_bd in procesos_lista_blanca:
            if proceso[1] == proceso_bd[1]:
                # Se encuentra dentro de la lista blanca
                proceso_legal = 1
                break
        cmd = "Proceso utiliza el valor máximo de los recursos: "
        if cpu > MAX_CPU:
            # Si supera el porcentaje limite de uso de la cpu
            recurso = recurso + "%CPU"
        if mem > MAX_MEM:
            # Si supera el porcentaje limite de uso de la mem
            if recurso != "":
                recurso = recurso + " & "
            recurso = recurso + "%MEM"
        cmd = cmd + recurso
        if recurso != "":
            if proceso_legal == 1:
                reportar_alarma(cmd, [])
            else :
                pid = proceso[0]
                kill_proc(pid)
                alarma = "El proceso no se encuentra dentro de la lista blanca y utiliza el valor máximo de los recursos: " + recurso
                prev = "El proceso con pid: " + pid + " ha sido matado."
                reportar_alarma(alarma, [])
                reportar_prevencion(alarma, prev, [])