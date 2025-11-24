import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from reportlab.lib.colors import black, white, HexColor
import io

'# Inventario'

def draw_card(c, x, y, fila, cuenta, color_fondo, barra):
    c.setFillColor(black)
    c.rect(x, y, 170*mm, 52*mm)
    c.setFont("Helvetica", 10)

    # lInea 1
    y_line = y + 3*mm
    c.drawString(x + 8*mm, y_line, 'Ubicación')
    c.drawString(x + (8 + 55)*mm, y_line, 'Lote')
    c.drawString(x + (8 + 55 + 55)*mm, y_line, 'Serie')
    c.drawString(x + 33*mm, y_line, fila['ubicaciOn'])
    c.drawString(x + (33 + 55)*mm, y_line, fila['lote'])
    c.drawString(x + (33 + 55 + 50)*mm, y_line, fila['serie'])
    c.line(x + 32*mm, y_line - 1*mm, x + 60*mm, y_line - 1*mm)
    c.line(x + (32 + 55)*mm, y_line - 1*mm, x + (60 + 55)*mm, y_line - 1*mm)
    c.line(x + (32 + 55 + 50)*mm, y_line - 1*mm, x + (60 + 55 + 50)*mm, y_line - 1*mm)
    # lInea 2
    y_line = y_line + 5.8*mm
    c.drawString(x + 8*mm, y_line, 'Contado por')
    c.drawString(x + (8 + 55)*mm, y_line, 'Auditado por')
    c.drawString(x + (8 + 55 + 55)*mm, y_line, 'Obs/Surp')
    c.line(x + 32*mm, y_line - 1*mm, x + 60*mm, y_line - 1*mm)
    c.line(x + (32 + 55)*mm, y_line - 1*mm, x + (60 + 55)*mm, y_line - 1*mm)
    c.line(x + (32 + 55 + 50)*mm, y_line - 1*mm, x + (60 + 55 + 50)*mm, y_line - 1*mm)
    # lInea 3
    y_line = y_line + 5.8*mm
    c.drawString(x + 8*mm, y_line, 'Cant. contada')
    c.drawString(x + (8 + 55)*mm, y_line, 'Cant. auditada')
    c.drawString(x + (8 + 55 + 55)*mm, y_line, 'Unidad')
    c.drawString(x + (33 + 55 + 50)*mm, y_line, fila['unidad'])
    c.line(x + 32*mm, y_line - 1*mm, x + 60*mm, y_line - 1*mm)
    c.line(x + (32 + 55)*mm, y_line - 1*mm, x + (60 + 55)*mm, y_line - 1*mm)
    c.line(x + (32 + 55 + 50)*mm, y_line - 1*mm, x + (60 + 55 + 50)*mm, y_line - 1*mm)
    # lInea 4
    y_line = y_line + 5.8*mm
    c.drawString(x + 8*mm, y_line, fila['producto'])
    c.drawString(x + 50*mm, y_line, fila['descripciOn'])
    c.line(x + 8*mm, y_line - 1*mm, x + 48*mm, y_line - 1*mm)
    c.line(x + 50*mm, y_line - 1*mm, x + 165*mm, y_line - 1*mm)
    # lInea 5
    y_line = y_line + 5.8*mm
    c.drawString(x + 8*mm, y_line, 'Producto')
    c.drawString(x + 50*mm, y_line, 'Descripción')
    # lInea 6
    y_line = y_line + 5.8*mm
    c.drawString(x + 8*mm, y_line, 'Folio')
    c.drawString(x + 30*mm, y_line, fila['folio'])
    c.setFillColor(color_fondo)
    c.rect(x + (32 + 55 + 50 - 2)*mm, y_line - 2*mm, 30*mm, 8*mm, fill=1, stroke=0)
    c.setFillColor(black)
    c.drawString(x + (32 + 55 + 50)*mm, y_line, cuenta)
    barcode = code128.Code128(barra, barHeight=10*mm, barWidth=1) # barWidth=0.5
    barcode.drawOn(c, x + 60*mm, y_line)
    # lInea 7
    y_line = y_line + 5.8*mm
    c.drawString(x + 8*mm, y_line, 'Almacen')
    c.drawString(x + 30*mm, y_line, fila['almacEn'])
    # lInea 8
    y_line = y_line + 5.8*mm
    c.drawString(x + 8*mm, y_line, 'Dynamics 365')
    c.drawString(x + 50*mm, y_line, 'Etiqueta inventario físico Svifflug')
    c.drawString(x + 140*mm, y_line, fila['fecha'].strftime('%Y-%m-%d'))

    #c.drawString(x + 100*mm, y + 10*mm, fila['folio'])
    #c.drawString(x + 100*mm, y + 20*mm, fila['producto'])

uploaded_file = st.file_uploader('¡Carga tu archivo!', type='xlsx')
if uploaded_file is not None:
    df=pd.read_excel(uploaded_file, dtype={
        'folio':'string',
        'almacEn':'string',
        'producto':'string',
        'descripciOn':'string',
        'unidad':'string',
        'lote':'string',
        'serie':'string'
    })
    buffer=io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    for i, fila in df.iterrows():
        draw_card(c, 23*mm, 219*mm, fila, 'Conteo 1', HexColor('#C6EFCD'), fila['almacEn'] + 'z' + fila['folio'])
        draw_card(c, 23*mm, 149*mm, fila, 'Conteo 2', HexColor('#FEEB9C'), fila['almacEn'] + 'z' + fila['folio'])
        draw_card(c, 23*mm,   9*mm, fila, 'Duplicado', white, 'D')
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

# python -m streamlit run card.py
# streamlit run card.py