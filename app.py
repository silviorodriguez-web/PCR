import streamlit as st

recibos = st.Page("pages/1_Recibos_de_Sueldo.py", title="Recibos de Sueldo", icon="📄")
# formularios = st.Page("pages/_2_Formularios_RRHH.py", title="Formularios RRHH", icon="📋")  # oculto temporalmente

pg = st.navigation([recibos])
st.set_page_config(page_title="Sistema PCR", page_icon="📄", layout="centered")
pg.run()
