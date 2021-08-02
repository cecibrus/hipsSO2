import sys
import psycopg2
from definiciones import BD_CONEXION
sys.path.insert(0, '/root/hips/cron')
from analiza_cron import analizar_crontabs
sys.path.insert(0, '/root/hips/base_de_datos')
from creacion_bd import inicializar_bd
from funciones_bd import obtener_lista_usuario_registro_bd
sys.path.insert(0, '/root/hips/sniffers')
from sniffers import promisc
sys.path.insert(0, '/root/hips/verificar_tmp')
from verificar_tmp import tmp
sys.path.insert(0, '/root/hips/correo')
from correo import funciones_correo
sys.path.insert(0, '/root/hips/modificacion_archivos')
from modificacion_archivos import hash
sys.path.insert(0, '/root/hips/usuario')
from usuarios_conectados import analizar_usuarios_conectados
sys.path.insert(0, '/root/hips/logs')
from analiza_log import analiza_login_su_messages,analiza_tcpdump,analiza_maillog,analiza_smtp_secure, analiza_smtp_messages
sys.path.insert(0, '/root/hips/proceso')
from analiza_procesos import analiza_proceso


# Creacion de BD
inicializar_bd()
analizar_crontabs()
promisc.analizar_sniffers()
tmp.analisis_tmp()
funciones_correo.verificar_cola()
hash.analisis_hash()
# Logs
analizar_usuarios_conectados()
analiza_login_su_messages()
analiza_proceso()
analiza_tcpdump()
analiza_maillog()
analiza_smtp_secure()
analiza_smtp_messages()







#inicializar_bd()

