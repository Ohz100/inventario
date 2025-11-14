import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
import io

'# Inventario'

def draw_card(c, x, y, fila):
    c.rect(x, y, 190*mm, 69*mm)
    c.setFont("Helvetica", 10)
    c.drawString(x + 5*mm, y + (69 - 5 - 15 - 5 - 5)*mm, fila['folio'])
    c.drawString(x + 30*mm, y + (69 - 5 - 15 - 5 - 5)*mm, fila['producto'])
    barcode = code128.Code128(fila['folio'], barHeight=15*mm, barWidth=0.5)
    barcode.drawOn(c, x + 5*mm, y + (69 - 5 - 15)*mm)

uploaded_file = st.file_uploader('¡Carga tu archivo!', type='xlsx')
if uploaded_file is not None:
    df=pd.read_excel(uploaded_file)
    buffer=io.BytesIO()
    c = canvas.Canvas('rprtlab.pdf', pagesize=letter)
    for i, fila in df.iterrows():
        draw_card(c, 16*mm, 194*mm, fila)
        draw_card(c, 16*mm, 105*mm, fila)
        draw_card(c, 16*mm,  16*mm, fila)
        c.showPage()
    c.save()
    buffer.seek(0)
    st.download_button(
        label='Descarga',
        data=buffer,
        file_name='marbete.pdf',
        mime='application/pdf',
        icon=':material/download:'
    )
