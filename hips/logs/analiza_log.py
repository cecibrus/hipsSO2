#Examinar los archivos log: Se deben buscar patrones de acceso indebidos en las
#bitácoras del sistema. A partir de lo detectado, deberán:
#   - bloquear IPs
#   - cambiar contraseña de usuario o directamente bloquear un usuario,
#   - bajar temporalmente el servicio de correo.
#   1. Failed Password y Authentication Failure en el /var/log /secure y /var/log/messages
#   2. Errores de carga de páginas desde un mismo IP, como se estuvieren
#   buscando un sitio desconocido. /var/log/httpd/access.log
#   3. Envío de mails masivos desde una misma cuenta, se puede verificar la
#   cola de mails, así como el registro del mail /var/log/maillog
#   4. Entre otros...
import sys
from funciones_bd import add_lista_negra_correo, obtener_lista_negra_correo

from funciones_usuario import bloquear_ip, bloquear_usuario, cambiar_contrasena, encontrar_ip
from reporte_alarmas_prevencion import reportar_alarma, reportar_prevencion
sys.path.insert(0, '/root/hips')
from definiciones import IP_LOCAL, MAX_ACCES_LOG, MAX_CORREOS_POR_DIA, MAX_DNS_COUNT, MAX_INTENTOS_LOGIN, MAX_INTENTOS_LOGIN_SMTP, MAX_INTENTOS_LOGIN_SSHD, MAX_INTENTOS_LOGIN_SU, MAX_INTENTOS_SMTP, MINIMAX_INTENTOS_LOGIN, MINIMAX_INTENTOS_SMTP
sys.path.insert(0, '/root/hips/correo')
from funciones_correo import reject, reject_email
import subprocess

# SU
def analiza_login_su_messages():
    p1 = subprocess.Popen("cat /var/log/messages | grep 'FAILED SU' | awk '{print($10,$9)}'  | grep -v  |sed 's/(//g' | sed 's/)//g' | sort | uniq -c", stdout=subprocess.PIPE,  universal_newlines=True, shell=True)
    lista, err = p1.communicate()
    lista = lista.spit('\n')
    for linea in lista:
        linea = linea.split(' ')
        contador = linea[0]
        from_user = linea[1]
        to_user = linea[2]
        extra = ""
        if contador == MAX_INTENTOS_LOGIN_SU:              
            # Alcanzo el limite de intentos
            # Alarma
            ip = encontrar_ip(from_user)
            alarma = "SU. FAILED SU. El ingreso a la sesión del usuario " + str(to_user) + " ha alcanzado el valor máximo de intentos."                
            # Prevencion
            bloquear_usuario(to_user)
            prev_situacion = "SU. FAILED SU. El ingreso a la sesión del usuario " + str(to_user) + " ha alcanzado el valor máximo de intentos."
            prev_decision = "La cuenta del usuario: " + to_user + " ha sido bloqueada."
            if contador > MAX_INTENTOS_LOGIN_SU:
                cambiar_contrasena(to_user)
                prev_situacion = "SU. FAILED SU. El ingreso a la sesión del usuario " + str(to_user) + " superó el valor máximo de intentos."
                if(ip != [] and ip != IP_LOCAL):
                    bloquear_ip(ip)
                    extra = "Dirección de IP bloqueada"
                prev_decision =prev_decision + ". " + extra
                alarma = "SU. FAILED SU. El ingreso a la sesión del usuario " + str(to_user) + " ha superado el valor máximo de intentos."
              
            reportar_alarma(alarma, ip)
            reportar_prevencion(prev_situacion, prev_decision, ip)


def analiza_login_su_secure():
    p1 = subprocess.Popen("cat /var/log/secure | grep 'su' | grep 'authentication failure' | awk '{print($13, $15)}' | sort | uniq -c", stdout=subprocess.PIPE,  universal_newlines=True, shell=True)
    lista, err = p1.communicate()
    lista = lista.spit('\n')

    for linea in lista:
        linea = linea.split(' ')
        contador = linea[0]
        from_user = linea[1]
        aux = linea[2]
        to_user = aux.split('=')[1]
        extra = ""
        if contador == MAX_INTENTOS_LOGIN_SU:              
            # Alcanzo el limite de intentos
            # Alarma
            ip = encontrar_ip(from_user)
            alarma = "SU. Authentication failure. El ingreso a la sesión del usuario " + str(to_user) + " ha alcanzado el valor máximo de intentos."    
           # Prevencion
            bloquear_usuario(to_user)
            prev_situacion = "SU. Authentication failure. El ingreso a la sesión del usuario " + str(to_user) + " ha alcanzado el valor máximo de intentos."
            prev_decision = "La cuenta del usuario: " + to_user + " ha sido bloqueada."
            if contador > MAX_INTENTOS_LOGIN_SU:
                cambiar_contrasena(to_user)
                prev_situacion = "SU. Authentication failure. El ingreso a la sesión del usuario " + str(to_user) + " superó el valor máximo de intentos."
                if(ip != [] and ip != IP_LOCAL):
                    bloquear_ip(ip)
                    extra = "Dirección de IP bloqueada"
                prev_decision =prev_decision + ". " + extra
                alarma = "SU. Authentication failure. El ingreso a la sesión del usuario " + str(to_user) + " ha superado el valor máximo de intentos."                
            reportar_alarma(alarma, ip)
            reportar_prevencion(prev_situacion, prev_decision, ip)




