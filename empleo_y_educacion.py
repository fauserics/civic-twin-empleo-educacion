import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración general sin scroll largo
st.set_page_config(
    page_title='Civic Twin: Empleo y Educación',
    layout='wide',
    initial_sidebar_state='collapsed'
)
st.title("📊 Civic Twin: Empleo, Educación y Futuro del Trabajo Tecnológico")

# Paleta azul única
BLUE_SCALE = px.colors.sequential.Blues

# Carga de datos (una sola vez)
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

# Defino pestañas principales
tabs = st.tabs([
    "📍 Empleo por Provincia",
    "💼 Profesiones Demandadas",
    "📚 Oferta vs Demanda",
    "👥 Diversidad",
    "🤖 Impacto IA"
])

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
    st.plotly_chart(fig, use_container_width=True, height=450)

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
    st.plotly_chart(fig, use_container_width=True, height=450)

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
    st.plotly_chart(fig, use_container_width=True, height=450)

# 4) Diversidad (pestañas internas)
with tabs[3]:
    sub_tabs = st.tabs(["Género", "Edad", "Educación"])
    # Género
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
        st.plotly_chart(fig, use_container_width=True, height=450)
    # Edad
    with sub_tabs[1]:
        fig = px.bar(
            datos['edad'],
            x='Rol',
            y='Edad_promedio',
            labels={'Edad_promedio': 'Edad (años)'},
            color_discrete_sequence=BLUE_SCALE
        )
        st.plotly_chart(fig, use_container_width=True, height=450)
    # Educación
    with sub_tabs[2]:
        fig = px.pie(
            datos['educacion'],
            names='Nivel_educativo',
            values='Porcentaje',
            color_discrete_sequence=BLUE_SCALE,
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True, height=450)

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
    st.plotly_chart(fig, use_container_width=True, height=450)
    st.markdown("""
    **Interpretación rápida:**
    - 🟥 Alta exposición + baja complementariedad = mayor riesgo.
    - 🟩 Alta complementariedad = gran oportunidad de colaboración con IA.
    """)

# Footer
st.markdown("---")
st.caption("Civic Twin © 2025 · Datos: Ministerio de Trabajo, Educación, INDEC, CESSI, Observatorios.")
