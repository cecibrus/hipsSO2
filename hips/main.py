import sys
sys.path.insert(0, '/root/hips/cron')
from analiza_cron import analizar_crontabs
sys.path.insert(0, '/root/hips/base_de_datos')
from base_de_datos import creacion_bd
sys.path.insert(0, '/root/hips/sniffers')
from sniffers import promisc
sys.path.insert(0, '/root/hips/verificar_tmp')
from verificar_tmp import tmp
sys.path.insert(0, '/root/hips/correo')
from correo import funciones_correo
sys.path.insert(0, '/root/hips/modificacion_archivos')
from modificacion_archivos import hash

inicializar_bd()
analizar_crontabs()
promisc.analizar_sniffers()
tmp.analisis_tmp()
funciones_correo.verificar_cola()
hash.analisis_hash()

