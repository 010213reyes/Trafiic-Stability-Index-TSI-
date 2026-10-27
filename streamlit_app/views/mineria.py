from __future__ import annotations

import pandas as pd
import streamlit as st

from components import render_phase_explanation, render_phase_header, render_phase_navigation
from config import CONTRACT_PATH, QUALITY_PATH, read_json


def render() -> None:
    render_phase_header("01", "Mineria de datos", "Define las fuentes, variables y limites antes de transformar los datos.")
    render_phase_explanation(
        "Primero entendemos el problema",
        "Se identifican fuentes publicas, variables observables y riesgos de comparacion antes de construir el pipeline. Guadalajara se conserva como destino de calibracion futura.",
        "Catalogo de fuentes y definiciones",
        "Contrato internacional y decisiones de alcance",
    )
    contract = read_json(CONTRACT_PATH)
    quality = read_json(QUALITY_PATH)
    quality_by_source = {item["source_id"]: item for item in quality.get("sources", [])}
    rows = []
    for source in contract.get("sources", []):
        source_quality = quality_by_source.get(source["source_id"], {})
        rows.append(
            {
                "Ciudad": source["city"],
                "Fuente": source["source_id"],
                "Rol": source["role"],
                "Variables": ", ".join(source.get("observed_variables", [])),
                "Registros CLEAN": source_quality.get("output_rows", "N/D"),
                "Calidad": source_quality.get("status", "Pendiente"),
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.subheader("Decisiones de minería")
    st.write("Las fuentes conservan su semantica original. Istanbul, Madrid, METR-LA, PEMS-BAY y Sao Paulo sirven para transferencia y comparacion; Guadalajara queda reservada para calibracion local.")
    render_phase_navigation("mineria")
