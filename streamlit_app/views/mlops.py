from __future__ import annotations

import pandas as pd
import streamlit as st

from components import render_phase_header, render_phase_navigation
from config import ANOMALY_SUMMARY_PATH, INFERENCE_METADATA_PATH, MODEL_MANIFEST_PATH, MONITORING_PATH, PREDICTIONS_PATH, read_csv, read_json


def render() -> None:
    render_phase_header("05", "MLOps", "Opera el modelo registrado, genera inferencia reproducible y supervisa sus resultados.")
    manifest = read_json(MODEL_MANIFEST_PATH)
    inference = read_json(INFERENCE_METADATA_PATH)
    monitoring = read_json(MONITORING_PATH)
    if not manifest or not inference or not monitoring or not PREDICTIONS_PATH.exists():
        st.warning("Faltan artefactos MLOps. Ejecute inferencia y monitoreo antes de consultar esta fase.")
        render_phase_navigation("mlops")
        return

    performance = monitoring.get("performance", {})
    metrics = st.columns(4)
    metrics[0].metric("Version", manifest.get("model_version", "N/D"))
    metrics[1].metric("Predicciones", f"{inference.get('rows_inferred', 0):,}")
    metrics[2].metric("MAE", f"{performance.get('mae', 0):.3f}")
    metrics[3].metric("Monitoreo", monitoring.get("status", "N/D").upper())
    st.write({"ejecucion_utc": inference.get("run_at_utc"), "hash_entrada": inference.get("input_sha256"), "filas_omitidas": inference.get("rows_skipped_incomplete")})

    st.subheader("Metricas y controles")
    st.dataframe(pd.DataFrame([
        {"Metrica": "MAE", "Valor": performance.get("mae")},
        {"Metrica": "RMSE", "Valor": performance.get("rmse")},
        {"Metrica": "P95 error absoluto", "Valor": performance.get("p95_error_absoluto")},
        {"Metrica": "Drift maximo", "Valor": monitoring.get("drift_max_mean_shift")},
    ]), use_container_width=True, hide_index=True)
    checks = monitoring.get("checks", [])
    if checks:
        checks_table = pd.DataFrame(checks)
        st.dataframe(checks_table[["name", "value", "status", "detail"]], use_container_width=True, hide_index=True)

    st.subheader("Predicciones y anomalias")
    st.dataframe(read_csv(PREDICTIONS_PATH).head(25), use_container_width=True, hide_index=True)
    anomalies = read_csv(ANOMALY_SUMMARY_PATH)
    if not anomalies.empty:
        st.dataframe(anomalies, use_container_width=True, hide_index=True)
    st.warning("El modelo es candidato internacional; el TSI es provisional y las anomalias no tienen ground truth externo.")
    render_phase_navigation("mlops")
