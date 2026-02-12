import urllib3
import ssl

from modules import cargar_datos

# Configuración de seguridad (si no no permite acceder a la API)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Configuración de la base de datos


cargar_datos("2020-01-01", "2025-12-31")


