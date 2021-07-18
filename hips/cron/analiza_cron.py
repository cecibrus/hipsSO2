import sys
sys.path.insert(0, '/root/hips/reportes')
from reporte_alarmas_prevencion import reportar_alarma, reportar_prevencion
sys.path.insert(0, '/root/hips/usuario')
from funciones_usuario import encontrar_ip
import os
import subprocess
sys.path.insert(0, '/root/hips/base_de_datos')
from funciones_bd import obtener_lista_cron_bd, obtener_lista_cron_bd
sys.path.insert(0, '/root/hips/cron')
from funciones_cron import listar_arhivos_crontabs, eliminar_cron

def analizar_crontabs():
    lista_cron = listar_arhivos_crontabs()
    lista_bd = obtener_lista_cron_bd()
    for usuario_cron in lista_cron:
        comando = "sudo crontab -l -u " + usuario_cron
        p1 = subprocess.Popen(comando, shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        result, err = p1.communicate() 
        crontab_actual = result.split('\n')
        for cron in crontab_actual:
            if cron != '':
                ban = 0
                for cron_bd in lista_bd:
                    restric_bd = cron_bd[0]
                    config_bd = cron_bd[1]
                    cmd_bd = cron_bd[2]
                    cadena = cron.find(cmd_bd)
                    print("Cron de la bd:")
                    print(cron_bd)
                    print("Cron conectado: ")
                    print(cron)
                    if cadena!= -1:
                        if(restric_bd=='si'):                   #requiere de un control mas estricto en la configuracion
                            cron_valido = str(config_bd + " " + cmd_bd)
                            if cron_valido == cron:                        
                                ban = 1
                                break
                        else:
                            ban = 1
                            break
                if ban==0:
                    print("Crontab ilegal. Reportar alarma")
                    mensaje = "Crontab en ejecución desconocido"
                    reportar_alarma(mensaje, encontrar_ip(usuario_cron))
                    #eliminar_cron(usuario_cron)
                    #reportar_prevencion(mensaje, "Crontab eliminado", encontrar_ip(usuario_cron))
