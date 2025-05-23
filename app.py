import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Análisis de vehículos', layout='wide')

@st.cache_data
def load_data():
    data = pd.read_csv('vehicles_us.csv')
    data['date_posted'] = pd.to_datetime(data['date_posted'], errors='coerce')
    return data

car_data = load_data()

st.title('🚗 Análisis de Vehículos Usados - EE.UU.')
st.markdown('Aplicación interactiva para análisis exploratorio de un conjunto de datos reales de anuncios de venta de vehículos.')

st.markdown('## ⏳ Filtros por año del modelo y año de publicación')

min_model_year = int(car_data['model_year'].dropna().min())
max_model_year = int(car_data['model_year'].dropna().max())

year_range = st.slider(
    'Selecciona el rango de **año del modelo**',
    min_value=min_model_year,
    max_value=max_model_year,
    value=(min_model_year, max_model_year)
)

min_post_date = car_data['date_posted'].min().date()
max_post_date = car_data['date_posted'].max().date()

date_range = st.date_input(
    'Selecciona el rango de **fecha de publicación**',
    value=(min_post_date, max_post_date),
    min_value=min_post_date,
    max_value=max_post_date
)

car_data_filtrado = car_data[
    (car_data['model_year'].between(year_range[0], year_range[1])) &
    (car_data['date_posted'].dt.date.between(date_range[0], date_range[1]))
]

if st.checkbox('Mostrar tabla de datos filtrados'):
    st.dataframe(car_data_filtrado)

st.markdown('## 📊 Visualizaciones')

col1, col2 = st.columns(2)

with col1:
    st.markdown('### Histograma')
    columna_hist = st.selectbox('Selecciona columna para histograma', ['odometer', 'price', 'model_year', 'days_listed'])
    if st.checkbox('Mostrar histograma'):
        fig = px.histogram(car_data_filtrado, x=columna_hist, nbins=50, title=f'Distribución de {columna_hist}')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('### Diagrama de Dispersión')
    x_axis = st.selectbox('Eje X', ['odometer', 'price', 'model_year'])
    y_axis = st.selectbox('Eje Y', ['price', 'odometer', 'model_year'])
    if st.checkbox('Mostrar dispersión'):
        fig2 = px.scatter(car_data_filtrado, x=x_axis, y=y_axis, color='condition',
                          title=f'{y_axis} vs {x_axis} por condición')
        st.plotly_chart(fig2, use_container_width=True)

st.markdown('---')

st.markdown('## 🔍 Filtro por tipo de vehículo')

tipos = st.multiselect('Selecciona uno o varios tipos de vehículo', sorted(car_data_filtrado['type'].dropna().unique()))

if tipos:
    df_filtrado_tipo = car_data_filtrado[car_data_filtrado['type'].isin(tipos)]
    st.success(f'Se encontraron {len(df_filtrado_tipo)} registros para: {", ".join(tipos)}')
    st.dataframe(
        df_filtrado_tipo[['price', 'odometer', 'model_year', 'type']]
        .sort_values(by='price', ascending=False)
        .head(10)
    )
