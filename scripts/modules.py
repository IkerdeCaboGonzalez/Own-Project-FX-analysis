import requests
import psycopg2
import pandas as pd
import numpy as np

# Función para extraer los datos desde la API y cargarlos en la base de datos

def importar_datos(fecha_inicio, fecha_fin, DB_CONFIG):
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
                
                # En caso de conflicto, actualizamos los valores. Nos permite lanzar el script de carga sin problemas. Simplemente se actualiza si hay nuevos datos.
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


# Función para cargar los datos desde la base de datos a un script.

def cargar_datos(DB_CONFIG):
    conn = None
    try:
        # Creamos la conexión
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Traemos todos los datos de la tabla
        cur.execute("SELECT * FROM divisas;")

        # Extraemos todas las filas y los nombres de las columnas para crear un DataFrame
        filas = cur.fetchall()
        nombres_columnas = [desc[0] for desc in cur.description]
        df = pd.DataFrame(filas, columns=nombres_columnas)

    except Exception as e:
        print("Error al cargar datos:", e)
    
    finally:
        if conn:
            conn.close()
    return df

# Función para calcular métricas de volatilidad acerca de las divisas

def metricas_volatilidad(df):

    fecha = df["fecha"]
    divisas = df.drop(columns=["fecha"])

    desviacion_estandar = divisas.std()
    desviacion_estandar_normalizada = divisas.std()/divisas.mean()
    rendimiento = (divisas.iloc[0]-divisas.iloc[-1])/divisas.iloc[-1] 
    returns = np.log(divisas / divisas.shift(1)).dropna()
    #var_diario = returns.quantile(1-0.95)

    return desviacion_estandar, desviacion_estandar_normalizada, rendimiento, returns # , var_diario







