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
    st.markdown('<div class="tsi-kicker">Demostracion del proyecto</div>', unsafe_allow_html=True)
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


st.sidebar.title("Recorrido TSI")
st.sidebar.caption("Selecciona una fase para explorarla")
navigation = [
    ("home", "Mapa del proyecto"),
    ("mineria", "01 | Mineria"),
    ("ingenieria", "02 | Ingenieria"),
    ("analisis", "03 | Analisis"),
    ("ciencia", "04 | Ciencia de datos"),
    ("mlops", "05 | MLOps"),
]
for page, label in navigation:
    if st.sidebar.button(label, key=f"nav_{page}", use_container_width=True):
        navigate_to(page)

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
