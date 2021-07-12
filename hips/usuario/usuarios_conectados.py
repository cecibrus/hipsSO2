from usuario.funciones_usuario import cambiar_contrasena, cerrar_sesion, eliminar_usuario
from base_de_datos.funciones_bd import  obtener_lista_usuario_registro
from base_de_datos.definiciones import BD_CONEXION
import os 
import subprocess
import psycopg2
from datetime import date, datetime


def analizar_usuarios_conectados():
    cmd = "who | awk '{print($1,$5,$3,$4)}' | sed 's/(//g' | sed 's/)//g'"
    p1 = subprocess.Popen(cmd, shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    conectados, err = p1.communicate() 
    lista = conectados.split('\n')
    lista_usuario_bd = obtener_lista_usuario_registro()

    for linea in lista:
        usuario_valido = False
        ip_valido = False
        hora_valido = False
        dia_valido = False
        usuario_conectado = linea.split(' ')  
        for usuario_valido in lista_usuario_bd:  
            if usuario_conectado[0] == usuario_valido[0]:         #el usuario es valido
                print('\nMismo nombre de usuario')
                u_valido=True
                if usuario_conectado[1]==usuario_valido[1] or (usuario_conectado[1]=='' and usuario_valido[1]=='localhost'):        #el ip es valido
                    ip_valido=True
                    print('\nMismo ip de usuario')
                
                if ip_valido and u_valido:                      
                    fecha = datetime.strptime(usuario_conectado[2], '%Y-%m-%d')
                    dia_semana = datetime.weekday(fecha)
                    dias_permitidos = usuario_valido[2].split('-')
                    print(dias_permitidos)
                    for dia in dias_permitidos:
                        if str(dia_semana) == dia:
                            print('\nMismo dia')
                            dia_valido = True 
                            horas = usuario_valido[3].split('-')
                            hora_inic = datetime.strptime(horas[0], '%H:%M')
                            hora_fin = datetime.strptime(horas[1],'%H:%M' )
                            if hora_inic <= datetime.strptime(usuario_conectado[3], '%H:%M') <= hora_fin: 
                                hora_valido = True
                                print('\nMismo horario')
                                break
        if usuario_valido == False : 
            cerrar_sesion(usuario_conectado[0])
            eliminar_usuario(usuario_conectado[0])
        else:
            if ip_valido == False or dia_valido == False or hora_valido == False:
                cerrar_sesion(usuario_conectado[0])
                cambiar_contrasena(usuario_conectado[0])

        
