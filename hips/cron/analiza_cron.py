import os
import subprocess
from base_de_datos.funciones_bd import obtener_lista_cron
from cron.funciones_cron import listar_crontabs_en_ejecucion,eliminar_cron

def analizar_crontabs():
    lista_cron = listar_crontabs_en_ejecucion()
    lista_bd = obtener_lista_cron()
    
    for cron_en_ejec in lista_cron:
        cron_en_ejec = cron_en_ejec.split('/')
        usuario_cron = cron_en_ejec[3]
        comando = "sudo crontab -l -u" + usuario_cron 
        p1 = subprocess.Popen(comando, shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        result, err = p1.communicate() 
        crontab_actual = result.split('\n')
        for cron_bd in lista_bd:
            restric_bd = cron_bd[0]
            config_bd = cron_bd[1]
            usuario_bd = cron_bd[2]
            cmd_bd = cron_bd[3]
            cadena = crontab_actual.find(cmd_bd)
            if cadena!= -1:
                if(cron_bd[0]=='si'):                   #requiere de un control mas estricto en la configuracion
                    cron_valido = str(config_bd + usuario_bd + cmd_bd)
                    if cron_valido == crontab_actual:                        
                        ban = 1
                        break
                else:
                    ban = 1
                    break
        if ban==0:
            print("Crontab ilegal. Reportar alarma")
            eliminar_cron(usuario_cron)
