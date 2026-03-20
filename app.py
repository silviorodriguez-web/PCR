import streamlit as st

st.set_page_config(page_title="Sistema de Firma", page_icon="📄", layout="centered")

st.title("📄 Sistema de Firma de Documentos")
st.markdown("---")

st.markdown("""
Bienvenido. Selecciona una herramienta desde el menú lateral:

- **Firma de Documentos** — Completa datos del trabajador y firma un PDF
- **Recibos de Sueldo** — Procesa recibos en lote (agrega nombre automáticamente)
- **Formularios** — Completa y firma formularios de RRHH de forma dinámica
""")
