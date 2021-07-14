from reportes.reporte_alarmas_prevencion import reportar_alarma, reportar_prevencion
from usuario.funciones_usuario import cambiar_contrasena, cerrar_sesion, eliminar_usuario
from base_de_datos.funciones_bd import  obtener_lista_usuario_registro
from definiciones import BD_CONEXION
import os 
import subprocess
import psycopg2
from datetime import date, datetime

# Analiza si un usuario conectado es legitimo respentando el dia y horario que le correponde
# En caso de que el usuario no pertenece al sistema
#   - Primero cierra la sesion del usuario
#   - Elimina la credencial del usuario del sistema
# En caso de que el usuario sea legitimo pero se encuentra conectado en un horario o dia que no le corresponde:
#   - Cierra la sesion del usuario
#   - Cambia la contraseña del usuario
def analizar_usuarios_conectados():
    cmd = "who | awk '{print($1,$5,$3,$4)}' | sed 's/(//g' | sed 's/)//g'"                  #Listamos los usuarios conectados actualmente
    p1 = subprocess.Popen(cmd, shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    conectados, err = p1.communicate() 
    lista = conectados.split('\n')
    lista_usuario_bd = obtener_lista_usuario_registro()                                     #Obtenemos la lista de los usuarios legitimos del sistema

    for linea in lista:                                                                     #Recorremos la lista de los usuarios conectados
        usuario_valido = 0
        ip_valido = 0
        hora_valido = 0
        dia_valido = 0
        usuario_conectado = linea.split(' ')  

        for usuario_valido in lista_usuario_bd:                                             #Recorremos la lista de los usuarios legitimos
            if usuario_conectado[0] == usuario_valido[0]:                                   #El usuario es valido
                print('\nMismo nombre de usuario')
                u_valido=1
                if usuario_conectado[1]==usuario_valido[1] or (usuario_conectado[1]=='' and usuario_valido[1]=='localhost'):        #el ip es valido
                    ip_valido=1                                                             #El ip es valido
                    print('\nMismo ip de usuario')
                if ip_valido and u_valido:                      
                    fecha = datetime.strptime(usuario_conectado[2], '%Y-%m-%d')
                    dia_semana = datetime.weekday(fecha)
                    dias_permitidos = usuario_valido[2].split('-')
                    print(dias_permitidos)
                    for dia in dias_permitidos:
                        if str(dia_semana) == dia:                                          #Se encuetra dentro de los dias permitidos
                            print('\nMismo dia')
                            dia_valido = 1 
                            horas = usuario_valido[3].split('-')
                            hora_inic = datetime.strptime(horas[0], '%H:%M')
                            
                            hora_fin = datetime.strptime(horas[1],'%H:%M' )
                            if hora_inic <= datetime.strptime(usuario_conectado[3], '%H:%M') <= hora_fin: 
                                hora_valido = 1
                                print('\nMismo horario')                                    #Se encuentra en el rango horario habilitado
                                break
        if usuario_valido == 0 :                                                            #No es un usuario legitimo
            cerrar_sesion(usuario_conectado[0])                                             #Cerramos la sesion del usuario
            eliminar_usuario(usuario_conectado[0])                                          #Eliminamos al usuario del sistea
            mensaje = "El usuario " + "'" + usuario_conectado[0] + "'" + "no pertenece al sistema"
            reportar_alarma("Intruso en el sistema (usuario clandestino)", usuario_conectado[1])
            reportar_prevencion("Intruso en el sistema (usuario clandestino)", "Cierre de sesion y usuario eliminado del sistema", usuario_conectado[1])

        else:
            if ip_valido == False or dia_valido == False or hora_valido == False:
                cerrar_sesion(usuario_conectado[0])
                cambiar_contrasena(usuario_conectado[0])
                mensaje = "El usuario " + "'" + usuario_conectado[0] + "'" + "no pertenece al sistema"
                reportar_alarma("Intruso en el sistema (usuario clandestino)", usuario_conectado[1])
                reportar_prevencion("Intruso en el sistema (posible usuario fraudulento o suplantador)", "Cierre de sesion y cambio de contraseña del usuario", usuario_conectado[1])
        
