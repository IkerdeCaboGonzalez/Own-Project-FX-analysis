import psycopg2
import matplotlib.pyplot as plt
import pandas as pd

# Ahora vamos a extraer los datos de la base en local y analizarlos 

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "IK008626"
}

conn = psycopg2.connect(**DB_CONFIG)

cur = conn.cursor()

cur.execute("SELECT * FROM divisas;")

filas = cur.fetchall()

nombre_columnas = [desc[0] for desc in cur.description]



cur.close()
conn.close()

# Visualización de los datos

filas_df = pd.DataFrame(filas, columns=nombre_columnas)


fechas = [fila[0] for fila in filas]
divisas = [fila[1:] for fila in filas]

fechas, divisas = pd.DataFrame(fechas), pd.DataFrame(divisas)

# print(fechas.head())

# print(divisas.head())

print(filas_df.head())

plt.plot(fechas, divisas.iloc[:,0:3])
plt.xlabel("Fecha")
plt.ylabel("Valor de las divisas")
plt.title("Evolución de las divisas a lo largo del tiempo")
plt.legend(nombre_columnas[1:], loc="upper left")
plt.xticks(rotation=45)
plt.show()