# SSHD
def analiza_login_sshd_secure():
    p1 = subprocess.Popen("cat /var/log/secure |  grep 'Failed password' | grep -v 'invalid' | grep 'sshd' | awk '{print($9,$11)}' | grep -v "+IP_LOCAL+" | sort | uniq -c", stdout=subprocess.PIPE,  universal_newlines=True, shell=True)
    lista, err = p1.communicate()
    lista = lista.spit('\n')
    for linea in lista:
        linea = linea.split(' ')
        contador = linea[0]
        from_usuario = linea[1]
        ip_usuario = linea[2]
        extra = ""
        if contador == MAX_INTENTOS_LOGIN_SSHD:
            #alcanzo el limite de intentos
            # Alarma
            alarma = "SSHD. Failed password. El ingreso a la sesión del usuario " + str(from_usuario) + " ha alcanzado el valor máximo de intentos."
            # Prevencion
            bloquear_usuario(from_usuario)
            prev_situacion = "SSHD. Failed password'. El ingreso a la sesión del usuario " + str(from_usuario) + " ha alcanzado el valor máximo de intentos."
            prev_decision = "La cuenta del usuario: " + from_usuario + " ha sido bloqueada."
            if contador > MAX_INTENTOS_LOGIN_SSHD:
                cambiar_contrasena(from_usuario)
                prev_situacion = "SSHD. Failed password. El ingreso a la sesión del usuario " + str(from_usuario) + " superó el valor máximo de intentos."
                if(ip_usuario != [] and ip_usuario != IP_LOCAL):
                    bloquear_ip(ip_usuario)
                    extra = "Dirección de IP bloqueada"
                prev_decision = prev_decision + ". " + extra
                alarma = "SSHD. Failed password. El ingreso a la sesión del usuario " + str(from_usuario) + " ha superado el valor máximo de intentos."
            reportar_alarma(alarma, ip_usuario)
            reportar_prevencion(prev_situacion, prev_decision, ip_usuario)




# SMTP
def analiza_smtp_secure():
    p1 = subprocess.Popen("cat /var/log/secure | grep 'smtp:auth' | grep 'authentication failure' | awk '{print($13 ,$15)}' | sort | uniq -c", stdout=subprocess.PIPE,  universal_newlines=True, shell=True)
    lista, err = p1.communicate()
    lista = lista.spit('\n')
    for linea in lista:
        linea = linea.split(' ')
        contador = linea[0]
        usuario = linea[1]
        extra = ""
        ip = []
        if contador[usuario] == MAX_INTENTOS_LOGIN_SMTP:              
        # Alcanzo el limite de intentos
        # Alarma
            ip = encontrar_ip(usuario)
            alarma = "Ataque SMTP. Authenticacion failure. El ingreso a la sesión del usuario " + str(usuario) + " ha alcanzado el valor máximo de intentos."
            # Prevencion
            bloquear_usuario(usuario)
            prev_situacion = "Ataque SMTP. Authenticacion failure. El ingreso a la sesión del usuario " + str(usuario) + " ha alcanzado el valor máximo de intentos."
            prev_decision = "La cuenta del usuario: " + usuario + " ha sido bloqueada."
            if contador == MAX_INTENTOS_SMTP:
                cambiar_contrasena(usuario)
                prev_situacion = "Ataque SMTP. Authenticacion failure. El ingreso a la sesión del usuario " + str(usuario) + " superó el valor máximo de intentos."
                if(ip != []):
                    bloquear_ip(ip)
                    extra = "Dirección de IP bloqueada"
                prev_decision = prev_decision + ". " + extra
                alarma = "Ataque SMTP. Authenticacion failure. El ingreso a la sesión del usuario " + str(usuario) + " ha superado el valor máximo de intentos."
            reportar_alarma(alarma, ip)
            reportar_prevencion(prev_situacion, prev_decision, ip)
   

