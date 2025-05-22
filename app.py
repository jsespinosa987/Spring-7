import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Análisis de vehículos', layout='wide')

car_data = pd.read_csv('vehicles_us.csv')

st.title('🚗 Análisis de Vehículos Usados - EE.UU.')
st.markdown('Interfaz interactiva para análisis exploratorio de datos con Streamlit.')

if st.checkbox('Mostrar tabla de datos'):
    st.dataframe(car_data)

col1, col2 = st.columns(2)

with col1:
    columna_hist = st.selectbox('Selecciona columna para histograma', ['odometer', 'price', 'model_year', 'days_listed'])
    if st.checkbox('Mostrar histograma'):
        fig = px.histogram(car_data, x=columna_hist, nbins=50, title=f'Distribución de {columna_hist}')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    x_axis = st.selectbox('Eje X (dispersión)', ['odometer', 'price', 'model_year'])
    y_axis = st.selectbox('Eje Y (dispersión)', ['price', 'odometer', 'model_year'])
    if st.checkbox('Mostrar diagrama de dispersión'):
        fig2 = px.scatter(car_data, x=x_axis, y=y_axis, color='condition', title=f'{y_axis} vs {x_axis} por condición')
        st.plotly_chart(fig2, use_container_width=True)

st.markdown('---')

tipos = st.multiselect('Filtrar por tipo de vehículo', sorted(car_data['type'].dropna().unique()))

if tipos:
    df_filtrado = car_data[car_data['type'].isin(tipos)]
    st.subheader(f'Filtrado: {", ".join(tipos)}')
    st.dataframe(df_filtrado[['price', 'odometer', 'model_year', 'type']].sort_values(by='price', ascending=False).head(10))
