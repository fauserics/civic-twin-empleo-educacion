import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ─── Página Configuración ───────────────────────────────────────────
st.set_page_config(
    page_title="Civic Twin™: Empleo y Educación Tecnológica",
    layout="wide",
    menu_items={"Get help": None, "Report a bug": None, "About": None}
)

# ─── CSS y Header de Civic Twin Café ───────────────────────────────
HEADER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
:root{
  --topbar-h: 42px;
  --header-h: 70px;
  --sidebar-w: 300px;
  --azul: #1F4E79;
}
.header-bar{
  position:fixed; top:var(--topbar-h); left:0; width:100%; height:var(--header-h);
  background:linear-gradient(90deg,#14406b 0%,var(--azul) 100%);
  display:flex; align-items:center; justify-content:center;
}
.header-left, .header-center{ display:flex; align-items:center; color:#fff; }
.header-left { position:absolute; left:16px; }
.header-center { font:600 20px 'Montserrat',sans-serif; }
.header-flag{ position:absolute; right:16px; height:32px; border-radius:3px; }
section[data-testid="stSidebar"]{ margin-top:calc(var(--topbar-h) + var(--header-h)); }
div.block-container{ margin-top:calc(var(--topbar-h) + var(--header-h) + 4px); overflow:hidden; }
</style>
"""

SVG_LOGO = """
<svg width="32" height="32" viewBox="0 0 64 64" fill="none"
     xmlns="http://www.w3.org/2000/svg"
     style="vertical-align:middle;margin-right:8px">
  <circle cx="24" cy="32" r="18" stroke="white" stroke-width="6" fill="none"/>
  <circle cx="40" cy="32" r="18" stroke="white" stroke-width="6" fill="none"/>
</svg>
"""

FLAG_AR = "https://flagcdn.com/w40/ar.png"

header_html = (
    HEADER_CSS +
    f"<div class='header-bar'>"
    f"<div class='header-left'>{SVG_LOGO}<span>Civic Twin™</span></div>"
    f"<div class='header-center'>Empleo, Educación y Futuro del Trabajo Tecnológico</div>"
    f"<img src='{FLAG_AR}' class='header-flag'>"
    f"</div>"
)

st.markdown(header_html, unsafe_allow_html=True)

# ─── Cargar Datos ────────────────────────────────────────────────────
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

# Paleta uniforme azul
BLUE_SCALE = px.colors.sequential.Blues

# ─── Navegación con Pestañas sin Scroll ─────────────────────────────
tabs = st.tabs(["📍 Empleo por Provincia", "💼 Profesiones Demandadas", "📚 Oferta vs Demanda", "👥 Diversidad", "🤖 Impacto IA"])

# 1) Empleo
with tabs[0]:
    fig = px.bar(
        datos['empleo'], x='Provincia', y='Empleos_tecnologicos',
        labels={'Empleos_tecnologicos':'% Empleos'},
        color='Empleos_tecnologicos', color_continuous_scale=BLUE_SCALE
    )
    st.plotly_chart(fig, use_container_width=True, height=450)

# 2) Profesiones Demandadas
with tabs[1]:
    fig = px.bar(
        datos['profesiones'], x='Porcentaje_demandado', y='Profesion', orientation='h',
        labels={'Porcentaje_demandado':'% Demanda'},
        color='Porcentaje_demandado', color_continuous_scale=BLUE_SCALE
    )
    st.plotly_chart(fig, use_container_width=True, height=450)

# 3) Oferta vs Demanda
with tabs[2]:
    df = datos['oferta_vs_demanda'].melt(
        id_vars='Especialidad', value_vars=['Egresados_anuales','Puestos_demandados'],
        var_name='Tipo', value_name='Cantidad'
    )
    fig = px.bar(
        df, x='Especialidad', y='Cantidad', color='Tipo', barmode='group',
        color_discrete_sequence=BLUE_SCALE
    )
    st.plotly_chart(fig, use_container_width=True, height=450)

# 4) Diversidad
with tabs[3]:
    sub = st.tabs(["Género","Edad","Educación"])
    with sub[0]:
        df = datos['genero'].melt(id_vars='Categoria', var_name='Tipo', value_name='Porcentaje')
        fig = px.bar(df, x='Categoria', y='Porcentaje', color='Tipo', barmode='group',
                     color_discrete_sequence=BLUE_SCALE)
        st.plotly_chart(fig, use_container_width=True, height=450)
    with sub[1]:
        fig = px.bar(datos['edad'], x='Rol', y='Edad_promedio', labels={'Edad_promedio':'Edad'},
                     color_discrete_sequence=BLUE_SCALE)
        st.plotly_chart(fig, use_container_width=True, height=450)
    with sub[2]:
        fig = px.pie(datos['educacion'], names='Nivel_educativo', values='Porcentaje', hole=0.3,
                     color_discrete_sequence=BLUE_SCALE)
        st.plotly_chart(fig, use_container_width=True, height=450)

# 5) Impacto IA
with tabs[4]:
    fig = px.scatter(
        datos['ia'], x='Exposicion_IA', y='Complementariedad_IA', size='Riesgo_desplazamiento',
        color='Rol_tecnologico', size_max=50, color_discrete_sequence=BLUE_SCALE,
        labels={'Exposicion_IA':'Exposición IA','Complementariedad_IA':'Complementariedad IA'}
    )
    st.plotly_chart(fig, use_container_width=True, height=450)
    st.markdown("""
    **Interpretación rápida:**
    - 🟥 Alta exposición + baja complementariedad = riesgo
    - 🟩 Alta complementariedad = oportunidad
    """)

# Footer
st.markdown("---")
st.caption("Civic Twin™ © 2025 · Datos: Ministerios, INDEC, CESSI, Observatorios.")
