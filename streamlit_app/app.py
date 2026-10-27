from __future__ import annotations

import streamlit as st

from components import inject_styles, navigate_to
from config import ADMIN_PASSWORD, ADMIN_USERNAME
from views import analisis, ciencia, home, ingenieria, mineria, mlops


st.set_page_config(
    page_title="TSI | Recorrido del proyecto",
    page_icon="TSI",
    layout="wide",
)
inject_styles()


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "home"


if not st.session_state.authenticated:
    st.markdown('<div class="tsi-kicker">Workspace del proyecto</div>', unsafe_allow_html=True)
    st.title("Traffic Stability Index")
    st.caption("Acceso a la investigacion internacional y su flujo MLOps local")
    with st.form("admin_login"):
        username = st.text_input("Usuario")
        password = st.text_input("Contrasena", type="password")
        submitted = st.form_submit_button("Ingresar", type="primary")
    if submitted:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Usuario o contrasena incorrectos.")
    st.stop()


st.sidebar.markdown("<div class='tsi-kicker'>TSI / DATA LAB</div>", unsafe_allow_html=True)
st.sidebar.title("Control del workspace")
st.sidebar.caption("Ejecucion y observabilidad del proyecto")
st.sidebar.markdown("### Workspace")
if st.sidebar.button("Vista general", key="control_home", use_container_width=True):
    navigate_to("home")
st.sidebar.markdown("### Vistas")
phase_options = {
    "Mapa del proyecto": "home",
    "01 | Mineria de datos": "mineria",
    "02 | Ingenieria de datos": "ingenieria",
    "03 | Analisis": "analisis",
    "04 | Ciencia de datos": "ciencia",
    "05 | MLOps": "mlops",
}
current_label = next((label for label, page in phase_options.items() if page == st.session_state.page), "Mapa del proyecto")
selected_phase = st.sidebar.selectbox("Abrir vista", list(phase_options), index=list(phase_options).index(current_label))
if st.sidebar.button("Abrir vista seleccionada", key="control_phase", use_container_width=True):
    navigate_to(phase_options[selected_phase])
st.sidebar.markdown("### Operacion")
if st.sidebar.button("Entrenar y registrar", key="control_run", use_container_width=True):
    st.session_state.page = "home"
    st.session_state.auto_run_pipeline = True
    st.rerun()
if st.sidebar.button("Abrir registro MLOps", key="control_mlops", use_container_width=True):
    navigate_to("mlops")

st.sidebar.divider()
if st.sidebar.button("Cerrar sesion", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.page = "home"
    st.rerun()


views = {
    "home": home.render,
    "mineria": mineria.render,
    "ingenieria": ingenieria.render,
    "analisis": analisis.render,
    "ciencia": ciencia.render,
    "mlops": mlops.render,
}
views.get(st.session_state.page, home.render)()
