import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración general del tablero
st.set_page_config(page_title='Civic Twin: Empleo y Educación', layout='wide')
st.title("📊 Civic Twin: Empleo, Educación y Futuro del Trabajo Tecnológico")

# Paleta de color azul uniforme para todo
color_scale = 'Blues'

# Botonera de navegación
secciones = [
    "📍 Empleo por Provincia",
    "💼 Profesiones más Demandadas",
    "📚 Oferta vs Demanda Educativa",
    "👥 Diversidad e Inclusión",
    "🤖 Impacto de la IA"
]
opcion = st.radio("Seleccioná una sección:", secciones, horizontal=True)

# Cargar todos los datos una sola vez
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

# Sección 1: Empleo por Provincia
if opcion == secciones[0]:
    fig = px.bar(
        datos['empleo'],
        x='Provincia',
        y='Empleos_tecnologicos',
        labels={'Empleos_tecnologicos': 'Porcentaje de Empleos (%)'},
        color='Empleos_tecnologicos',
        color_continuous_scale=color_scale
    )
    st.plotly_chart(fig, use_container_width=True)

# Sección 2: Profesiones más Demandadas
elif opcion == secciones[1]:
    fig = px.bar(
        datos['profesiones'],
        x='Porcentaje_demandado',
        y='Profesion',
        orientation='h',
        labels={'Porcentaje_demandado': 'Demanda (%)'},
        color='Porcentaje_demandado',
        color_continuous_scale=color_scale
    )
    st.plotly_chart(fig, use_container_width=True)

# Sección 3: Oferta vs Demanda Educativa
elif opcion == secciones[2]:
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
        color_discrete_sequence=px.colors.sequential.Blues,
        labels={'Cantidad': 'Cantidad de personas'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Sección 4: Diversidad e Inclusión
elif opcion == secciones[3]:
    col1, col2 = st.columns(2)

    with col1:
        df = datos['genero'].melt(id_vars='Categoria', var_name='Tipo', value_name='Porcentaje')
        fig = px.bar(df, x='Categoria', y='Porcentaje', color='Tipo', barmode='group',
                     color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(datos['edad'], x='Rol', y='Edad_promedio',
                     color_discrete_sequence=px.colors.sequential.Blues,
                     labels={'Edad_promedio': 'Edad promedio (años)'})
        st.plotly_chart(fig, use_container_width=True)

    fig = px.pie(datos['educacion'], names='Nivel_educativo', values='Porcentaje',
                 color_discrete_sequence=px.colors.sequential.Blues)
    st.plotly_chart(fig, use_container_width=True)

# Sección 5: Impacto de la IA
elif opcion == secciones[4]:
    fig = px.scatter(
        datos['ia'],
        x='Exposicion_IA',
        y='Complementariedad_IA',
        size='Riesgo_desplazamiento',
        color='Rol_tecnologico',
        size_max=60,
        color_discrete_sequence=px.colors.sequential.Blues,
        labels={
            'Exposicion_IA': 'Exposición a la IA',
            'Complementariedad_IA': 'Complementariedad con IA'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **📌 Interpretación del gráfico:**

    - 🟥 Alta exposición y poca complementariedad → riesgo de desplazamiento.
    - 🟩 Alta complementariedad → oportunidad de adaptación con IA.
    """)

# Footer
st.markdown("---")
st.caption("Civic Twin © 2025 · Datos: Ministerio de Trabajo, Educación, INDEC, CESSI y otros.")
