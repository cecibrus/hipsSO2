import sys
sys.path.insert(0, '/root/hips/cron')
from analiza_cron import analizar_crontabs
sys.path.insert(0, '/root/hips/base_de_datos')
from base_de_datos import creacion_bd

inicializar_bd()
analizar_crontabs()
