import streamlit as st
import pandas as pd
from modules import cargar_datos, metricas_volatilidad

# Configuración de la base de datos (Consistente con tu Dockerfile)
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "IK008626"
}

st.set_page_config(page_title="Análisis Divisas", layout="wide")

st.title("Análisis del valor de las divisas respecto al Euro")

# 1. Carga inicial de datos para conocer el rango disponible

@st.cache_data
def obtener_todo(config):
    return cargar_datos(config)

df_total = obtener_todo(DB_CONFIG)

# 2. Barra lateral para filtros
st.sidebar.header("Filtros de Análisis")

# Filtro de Fechas
fecha_min = pd.to_datetime(df_total['fecha'].min())
fecha_max = pd.to_datetime(df_total['fecha'].max())

rango_fechas = st.sidebar.date_input(
    "Selecciona el rango de fechas:",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

# Filtro de Divisas
todas_las_divisas = [col for col in df_total.columns if col != 'fecha']
divisas_seleccionadas = st.sidebar.multiselect(
    "Selecciona las divisas a analizar:",
    options=todas_las_divisas,
    default=["usd", "gbp", "jpy", "chf"]
)

# 3. Procesamiento de datos filtrados
if len(rango_fechas) == 2:
    inicio, fin = rango_fechas
    # Filtrar por fecha y divisa
    mask = (df_total['fecha'] >= inicio) & (df_total['fecha'] <= fin)
    df_filtrado = df_total.loc[mask, ['fecha'] + divisas_seleccionadas]

    if not df_filtrado.empty:
        # Calcular métricas con tu función de modules.py
        # Nota: Asegúrate de que tu función filtre tipos numéricos internamente
        std, std_norm, rendimiento, matriz_correlacion = metricas_volatilidad(df_filtrado)

        # 4. Visualización de Tablas
        st.subheader(f"Resultados del periodo: {inicio} a {fin}")
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.dataframe(std.rename("Volatilidad").sort_values(ascending=False), use_container_width=True)
        with col2:
            st.dataframe(std_norm.rename("Volatilidad Relativa").sort_values(ascending=False), use_container_width=True)
        with col3:
            st.dataframe(rendimiento.rename("Rendimiento Total %").sort_values(ascending=False), use_container_width=True)
        with col4:
            st.dataframe(matriz_correlacion.rename("Matriz de Correlación"), use_container_width=True)

        # 5. Gráfico de apoyo
        st.divider()
        st.subheader("Evolución Temporal")
        st.line_chart(df_filtrado.set_index('fecha'))
    else:
        st.warning("No hay datos para el rango seleccionado.")
else:
    st.info("Por favor, selecciona un rango de fechas completo (inicio y fin).")