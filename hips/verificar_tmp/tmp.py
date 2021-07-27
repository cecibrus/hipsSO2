import sys
sys.path.insert(0, '/root/hips/reportes')
import subprocess
import sys
sys.path.insert(0, '/root/hips/amenazas')
from amenazas.funciones_prevencion import cuarentena
from reportes.reporte_alarmas_prevencion import reportar_prevencion, reportar_alarma

#hay que buscar scripts y cualquier proceso que pueda ser extraño. Verificar terminaciones sh, py java, php, c
def buscar_ejecutable_o_sospechoso():
    #primero buscamos los archivos que son scripts
    p=subprocess.Popen("sudo grep -aril '#!' /tmp", stdout=subprocess.PIPE, shell=True) 
    output, err= p.communicate()

    #ahora busca los archivos que son . algo viendo alguna extension comun de script
    extensiones=['.py','.java','.c','.csh','.pl','.sh','.cpp','.exe','.php']
    for extension in extensiones:
        p=subprocess.Popen("ls -d /tmp/* | grep '\.'| uniq | grep '" + extension + "'", stdout=subprocess.PIPE, shell=True) 
        output, err= p.communicate()
        for archivo in output:
            cuarentena(archivo)
            reportar_alarma("Se encontro un posible script en el directorio /tmp")
            reportar_prevencion("Se movio el posible script a cuarentena desde /tmp")
