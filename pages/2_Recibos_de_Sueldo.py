import streamlit as st
import fitz
import re
import zipfile
import io

st.title("Procesador de Recibos de Sueldo")

uploaded_files = st.file_uploader(
    "Sube todos los recibos PDF",
    type="pdf",
    accept_multiple_files=True
)

def extraer_nombre(texto):
    match = re.search(
        r"([A-ZÁÉÍÓÚÑ]+(?:\s+[A-ZÁÉÍÓÚÑ]+){2,9})",
        texto
    )
    if match:
        return match.group(0)
    return None

if uploaded_files:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            page = pdf[0]
            texto = page.get_text()
            nombre = extraer_nombre(texto)

            if nombre:
                rects = page.search_for("RECIBI CONFORME")
                for rect in rects:
                    center_x = rect.x0 + rect.width / 2
                    y = rect.y0 - 6
                    fontsize = 6
                    text_length = fitz.get_text_length(nombre, fontsize=fontsize)
                    max_width = rect.width + 40

                    while text_length > max_width and fontsize > 4:
                        fontsize -= 0.5
                        text_length = fitz.get_text_length(nombre, fontsize=fontsize)

                    x = center_x - (text_length / 2)
                    page.insert_text((x, y), nombre, fontsize=fontsize)

            output_stream = io.BytesIO()
            pdf.save(output_stream)
            output_stream.seek(0)
            zip_file.writestr("procesado_" + uploaded_file.name, output_stream.read())

    st.download_button(
        label="Descargar todos los recibos procesados (ZIP)",
        data=zip_buffer.getvalue(),
        file_name="recibos_procesados.zip",
        mime="application/zip"
    )
