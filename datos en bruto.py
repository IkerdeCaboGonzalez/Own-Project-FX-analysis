import requests
import urllib3
import ssl

# 1. CONFIGURACIÓN DE SEGURIDAD
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

def consultar_divisas_completo(fecha_inicio, fecha_fin):
    url = f"http://api.frankfurter.app/{fecha_inicio}..{fecha_fin}"
    
    try:
        respuesta = requests.get(url, verify=False, timeout=15)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            rates = datos.get('rates', {})
            
            if not rates:
                print("No se encontraron datos.")
                return

            # --- BLOQUE 1: TABLA DE DIVISAS PRINCIPALES ---
            print(f"\n{'='*60}")
            print(f" HISTORIAL DE DIVISAS (Base: 1 EUR)")
            print(f"{'='*60}")
            print(f"{'FECHA':<12} | {'USD':<12} | {'GBP':<12} | {'JPY':<12}")
            print("-" * 60)

            for fecha in sorted(rates.keys()):
                val = rates[fecha]
                usd = val.get('USD', '---')
                gbp = val.get('GBP', '---')
                jpy = val.get('JPY', '---')
                print(f"{fecha:<12} | {usd:<12} | {gbp:<12} | {jpy:<12}")

            # --- BLOQUE 2: LISTA DE TODAS LAS DIVISAS DISPONIBLES ---
            # Extraemos las claves del primer día para saber qué monedas hay
            primera_fecha = sorted(rates.keys())[0]
            todas_las_divisas = sorted(rates[primera_fecha].keys())

            print(f"\n{'='*60}")
            print(f" LISTA COMPLETA DE DIVISAS DISPONIBLES ({len(todas_las_divisas)})")
            print(f"{'='*60}")
            
            # Formateamos la lista en grupos de 8 para que no sea una línea infinita
            for i in range(0, len(todas_las_divisas), 8):
                grupo = todas_las_divisas[i:i+8]
                print("  ".join(f"[{m}]" for m in grupo))
            
            print(f"{'='*60}\n")

        else:
            print(f"Error en la API: {respuesta.status_code}")

    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    # Formato AAAA-MM-DD
    consultar_divisas_completo("2026-02-01", "2026-02-10")