def analiza_smtp_messages():
    #p1 = subprocess.Popen("cat /var/log/messages | grep 'auth failure' | grep 'service=smtp' | awk '{print($10)}' | sed 's/\[//g' | sed 's/\]//g' | sed 's/user=//g' | sort | uniq -c", stdout=subprocess.PIPE,  universal_newlines=True, shell=True)
    p1 = subprocess.Popen("cat smtp_messages.txt | grep 'auth failure' | grep 'service=smtp' | awk '{print($10)}' | sed 's/\[//g' | sed 's/\]//g' | sed 's/user=//g' | sort | uniq -c", stdout=subprocess.PIPE,  universal_newlines=True, shell=True)
    lista, err = p1.communicate()
    lista = lista.spit('\n')
    for linea in lista:
        linea = linea.split(' ')
        contador = linea[0]
        usuario = linea[1]      
        extra = ""
        ip = []
        if contador == MAX_INTENTOS_LOGIN_SMTP:              
            # Alcanzo el limite de intentos
            # Alarma
            ip = encontrar_ip(usuario)
            alarma = "Ataque SMTP. Auth failure El ingreso a la sesión del usuario " + str(usuario) + " ha alcanzado el valor máximo de intentos."
            # Prevencion
            bloquear_usuario(usuario)
            situacion = "Posible Ataque SMTP"
            decision = "Ingreso bloqueado al usuario " + usuario
            reportar_prevencion(situacion, decision, ip)
            if contador > MAX_INTENTOS_LOGIN_SMTP:
                cambiar_contrasena(usuario)
                prev_situacion = "Ataque SMTP. Auth failure. El ingreso a la sesión del usuario " + str(usuario) + " superó el valor máximo de intentos."
                if(ip != []):
                    bloquear_ip(ip)
                    extra = "Dirección de IP bloqueada"
                prev_decision = prev_decision + ". " + extra
                alarma = "Ataque SMTP. Auth failure. El ingreso a la sesión del usuario " + str(usuario) + " ha superado el valor máximo de intentos."
            reportar_alarma(alarma, ip)
            reportar_prevencion(prev_situacion, prev_decision, ip)
     




# LOG ACCESS
def analiza_access_log():
    #p1 = subprocess.Popen("cat /var/log/httpd/access.log | grep '404' |  grep -v "+IP_LOCAL+" | awk '{print($1)}' | sort | uniq -c", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    p1 = subprocess.Popen(" cat acces_log.txt | grep '404' |  grep -v "+IP_LOCAL+" | awk '{print($1)}' | sort | uniq -c", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    (lista, err) = p1.communicate()
    lista = lista.split('\n')
    for elemento in lista:
        elemento = elemento.split(' ')
        if elemento[0] > MAX_ACCES_LOG:
            bloquear_ip(elemento[1])
            reportar_alarma('Errores 404 repetitivos desde una misma ip', elemento[1])
            reportar_prevencion('Errores 404 repetitivos dessde una misma ip', 'Bloqueo de ip', elemento[1])




#MAILLOG	
def analiza_maillog():
    p1 = subprocess.Popen(" sudo cat maillog.txt | grep 'from=' | grep '@' | awk '{print($7)}' | sed 's/from=//g' | sed 's/<//g' | sed 's/>,//g' | sort | uniq -c", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    (lista, err) = p1.communicate()
    lista = lista.split('\n')
    for aux in lista:
        ban = 0
        elemento = aux.split(' ')
        intentos = elemento[0]
        from_correo = elemento[1]
        if intentos > MAX_CORREOS_POR_DIA:
            reportar_alarma('Spam de correos. Exceso de envío de correos por día', from_correo)
            lista_negra = obtener_lista_negra_correo()
            for mail in lista_negra:
                if from_correo == mail:
                    reject_email(from_correo)
                    prev_decision = prev_decision + " La cuenta de correo ya se encuentra en la lista negra, por lo que se rechaza sus proximos envios de correos "
                    ban = 1
            if ban != 1: 
                add_lista_negra_correo(from_correo)
                prev_decision = "Se agrego la cuenta de correo a la lista negra."
            reportar_prevencion('Spam de correo. Exceso de envío de correos por día', prev_decision, from_correo)



# TCPDUMP
def analiza_tcpdump():
    p1 = subprocess.Popen(" sudo cat tcpdump.txt | grep 'Flags' |awk '{print $3}'  | sed 's/\./ /g' | awk '{print $1,$2,$3,$4}' | sed 's/ /\./g' | sort| uniq -c", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    (lista, err) = p1.communicate()
    lista = lista.split('\n')
    for elemento in lista:
        if elemento[0] > MAX_DNS_COUNT:
            ip = elemento[1]
            reportar_alarma("Ataque DNS. Sobrecarga al servidor", ip)
            
            aux = "sudo cat tcpdump.txt | grep 'Flags' | grep " + ip + " | awk '{print $5}' | sed 's/\./ /g' | awk '{print $1,$2,$3,$4}' | sed 's/ /\./g'"
            p2 = subprocess.Popen(aux, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
            (ips, err) = p2.communicate()
            ips = ips.split('\n')
            for ip_individual in ips:
                bloquear_ip(ip_individual)
                situacion = "Ataque DNS. Sobrecarga al servidor: " + ip
                decision = "Se bloqueo a la ip: " + ip_individual
                reportar_prevencion(situacion, decision, ip  )


       







