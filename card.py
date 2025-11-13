import streamlit as st
import pandas as pd

'# Inventario'

uploaded_file = st.file_uploader('¡Carga tu archivo!', type='xlsx')
if uploaded_file is not None:
    df=pd.read_excel(uploaded_file)
    df['c']=df['a'] + df['b']
    st.download_button(
        label='Descarga',
        data=df.to_csv(),
        file_name='output.csv',
        mime='text/csv',
        icon=':material/download:'
    )