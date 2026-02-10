import psycopg2
import matplotlib.pyplot as plt

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

#for fila in filas:
#    print(fila)

print(filas[0])  # Imprimir la primera fila como ejemplo

cur.close()
conn.close()

# Visualización de los datos

fechas = [fila[0] for fila in filas]
divisas = [fila[1:] for fila in filas]

plt.plot(fechas, divisas)


