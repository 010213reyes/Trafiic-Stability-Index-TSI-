from __future__ import annotations

import streamlit as st

from components import render_phase_header, render_phase_navigation
from config import OBSERVATIONS_PATH, SQL_PLAN_PATH, parquet_row_count


def render() -> None:
    render_phase_header("03", "Analisis", "Convierte los datos consolidados en evidencia sobre calidad, cobertura y estabilidad.")
    left, right = st.columns(2)
    with left:
        st.metric("Observaciones consolidadas", f"{parquet_row_count(OBSERVATIONS_PATH) or 0:,}")
        st.write("El analisis conserva separadas las metricas de velocidad, intensidad, indice de congestion y longitud de congestion.")
    with right:
        st.metric("SQL", "Plan documentado" if SQL_PLAN_PATH.exists() else "Pendiente")
        st.write("La validacion SQL compara los conteos de Parquet y MySQL por fuente.")
    st.subheader("Salida analitica")
    st.write("La fase produce perfiles de calidad, cobertura temporal, comparacion metodologica y el TSI provisional normalizado en escala 0-100.")
    render_phase_navigation("analisis")
