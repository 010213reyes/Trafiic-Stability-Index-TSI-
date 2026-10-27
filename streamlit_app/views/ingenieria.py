from __future__ import annotations

import pandas as pd
import streamlit as st

from components import render_phase_header, render_phase_navigation
from config import CONSOLIDATION_PATH, OBSERVATIONS_PATH, QUALITY_PATH, read_json, parquet_row_count


def render() -> None:
    render_phase_header("02", "Ingenieria de datos", "Transforma fuentes heterogeneas en datos trazables y listos para analisis.")
    quality = read_json(QUALITY_PATH)
    consolidation = read_json(CONSOLIDATION_PATH)
    source_rows = quality.get("sources", [])
    stages = pd.DataFrame(
        [
            {"Etapa": "RAW", "Estado": "Completada", "Evidencia": "Fuentes originales y contratos"},
            {"Etapa": "PROCESSED", "Estado": "Completada", "Evidencia": "Parquet por fuente"},
            {"Etapa": "CLEAN", "Estado": "Completada", "Evidencia": f"{len(source_rows)} reportes de calidad"},
            {"Etapa": "CONSOLIDATED", "Estado": "Completada", "Evidencia": f"{parquet_row_count(OBSERVATIONS_PATH) or 0:,} observaciones"},
        ]
    )
    st.dataframe(stages, use_container_width=True, hide_index=True)
    st.subheader("Linaje de la consolidacion")
    source_manifest = consolidation.get("sources", [])
    if source_manifest:
        st.dataframe(pd.DataFrame(source_manifest), use_container_width=True, hide_index=True)
    st.caption("Los datos grandes se leen por metadatos y muestras; la interfaz no carga el consolidado completo en memoria.")
    render_phase_navigation("ingenieria")
