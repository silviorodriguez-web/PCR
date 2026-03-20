import streamlit as st
import fitz
from PIL import Image
import io
from datetime import datetime

st.title("Sistema de Formularios y Firma")

pdf_file = st.file_uploader("Subir formulario PDF", type="pdf")

if pdf_file:
    pdf_bytes = pdf_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[0]

    text = page.get_text()
    lineas = text.split("\n")

    etiquetas = []
    for linea in lineas:
        if ":" in linea and len(linea) < 40:
            etiqueta = linea.split(":")[0]
            etiquetas.append(etiqueta)

    st.subheader("Completar información")

    datos = {}
    for etiqueta in etiquetas:
        valor = st.text_input(etiqueta)
        datos[etiqueta] = valor

    firma_file = st.file_uploader("Subir firma (PNG)", type=["png", "jpg"])

    if st.button("Generar vista previa"):
        for etiqueta, valor in datos.items():
            rects = page.search_for(etiqueta + ":")
            if rects:
                r = rects[0]
                x = r.x1 + 5
                y = r.y0
                page.insert_text((x, y), valor, fontsize=10)

        if firma_file:
            firma_img = Image.open(firma_file)
            img_bytes = io.BytesIO()
            firma_img.save(img_bytes, format="PNG")

            rects = page.search_for("Firma")
            if rects:
                r = rects[0]
                firma_rect = fitz.Rect(r.x0, r.y0 - 40, r.x0 + 150, r.y0)
                page.insert_image(firma_rect, stream=img_bytes.getvalue())

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        page.insert_text((400, 750), f"Firmado: {fecha}", fontsize=8)

        pix = page.get_pixmap()
        st.subheader("Vista previa")
        st.image(pix.tobytes())

        output = io.BytesIO()
        doc.save(output)

        st.download_button(
            "Descargar PDF firmado",
            data=output.getvalue(),
            file_name="documento_firmado.pdf",
            mime="application/pdf"
        )
