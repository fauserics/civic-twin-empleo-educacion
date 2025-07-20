import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ─── Configuración de Página ─────────────────────────────────────────
st.set_page_config(
    page_title="Civic Twin™: Empleo y Educación Tecnológica",
    layout="wide",
    menu_items={"Get help": None, "Report a bug": None, "About": None}
)

# ─── Ocultar UI por defecto ───────────────────────────────────────────
st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# ─── Globals y Header de Civic Twin Café ─────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
:root{
  --topbar-h: 42px;
  --header-h: 70px;
  --azul: #1F4E79;
}
.header-bar{
  position: fixed; top: var(--topbar-h); left: 0; width: 100%; height: var(--header-h);
  background: linear-gradient(90deg,#14406b 0%,var(--azul)100%);
  display: flex; align-items: center; padding: 0 16px; z-index: 100;
}
.header-left{ display: flex; align-items: center; }
.header-center{ flex: 1; text-align: center; font: 700 24px 'Montserrat',sans-serif; color: #fff; }
.header-flag{ height: 32px; border-radius: 3px; }
/* Ajuste de contenido bajo header y sin scroll */
html, body, [data-testid="stAppViewContainer"]{ height:100vh !important; overflow:hidden !important; }
div.block-container, section[data-testid="stSidebar"]{ margin-top: calc(var(--topbar-h) + var(--header-h)) !important; padding-top: 0 !important; height: calc(100vh - var(--topbar-h) - var(--header-h)); overflow: hidden; display: flex; flex-direction: column; }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# SVG Logo y Header HTML
FLAG_AR = "https://flagcdn.com/w40/ar.png"
SVG_LOGO = """
<svg width="32" height="32" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle;margin-right:8px">
  <circle cx="24" cy="32" r="18" stroke="white" stroke-width="6" fill="none"/>
  <circle cx="40" cy="32" r="18" stroke="white" stroke-width="6" fill="none"/>
</svg>
"""
header_html = (
    "<div class='header-bar'>"
      f"<div class='header-left'>{SVG_LOGO}<span style='font:600 20px Montserrat,sans-serif;color:#d0e1ff'>Civic Twin™</span></div>"
      "<div class='header-center'>Empleo y Educación Tecnológica</div>"
      f"<img src='{FLAG_AR}' class='header-flag'>"
    "</div>"
)
st.markdown(header_html, unsafe_allow_html=True)

# ─── Carga de datos ────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    base = Path(__file__).parent
    return {
        'empleo': pd.read_csv(base/'empleo_tecnologico_por_provincia.csv'),
        'profesiones': pd.read_csv(base/'demanda_profesiones_tecnologicas.csv'),
        'oferta': pd.read_csv(base/'oferta_vs_demanda_tecnologica.csv'),
        'genero': pd.read_csv(base/'participacion_genero_tecnologia.csv'),
        'edad': pd.read_csv(base/'edad_promedio_roles_tecnologicos.csv'),
        'educacion': pd.read_csv(base/'nivel_educativo_trabajadores_tecnologia.csv'),
        'ia': pd.read_csv(base/'impacto_ia_roles_tecnologicos.csv')
    }
datos = cargar_datos()

# ─── Tablero con pestañas ──────────────────────────────────────────────
tabs = st.tabs(["Empleo por Provincia","Profesiones Demandadas","Oferta vs Demanda","Diversidad","Impacto IA"])

# Empleo por Provincia
with tabs[0]:
    fig = px.bar(
        datos['empleo'], x='Provincia', y='Empleos_tecnologicos',
        labels={'Empleos_tecnologicos':'Empleos (%)'},
        color='Empleos_tecnologicos', color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True, height=380)
    st.caption("Fuente: Ministerio de Trabajo, INDEC, CESSI")

# Profesiones Demandadas
with tabs[1]:
    fig = px.bar(
        datos['profesiones'], x='Porcentaje_demandado', y='Profesion', orientation='h',
        labels={'Porcentaje_demandado':'Demanda (%)'},
        color='Porcentaje_demandado', color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True, height=380)
    st.caption("Fuente: Portales laborales y CESSI")

# Oferta vs Demanda
with tabs[2]:
    df = datos['oferta'].melt(id_vars='Especialidad', value_vars=['Egresados_anuales','Puestos_demandados'], var_name='Tipo', value_name='Cantidad')
    fig = px.bar(
        df, x='Especialidad', y='Cantidad', color='Tipo', barmode='group',
        color_discrete_sequence=px.colors.sequential.Blues
    )
    st.plotly_chart(fig, use_container_width=True, height=380)
    st.caption("Fuente: Ministerio de Educación, Observatorios académicos")

# Diversidad
with tabs[3]:
    sub = st.tabs(["Género","Edad","Educación"])
    with sub[0]:
        df_g = datos['genero'].melt(id_vars='Categoria', var_name='Tipo', value_name='Porcentaje')
        fig = px.bar(df_g, x='Categoria', y='Porcentaje', color='Tipo', barmode='group', color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig, use_container_width=True, height=380)
        st.caption("Fuente: Chicas en Tecnología, CESSI")
    with sub[1]:
        fig = px.bar(datos['edad'], x='Rol', y='Edad_promedio', labels={'Edad_promedio':'Edad (años)'}, color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig, use_container_width=True, height=380)
        st.caption("Fuente: Observatorio de Empleo Tecnológico")
    with sub[2]:
        fig = px.pie(datos['educacion'], names='Nivel_educativo', values='Porcentaje', hole=0.3, color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig, use_container_width=True, height=380)
        st.caption("Fuente: INDEC, Ministerio de Educación")

# Impacto IA
with tabs[4]:
    fig = px.scatter(
        datos['ia'], x='Exposicion_IA', y='Complementariedad_IA', size='Riesgo_desplazamiento',
        color='Rol_tecnologico', size_max=50, color_discrete_sequence=px.colors.sequential.Blues,
        labels={'Exposicion_IA':'Exposición IA','Complementariedad_IA':'Complementariedad'}
    )
    st.plotly_chart(fig, use_container_width=True, height=380)
    st.caption("Fuente: Ministerio de Trabajo, OCDE, Banco Mundial")
    st.markdown("**Alta exposición + baja complementariedad = riesgo**; **alta complementariedad = oportunidad**")
```
