import urllib3
import ssl
from datetime import datetime

from modules import importar_datos, cargar_datos, metricas_volatilidad

# Configuración de seguridad (si no no permite acceder a la API)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Configuración de la base de datos

DB_CONFIG = {
    "host": "db",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "IK008626"
}

today = datetime.today().strftime('%Y-%m-%d')

importar_datos("2000-01-01", today, DB_CONFIG)

data = cargar_datos(DB_CONFIG)

print(data.head())


desviacion_estandar, desviacion_estandar_normalizada, rendimiento, returns = metricas_volatilidad(data)


print("Desviación Estándar:")
print(desviacion_estandar)

print("Desviación Estándar Normalizada:")
print(desviacion_estandar_normalizada)

print("Rendimiento:")
print(rendimiento)

print("Returns:")
print(returns)
