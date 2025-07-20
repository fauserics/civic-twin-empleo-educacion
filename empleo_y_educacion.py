import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ─── Configuración de Página ───────────────────────────────────────────
st.set_page_config(
    page_title="Civic Twin™: Empleo y Educación Tecnológica",
    layout="wide",
    menu_items={"Get help": None, "Report a bug": None, "About": None}
)

# ─── CSS Global para eliminar espacio extra y ajustar banner ────────────
st.markdown(
    """
    <style>
      /* Eliminar padding superior del contenedor */
      .block-container {
        padding-top: 0rem;
        padding-bottom: 1rem;
      }
      /* Reducir margen debajo del encabezado */
      .banner {
        margin-bottom: 0.5rem !important;
      }
      /* Ajustar cabecera fija */
      header {
        top: 0;
      }
    </style>
    """, unsafe_allow_html=True
)

# ─── Banner con Logo y Título ──────────────────────────────────────────
st.markdown(
    """
    <div class='banner' style='background-color:#f0f8ff; padding:0.5rem 1rem; display:flex; align-items:center;'>
      <img src='https://your-civic-twin-logo-url/logo.svg' style='height:40px; margin-right:0.5rem;' alt='Civic Twin™ Logo'/>
      <h2 style='margin:0; color:#004080;'>Civic Twin™ Dashboard: Empleo y Educación</h2>
    </div>
    """, unsafe_allow_html=True
)

# ─── Paleta de color azul uniforme ────────────────────────────────────
BLUE_SCALE = px.colors.sequential.Blues

# ─── Carga de Datos (cacheada) ────────────────────────────────────────
@st.cache_data
def cargar_datos():
    base = Path(__file__).parent
    return {
        'empleo': pd.read_csv(base / 'empleo_tecnologico_por_provincia.csv'),
        'profesiones': pd.read_csv(base / 'demanda_profesiones_tecnologicas.csv'),
        'oferta_vs_demanda': pd.read_csv(base / 'oferta_vs_demanda_tecnologica.csv'),
        'genero': pd.read_csv(base / 'participacion_genero_tecnologia.csv'),
        'edad': pd.read_csv(base / 'edad_promedio_roles_tecnologicos.csv'),
        'educacion': pd.read_csv(base / 'nivel_educativo_trabajadores_tecnologia.csv'),
        'ia': pd.read_csv(base / 'impacto_ia_roles_tecnologicos.csv')
    }

datos = cargar_datos()

# ─── Crear Pestañas Principales ───────────────────────────────────────
tabs = st.tabs([
    "📍 Empleo por Provincia",
    "💼 Profesiones Demandadas",
    "📚 Oferta vs Demanda",
    "👥 Diversidad",
    "🤖 Impacto IA"
])

# Altura fija para minimizar scroll
CHART_HEIGHT = 380

# 1) Empleo por Provincia
with tabs[0]:
    fig = px.bar(
        datos['empleo'],
        x='Provincia',
        y='Empleos_tecnologicos',
        labels={'Empleos_tecnologicos': 'Empleos (%)'},
        color='Empleos_tecnologicos',
        color_continuous_scale=BLUE_SCALE
    )
    st.plotly_chart(fig, use_container_width=True, height=CHART_HEIGHT)

# 2) Profesiones más Demandadas
with tabs[1]:
    fig = px.bar(
        datos['profesiones'],
        x='Porcentaje_demandado',
        y='Profesion',
        orientation='h',
        labels={'Porcentaje_demandado': 'Demanda (%)'},
        color='Porcentaje_demandado',
        color_continuous_scale=BLUE_SCALE
    )
    st.plotly_chart(fig, use_container_width=True, height=CHART_HEIGHT)

# 3) Oferta vs Demanda Educativa
with tabs[2]:
    df = datos['oferta_vs_demanda'].melt(
        id_vars='Especialidad',
        value_vars=['Egresados_anuales', 'Puestos_demandados'],
        var_name='Tipo',
        value_name='Cantidad'
    )
    fig = px.bar(
        df,
        x='Especialidad',
        y='Cantidad',
        color='Tipo',
        barmode='group',
        color_discrete_sequence=BLUE_SCALE,
        labels={'Cantidad': 'Personas'}
    )
    st.plotly_chart(fig, use_container_width=True, height=CHART_HEIGHT)

# 4) Diversidad (pestañas internas)
with tabs[3]:
    sub_tabs = st.tabs(["Género", "Edad", "Educación"])
    with sub_tabs[0]:
        df_g = datos['genero'].melt(
            id_vars='Categoria', var_name='Tipo', value_name='Porcentaje'
        )
        fig = px.bar(
            df_g,
            x='Categoria',
            y='Porcentaje',
            color='Tipo',
            barmode='group',
            color_discrete_sequence=BLUE_SCALE
        )
        st.plotly_chart(fig, use_container_width=True, height=CHART_HEIGHT)
    with sub_tabs[1]:
        fig = px.bar(
            datos['edad'],
            x='Rol',
            y='Edad_promedio',
            labels={'Edad_promedio': 'Edad (años)'},
            color_discrete_sequence=BLUE_SCALE
        )
        st.plotly_chart(fig, use_container_width=True, height=CHART_HEIGHT)
    with sub_tabs[2]:
        fig = px.pie(
            datos['educacion'],
            names='Nivel_educativo',
            values='Porcentaje',
            color_discrete_sequence=BLUE_SCALE,
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True, height=CHART_HEIGHT)

# 5) Impacto de la IA
with tabs[4]:
    fig = px.scatter(
        datos['ia'],
        x='Exposicion_IA',
        y='Complementariedad_IA',
        size='Riesgo_desplazamiento',
        color='Rol_tecnologico',
        size_max=50,
        color_discrete_sequence=BLUE_SCALE,
        labels={
            'Exposicion_IA': 'Exposición a IA',
            'Complementariedad_IA': 'Complementariedad con IA'
        }
    )
    st.plotly_chart(fig, use_container_width=True, height=CHART_HEIGHT)
    st.markdown(
        """
        **Interpretación rápida:**
        - 🟥 Alta exposición + baja complementariedad = mayor riesgo.
        - 🟩 Alta complementariedad = gran oportunidad de colaboración con IA.
        """
    )

# ─── Footer ──────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Civic Twin © 2025 · Datos: Ministerio de Trabajo, Educación, INDEC, CESSI, Observatorios.")
