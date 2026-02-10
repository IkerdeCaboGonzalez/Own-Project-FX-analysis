import requests
import psycopg2
import urllib3
import ssl

# Configuración de seguridad (si no no permite acceder a la API)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Configuración de la base de datos

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "IK008626"
}

# Función para extraer y cargar losd atos en la base de datos local

def cargar_datos(fecha_inicio, fecha_fin):
    conn = None
    try:
        # URL de la API con rango de fechas
        url = f"http://api.frankfurter.app/{fecha_inicio}..{fecha_fin}"
        respuesta = requests.get(url, verify=False, timeout=15)

        # Verificamos que la respuesta sea correcta (status_code=200 significa que recibió los datos sin problemas)

        if respuesta.status_code == 200:
            datos_completos = respuesta.json()
            cambios = datos_completos.get("rates", {})
            
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()

            # Lista de todas las divisas disponibles
            lista_divisas = sorted(cambios[list(cambios.keys())[0]].keys())

            # Creamos la tabla si no existe

            columnas_tabla = ", ".join([f"{divisa} FLOAT" for divisa in lista_divisas])
            cur.execute(f"CREATE TABLE IF NOT EXISTS divisas (fecha DATE PRIMARY KEY, {columnas_tabla});")

            # Insertamos los datos
            for fecha, valores in cambios.items():
                
                # Definimos las columnas y sus nombres
                placeholders = ", ".join(["%s"] * (len(lista_divisas) + 1))
                nombres_cols = ", ".join(["fecha"] + lista_divisas)
                
                # Lista con los valores a insertar
                lista_valores = [fecha] + [valores.get(divisa) for divisa in lista_divisas]
                
                # En caso de conflicto, actualizamos los valores
                update_set = ", ".join([f"{divisa} = EXCLUDED.{divisa}" for divisa in lista_divisas])

                # Query de inserción
                query = f"INSERT INTO divisas ({nombres_cols}) VALUES ({placeholders}) ON CONFLICT (fecha) DO UPDATE SET {update_set};"
                cur.execute(query, lista_valores)

            conn.commit()

    except Exception as e:
        print("Error al cargar datos:", e)

    # Esto asegura que siempre se cierra la conexión con la base de datos
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    cargar_datos("2024-01-01", "2024-02-28")