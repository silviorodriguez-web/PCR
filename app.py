import streamlit as st

st.set_page_config(page_title="Sistema PCR", page_icon="📄", layout="centered")

st.title("📄 Sistema de RRHH - PCR")
st.markdown("---")

st.markdown("""
Bienvenido. Selecciona una herramienta desde el menú lateral:

- **Recibos de Sueldo** — Procesa recibos en lote o sábana (agrega nombre automáticamente)
- **Formularios RRHH** — Completa y firma formularios de vacaciones, permisos y días libres
""")
