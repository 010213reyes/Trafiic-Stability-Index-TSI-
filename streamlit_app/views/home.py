from __future__ import annotations

import streamlit as st

from components import navigate_to, render_pipeline_runner, render_process_animation, render_workspace_bar
from config import MODEL_MANIFEST_PATH, OBSERVATIONS_PATH, QUALITY_PATH, CONTRACT_PATH, parquet_row_count, read_json


def render() -> None:
    render_workspace_bar("Mapa del proyecto", "Vista general")
    contract = read_json(CONTRACT_PATH)
    quality = read_json(QUALITY_PATH)
    manifest = read_json(MODEL_MANIFEST_PATH)
    st.markdown('<div class="tsi-kicker">Investigacion internacional de trafico</div>', unsafe_allow_html=True)
    st.markdown('<div class="tsi-hero"><h1>Traffic Stability Index</h1><p>Una investigacion de trafico explicada como workspace: cada fase transforma la anterior y deja evidencia para la siguiente.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="tsi-kicker">Execution graph</div>', unsafe_allow_html=True)
    st.subheader("Flujo de trabajo")
    render_process_animation()
    st.caption("Cada etapa deja artefactos que alimentan la siguiente.")
    render_pipeline_runner()

    st.markdown('<div class="tsi-explanation"><h3>Workspace del proyecto</h3><p>Usa la navegacion lateral para abrir una fase. Cada vista combina una explicacion operativa con la evidencia generada por el proyecto.</p></div>', unsafe_allow_html=True)

    metrics = st.columns(4)
    metrics[0].metric("Fuentes", len(contract.get("sources", [])))
    metrics[1].metric("Fuentes CLEAN", len(quality.get("sources", [])))
    metrics[2].metric("Observaciones", f"{parquet_row_count(OBSERVATIONS_PATH) or 0:,}")
    metrics[3].metric("Modelo", manifest.get("model_name", "N/D"))

    st.subheader("Workspace views")
    phases = [
        ("mineria", "01", "Mineria de datos", "Fuentes, variables y decisiones"),
        ("ingenieria", "02", "Ingenieria de datos", "RAW a consolidado"),
        ("analisis", "03", "Analisis", "Calidad, comparacion y TSI"),
        ("ciencia", "04", "Ciencia de datos", "Features, modelos y validacion"),
        ("mlops", "05", "MLOps", "Registro, inferencia y monitoreo"),
    ]
    columns = st.columns(5)
    for column, (page, number, title, description) in zip(columns, phases):
        with column:
            st.markdown(f'<div class="tsi-phase"><div class="tsi-phase-num">FASE {number}</div><h3>{title}</h3><p>{description}</p></div>', unsafe_allow_html=True)
            if st.button("Abrir fase", key=f"open_{page}", use_container_width=True):
                navigate_to(page)

    st.info("La vista general consulta artefactos registrados. La accion Entrenar y registrar ejecuta el pipeline MLOps real y actualiza el historial de versiones.")
