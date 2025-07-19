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
    df_empleo = pd.read_csv('empleo_tecnologico_por_provincia.csv')
    df_profesiones = pd.read_csv('demanda_profesiones_tecnologicas.csv')
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

# Sección 3: Comparación entre oferta educativa y demanda laboral
st.subheader("📚 Brecha entre Oferta Educativa y Demanda Laboral en Tecnología")

# Cargar nuevo dataset
df_oferta_vs_demanda = pd.read_csv('oferta_vs_demanda_tecnologica.csv')

# Crear gráfico de barras agrupadas
fig_brecha = px.bar(
    df_oferta_vs_demanda.melt(id_vars='Especialidad', 
                               value_vars=['Egresados_anuales', 'Puestos_demandados'],
                               var_name='Tipo', value_name='Cantidad'),
    x='Especialidad',
    y='Cantidad',
    color='Tipo',
    barmode='group',
    labels={'Cantidad': 'Cantidad de personas', 'Especialidad': 'Especialidad tecnológica'},
    title='Comparación de Egresados vs Puestos Demandados por Especialidad'
)

st.plotly_chart(fig_brecha, use_container_width=True)


