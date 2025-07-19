import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración general del tablero
st.set_page_config(page_title='Civic Twin: Empleo y Educación Tecnológica en Argentina', layout='wide')

# Título del tablero
st.title("📊 Civic Twin: Empleo, Educación y Futuro del Trabajo Tecnológico en Argentina")

# Carga de datos
@st.cache_data
def cargar_datos():
    df_empleo = pd.read_csv('data/empleo_tecnologico_por_provincia.csv')
    df_profesiones = pd.read_csv('data/demanda_profesiones_tecnologicas.csv')
    return df_empleo, df_profesiones

df_empleo, df_profesiones = cargar_datos()

# Sección 1: Demanda laboral tecnológica por provincia
st.subheader("Distribución del Empleo Tecnológico por Provincia (2023)")

fig_empleo = px.bar(
    df_empleo, 
    x='Provincia', 
    y='Empleos_tecnologicos',
    labels={'Empleos_tecnologicos': 'Porcentaje de empleos (%)'},
    color='Empleos_tecnologicos',
    color_continuous_scale='blues'
)

st.plotly_chart(fig_empleo, use_container_width=True)

# Sección 2: Demanda laboral por tipo de profesión tecnológica
st.subheader("Demanda Laboral por Profesión Tecnológica (2024)")

fig_profesiones = px.bar(
    df_profesiones,
    x='Porcentaje_demandado',
    y='Profesion',
    orientation='h',
    labels={'Porcentaje_demandado': 'Porcentaje de demanda (%)'},
    color='Porcentaje_demandado',
    color_continuous_scale='greens'
)

st.plotly_chart(fig_profesiones, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Civic Twin © 2025 | Datos reales provenientes del Ministerio de Trabajo, Educación, INDEC y CESSI.")
