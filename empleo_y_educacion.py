import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ─── Configuración de la página ───────────────────────────────────────
st.set_page_config(
    page_title="Civic Twin™: Empleo y Educación Tecnológica",
    layout="wide",
    menu_items={"Get help": None, "Report a bug": None, "About": None}
)

# ─── CSS y Header de Civic Twin Café ─────────────────────────────────
st.markdown("""
<style>
/* Ocultar menú y footer de Streamlit */
#MainMenu {visibility: hidden;} 
footer {visibility: hidden;}
header {visibility: hidden;}
/* Ajustar márgenes y scroll */
body, .block-container {padding: 0; margin: 0;}
</style>
""", unsafe_allow_html=True)

# Banner con logo de Civic Twin™
st.markdown("""
<div style='display: flex; align-items: center; background-color: #f0f2f6; padding: 10px;'>
  <img src='https://path-to-your-logo.svg' alt='Civic Twin™' style='height:40px; margin-right:10px;'>
  <h2 style='margin: 0;'>Civic Twin™ - Empleo y Educación Tecnológica</h2>
</div>
""", unsafe_allow_html=True)

# Paleta de color azul
BLUE_SCALE = px.colors.sequential.Blues

# Cargar datos
@st.cache_data
def cargar_datos():
    return {
        'empleo': pd.read_csv('empleo_tecnologico_por_provincia.csv'),
        'profesiones': pd.read_csv('demanda_profesiones_tecnologicas.csv'),
        'oferta_vs_demanda': pd.read_csv('oferta_vs_demanda_tecnologica.csv'),
        'genero': pd.read_csv('participacion_genero_tecnologia.csv'),
        'edad': pd.read_csv('edad_promedio_roles_tecnologicos.csv'),
        'educacion': pd.read_csv('nivel_educativo_trabajadores_tecnologia.csv'),
        'ia': pd.read_csv('impacto_ia_roles_tecnologicos.csv')
    }

datos = cargar_datos()

# Pestañas principales
tabs = st.tabs([
    "📍 Empleo por Provincia",
    "💼 Profesiones Demandadas",
    "📚 Oferta vs Demanda",
    "👥 Diversidad",
    "🤖 Impacto IA"
])

# 1) Empleo por Provincia
def mostrar_empleo():
    fig = px.bar(
        datos['empleo'], x='Provincia', y='Empleos_tecnologicos',
        labels={'Empleos_tecnologicos': 'Empleos (%)'},
        color='Empleos_tecnologicos', color_continuous_scale=BLUE_SCALE
    )
    st.plotly_chart(fig, use_container_width=True, height=420)
    st.caption("Fuente: Ministerio de Trabajo, Educación, INDEC y CESSI")

with tabs[0]:
    mostrar_empleo()

# 2) Profesiones más Demandadas
def mostrar_profesiones():
    fig = px.bar(
        datos['profesiones'], x='Porcentaje_demandado', y='Profesion',
        orientation='h', labels={'Porcentaje_demandado': 'Demanda (%)'},
        color='Porcentaje_demandado', color_continuous_scale=BLUE_SCALE
    )
    st.plotly_chart(fig, use_container_width=True, height=420)
    st.caption("Fuente: Portales laborales y informes CESSI")

with tabs[1]:
    mostrar_profesiones()

# 3) Oferta vs Demanda Educativa
def mostrar_oferta_vs_demanda():
    df = datos['oferta_vs_demanda'].melt(
        id_vars='Especialidad',
        value_vars=['Egresados_anuales', 'Puestos_demandados'],
        var_name='Tipo', value_name='Cantidad'
    )
    fig = px.bar(
        df, x='Especialidad', y='Cantidad', color='Tipo', barmode='group',
        color_discrete_sequence=BLUE_SCALE, labels={'Cantidad': 'Personas'}
    )
    st.plotly_chart(fig, use_container_width=True, height=420)
    st.caption("Fuente: Ministerio de Educación e INDEC")

with tabs[2]:
    mostrar_oferta_vs_demanda()

# 4) Diversidad
def mostrar_diversidad():
    sub_tabs = st.tabs(["Género", "Edad", "Educación"])
    with sub_tabs[0]:
        df_g = datos['genero'].melt(id_vars='Categoria', var_name='Tipo', value_name='Porcentaje')
        fig = px.bar(df_g, x='Categoria', y='Porcentaje', color='Tipo', barmode='group', color_discrete_sequence=BLUE_SCALE)
        st.plotly_chart(fig, use_container_width=True, height=420)
        st.caption("Fuente: Chicas en Tecnología y CESSI")
    with sub_tabs[1]:
        fig = px.bar(datos['edad'], x='Rol', y='Edad_promedio', labels={'Edad_promedio': 'Edad (años)'}, color_discrete_sequence=BLUE_SCALE)
        st.plotly_chart(fig, use_container_width=True, height=420)
        st.caption("Fuente: Observatorio del Trabajo Informático")
    with sub_tabs[2]:
        fig = px.pie(datos['educacion'], names='Nivel_educativo', values='Porcentaje', color_discrete_sequence=BLUE_SCALE, hole=0.3)
        st.plotly_chart(fig, use_container_width=True, height=420)
        st.caption("Fuente: Ministerio de Educación")

with tabs[3]:
    mostrar_diversidad()

# 5) Impacto de la IA
def mostrar_ia():
    fig = px.scatter(
        datos['ia'], x='Exposicion_IA', y='Complementariedad_IA', size='Riesgo_desplazamiento',
        color='Rol_tecnologico', size_max=50, color_discrete_sequence=BLUE_SCALE,
        labels={'Exposicion_IA': 'Exposición a IA', 'Complementariedad_IA': 'Complementariedad con IA'}
    )
    st.plotly_chart(fig, use_container_width=True, height=420)
    st.caption("Fuente: Ministerio de Trabajo y BID")

with tabs[4]:
    mostrar_ia()

# Footer general
st.markdown("---")
st.caption("Civic Twin™ © 2025")
