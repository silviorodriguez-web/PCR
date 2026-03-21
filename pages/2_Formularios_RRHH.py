import streamlit as st
import fitz
from PIL import Image
import io
from datetime import date
import os

st.title("Formularios RRHH")

FORMULARIOS = {
    "Solicitud de Vacaciones": {
        "archivo": "templates/vacaciones.pdf",
        "fechas": ["Desde", "Hasta"],
        "textos": ["N° días solicitados"],
        "motivo": False,
    },
    "Día Libre Semestral": {
        "archivo": "templates/semestral.pdf",
        "fechas": ["Día Libre Solicitado"],
        "textos": ["Semestre I o II"],
        "motivo": False,
    },
    "Día Libre por Cumpleaños": {
        "archivo": "templates/cumpleanos.pdf",
        "fechas": ["Día Libre Solicitado"],
        "textos": [],
        "motivo": False,
    },
    "Permisos y Licencias": {
        "archivo": "templates/permisos.pdf",
        "fechas": ["Fecha permiso", "Desde", "Hasta"],
        "textos": ["N° días solicitados"],
        "motivo": True,
    },
}

# --- Selector de formulario ---
tipo = st.selectbox("Seleccionar formulario", list(FORMULARIOS.keys()))
config = FORMULARIOS[tipo]

st.markdown("---")

# --- Datos del trabajador ---
st.subheader("Datos del trabajador")

col1, col2, col3 = st.columns(3)
with col1:
    apellido_p = st.text_input("Apellido Paterno")
with col2:
    apellido_m = st.text_input("Apellido Materno")
with col3:
    nombre = st.text_input("Nombre")

col4, col5, col6 = st.columns(3)
with col4:
    area = st.text_input("Área")
with col5:
    cargo = st.text_input("Cargo")
with col6:
    dni = st.text_input("DNI")

fecha_hoy = st.date_input("Fecha", value=date.today())

st.markdown("---")

# --- Campos específicos del formulario ---
st.subheader("Información de la solicitud")

datos_extra = {}

for campo in config["fechas"]:
    datos_extra[campo] = st.date_input(campo, key=campo).strftime("%d/%m/%Y")

for campo in config["textos"]:
    datos_extra[campo] = st.text_input(campo, key=campo)

if config["motivo"]:
    motivo = st.selectbox(
        "Motivo del permiso",
        ["Consulta Médica", "Permiso Personal", "Otros"]
    )
    datos_extra["Motivo"] = motivo

observaciones = st.text_area("Observaciones")

st.markdown("---")

# --- Firma ---
st.subheader("Firma del trabajador")
firma_file = st.file_uploader("Subir firma (PNG/JPG)", type=["png", "jpg"])

# --- Generar PDF ---
def insertar_campo(page, label, valor, fontsize=9):
    for variante in [label + ":", label + " :", label]:
        rects = page.search_for(variante)
        if rects:
            r = rects[0]
            page.insert_text((r.x1 + 3, r.y1 - 1), valor, fontsize=fontsize)
            return True
    return False

if st.button("Generar formulario", type="primary"):
    template_path = config["archivo"]

    if not os.path.exists(template_path):
        st.error(f"No se encontró el template: {template_path}")
    else:
        doc = fitz.open(template_path)
        page = doc[0]

        todos_los_datos = {
            "FECHA": fecha_hoy.strftime("%d/%m/%Y"),
            "Apellido Paterno": apellido_p,
            "Apellido materno": apellido_m,
            "Apellido Materno": apellido_m,
            "Nombre": nombre,
            "Área": area,
            "Cargo": cargo,
            "DNI": dni,
            "Observaciones": observaciones,
            **datos_extra,
        }

        # Intentar llenar widgets del PDF (campos de formulario)
        widgets_filled = set()
        try:
            for widget in page.widgets():
                fname = (widget.field_name or "").strip()
                for key, val in todos_los_datos.items():
                    if fname and (key.lower() in fname.lower() or fname.lower() in key.lower()):
                        widget.field_value = str(val)
                        widget.update()
                        widgets_filled.add(key)
                        break
        except Exception:
            pass

        # Para campos no llenados por widget, usar búsqueda de texto
        for key, val in todos_los_datos.items():
            if key not in widgets_filled and val:
                insertar_campo(page, key, str(val))

        # Insertar firma
        if firma_file:
            firma_img = Image.open(firma_file)
            img_bytes = io.BytesIO()
            firma_img.save(img_bytes, format="PNG")

            for texto_firma in ["Firma del trabajador", "Firma del Trabajador"]:
                rects = page.search_for(texto_firma)
                if rects:
                    r = rects[0]
                    firma_rect = fitz.Rect(r.x0, r.y0 - 45, r.x0 + 130, r.y0 - 5)
                    page.insert_image(firma_rect, stream=img_bytes.getvalue())
                    break

        output = io.BytesIO()
        doc.save(output)

        nombre_archivo = f"{tipo} - {apellido_p} {nombre}.pdf".strip()

        st.download_button(
            "Descargar formulario completado",
            data=output.getvalue(),
            file_name=nombre_archivo,
            mime="application/pdf",
        )
        st.success("Formulario generado correctamente")
