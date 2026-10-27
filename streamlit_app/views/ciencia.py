from __future__ import annotations

import pandas as pd
import streamlit as st

from components import render_phase_header, render_phase_navigation
from config import EXPERIMENT_PATH, VALIDATION_PATH, read_csv, read_json


def render() -> None:
    render_phase_header("04", "Ciencia de datos", "Construye features temporales, compara modelos y valida el candidato internacional.")
    experiment = read_json(EXPERIMENT_PATH)
    metrics = st.columns(4)
    metrics[0].metric("Modelo candidato", experiment.get("modelo_candidato", "N/D"))
    metrics[1].metric("MAE modelo", f"{experiment.get('mae_prueba_modelo_candidato', 0):.3f}")
    metrics[2].metric("MAE baseline", f"{experiment.get('mae_prueba_baseline', 0):.3f}")
    metrics[3].metric("Fuentes con mejora", f"{experiment.get('fuentes_con_mejora', 0)}/{experiment.get('fuentes_evaluadas', 0)}")

    st.subheader("Validacion por fuente")
    validation = read_csv(VALIDATION_PATH)
    if validation.empty:
        st.warning("No existe una tabla de validacion disponible.")
    else:
        st.dataframe(validation, use_container_width=True, hide_index=True)

    st.warning("Estado: candidato internacional no final. Madrid necesita una muestra de prueba mas amplia y Guadalajara queda para calibracion futura.")
    render_phase_navigation("ciencia")
