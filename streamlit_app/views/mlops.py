from __future__ import annotations

import pandas as pd
import streamlit as st

from components import render_phase_explanation, render_phase_header, render_phase_navigation, render_pipeline_runner
from config import ANOMALY_SUMMARY_PATH, INFERENCE_METADATA_PATH, MODEL_MANIFEST_PATH, MODEL_METRICS_PATH, MODEL_REGISTRY_PATH, MONITORING_PATH, PREDICTIONS_PATH, latest_model_manifest_path, read_csv, read_json


def render() -> None:
    render_phase_header("05", "MLOps", "Opera el modelo registrado, genera inferencia reproducible y supervisa sus resultados.")
    render_phase_explanation(
        "El resultado se vuelve operable",
        "MLOps fija la version del modelo y el hash de entrada, ejecuta inferencia sin reentrenar y registra controles para detectar problemas de calidad o drift.",
        "Modelo Joblib y manifest JSON",
        "Predicciones, metadatos y reporte de monitoreo",
    )
    render_pipeline_runner()
    selected_model = st.session_state.get("last_pipeline_model", "random_forest")
    model_families = {
        "random_forest": "rf_tsi_internacional",
        "ridge": "ridge_tsi_internacional",
        "baseline": "baseline_persistencia_tsi",
    }
    manifest_path = latest_model_manifest_path(model_families.get(selected_model, "rf_tsi_internacional"))
    manifest = read_json(manifest_path)
    inference = read_json(INFERENCE_METADATA_PATH)
    monitoring = read_json(MONITORING_PATH)
    is_operational_model = selected_model == "random_forest"
    if not manifest:
        st.warning("No existe un registro para el modelo seleccionado.")
        render_phase_navigation("mlops")
        return

    if st.session_state.pop("pipeline_run_completed", False):
        st.success("Ejecucion completada. Estos son los artefactos registrados por el flujo.")

    performance = monitoring.get("performance", {}) if is_operational_model else manifest.get("evaluation_metrics", {})
    metrics = st.columns(4)
    metrics[0].metric("Modelo seleccionado", manifest.get("model_name", "N/D").replace("_", " ").title())
    metrics[1].metric("Version", manifest.get("model_version", "N/D"))
    metrics[2].metric("MAE", f"{performance.get('mae', 0):.3f}")
    metrics[3].metric("Estado", "Activo" if is_operational_model else "Registrado")
    if is_operational_model:
        st.write({"ejecucion_utc": inference.get("run_at_utc"), "hash_entrada": inference.get("input_sha256"), "filas_omitidas": inference.get("rows_skipped_incomplete")})

    st.subheader("Registro del modelo")
    st.dataframe(pd.DataFrame([
        {"Campo": "Estado", "Valor": "Activo" if is_operational_model else "Evaluado y registrado"},
        {"Campo": "Algoritmo", "Valor": manifest.get("model_name", "N/D")},
        {"Campo": "Objetivo", "Valor": manifest.get("task", "N/D")},
        {"Campo": "Creado UTC", "Valor": manifest.get("created_at_utc", "N/D")},
        {"Campo": "Hash de datos", "Valor": manifest.get("data", {}).get("sha256", "N/D")},
    ]), use_container_width=True, hide_index=True)

    st.subheader("Historial de modelos evaluados")
    model_metrics = read_csv(MODEL_METRICS_PATH)
    if not model_metrics.empty:
        model_metrics = model_metrics.rename(columns={"modelo": "Algoritmo", "mae": "MAE", "rmse": "RMSE", "r2": "R2"})
        model_metrics["Estado"] = model_metrics["Algoritmo"].map(
            {"random_forest": "Seleccionado", "ridge": "Evaluado", "baseline_persistencia": "Referencia"}
        ).fillna("Evaluado")
        st.dataframe(model_metrics, use_container_width=True, hide_index=True)

    st.subheader("Historial de versiones registradas")
    registered_models = []
    for manifest_path in sorted(MODEL_REGISTRY_PATH.glob("*/manifest.json")):
        registered = read_json(manifest_path)
        registered_models.append(
            {
                "Version": registered.get("model_version", manifest_path.parent.name),
                "Algoritmo": registered.get("model_name", "N/D"),
                "Estado": "Seleccionado" if registered.get("model_version") == manifest.get("model_version") else registered.get("status", "Registrado"),
                "Creado UTC": registered.get("created_at_utc", "N/D"),
                "Hash datos": registered.get("data", {}).get("sha256", "N/D")[:12],
            }
        )
    if registered_models:
        st.dataframe(pd.DataFrame(registered_models), use_container_width=True, hide_index=True)

    st.subheader("Historial de ejecuciones")
    if is_operational_model:
        execution_row = {
            "Ejecucion UTC": inference.get("run_at_utc", "N/D"),
            "Version": inference.get("model_version", "N/D"),
            "Filas entrada": inference.get("rows_input", "N/D"),
            "Filas inferidas": inference.get("rows_inferred", "N/D"),
            "Estado": monitoring.get("status", "N/D").upper(),
            "MAE": performance.get("mae", "N/D"),
            "RMSE": performance.get("rmse", "N/D"),
        }
    else:
        execution_row = {
            "Ejecucion UTC": manifest.get("created_at_utc", "N/D"),
            "Version": manifest.get("model_version", "N/D"),
            "Filas entrada": manifest.get("rows", {}).get("features_input", "N/D"),
            "Filas inferidas": "No aplica",
            "Estado": "REGISTRADO",
            "MAE": performance.get("mae", "N/D"),
            "RMSE": performance.get("rmse", "N/D"),
        }
    st.dataframe(pd.DataFrame([execution_row]), use_container_width=True, hide_index=True)

    st.subheader("Metricas y controles")
    st.dataframe(pd.DataFrame([
        {"Metrica": "MAE", "Valor": performance.get("mae")},
        {"Metrica": "RMSE", "Valor": performance.get("rmse")},
        {"Metrica": "P95 error absoluto", "Valor": performance.get("p95_error_absoluto")},
        {"Metrica": "Drift maximo", "Valor": monitoring.get("drift_max_mean_shift")},
    ]), use_container_width=True, hide_index=True)
    checks = monitoring.get("checks", []) if is_operational_model else []
    if checks:
        checks_table = pd.DataFrame(checks)
        st.dataframe(checks_table[["name", "value", "status", "detail"]], use_container_width=True, hide_index=True)

    if is_operational_model:
        st.subheader("Predicciones y anomalias")
        st.dataframe(read_csv(PREDICTIONS_PATH).head(25), use_container_width=True, hide_index=True)
        anomalies = read_csv(ANOMALY_SUMMARY_PATH)
        if not anomalies.empty:
            st.dataframe(anomalies, use_container_width=True, hide_index=True)
        st.info("Random Forest es el modelo activo del ciclo internacional. El TSI es provisional por fuente y la validacion de anomalias es exploratoria.")
    else:
        st.info(f"{manifest.get('model_name', 'Modelo')} se registro como comparativo. Random Forest permanece como modelo activo de inferencia.")
    render_phase_navigation("mlops")
