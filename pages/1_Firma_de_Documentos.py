import streamlit as st
import fitz
from PIL import Image
from datetime import datetime
import io

st.title("Firma de Documentos")

pdf_file = st.file_uploader("Subir PDF", type="pdf")
firma_file = st.file_uploader("Subir imagen de firma", type=["png", "jpg"])

st.subheader("Datos del trabajador")

nombre = st.text_input("Nombre")
apellido_p = st.text_input("Apellido Paterno")
apellido_m = st.text_input("Apellido Materno")
area = st.text_input("Área")
cargo = st.text_input("Cargo")
dni = st.text_input("DNI")
dias = st.text_input("Días solicitados")
desde = st.text_input("Desde")
hasta = st.text_input("Hasta")
observaciones = st.text_area("Observaciones")

if st.button("Firmar documento"):
    if pdf_file and firma_file:
        pdf_bytes = pdf_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0]

        page.insert_text((80, 150), f"Nombre: {nombre}", fontsize=10)
        page.insert_text((80, 170), f"Apellido Paterno: {apellido_p}", fontsize=10)
        page.insert_text((80, 190), f"Apellido Materno: {apellido_m}", fontsize=10)
        page.insert_text((80, 210), f"Área: {area}", fontsize=10)
        page.insert_text((80, 230), f"Cargo: {cargo}", fontsize=10)
        page.insert_text((80, 250), f"DNI: {dni}", fontsize=10)
        page.insert_text((80, 270), f"Días solicitados: {dias}", fontsize=10)
        page.insert_text((80, 290), f"Desde: {desde}", fontsize=10)
        page.insert_text((80, 310), f"Hasta: {hasta}", fontsize=10)
        page.insert_text((80, 330), f"Observaciones: {observaciones}", fontsize=10)

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        page.insert_text((350, 700), f"Firmado: {fecha}", fontsize=10)

        firma = Image.open(firma_file)
        img_bytes = io.BytesIO()
        firma.save(img_bytes, format="PNG")

        rect = fitz.Rect(350, 650, 500, 720)
        page.insert_image(rect, stream=img_bytes.getvalue())

        output = io.BytesIO()
        doc.save(output)

        st.download_button(
            "Descargar PDF firmado",
            data=output.getvalue(),
            file_name="documento_firmado.pdf",
            mime="application/pdf"
        )
        st.success("Documento firmado correctamente")
    else:
        st.warning("Por favor sube el PDF y la imagen de firma.")
