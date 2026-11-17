
from __future__ import annotations

import pandas as pd
import streamlit as st

from components import (
    render_phase_explanation,
    render_phase_header,
    render_phase_navigation,
    render_pipeline_runner,
)
from config import (
    ANOMALY_SUMMARY_PATH,
    INFERENCE_METADATA_PATH,
    MODEL_METRICS_PATH,
    MODEL_REGISTRY_PATH,
    MONITORING_PATH,
    PREDICTIONS_PATH,
    latest_model_manifest_path,
    read_csv,
    read_json,
)
from services.databricks_client import obtener_predicciones_mlops


def render() -> None:
    render_phase_header(
        "05",
        "MLOps",
        "Consulta predicciones historicas, registros de modelos y resultados de monitoreo.",
    )

    render_phase_explanation(
        "El resultado se vuelve operable",
        "MLOps permite consultar resultados experimentales, revisar versiones "
        "y supervisar el comportamiento de los modelos.",
        "Modelos registrados y artefactos de evaluacion",
        "Predicciones historicas y metricas de monitoreo",
    )

    # Conservamos el componente original del proyecto.
    render_pipeline_runner()

    selected_model = st.session_state.get(
        "last_pipeline_model", "random_forest"
    )

    model_families = {
        "random_forest": "rf_tsi_internacional",
        "ridge": "ridge_tsi_internacional",
        "baseline": "baseline_persistencia_tsi",
    }

    model_family = model_families.get(
        selected_model, "rf_tsi_internacional"
    )

    manifest_path = latest_model_manifest_path(model_family)
    manifest = read_json(manifest_path)
    inference = read_json(INFERENCE_METADATA_PATH)
    monitoring = read_json(MONITORING_PATH)

    is_operational_model = selected_model == "random_forest"

    if not manifest:
        st.warning(
            "No existe un registro local para el modelo seleccionado."
        )
        render_phase_navigation("mlops")
        return

    if st.session_state.pop("pipeline_run_completed", False):
        st.success(
            "Ejecucion local completada. "
            "Se muestran los artefactos registrados."
        )

    performance = (
        monitoring.get("performance", {})
        if is_operational_model
        else manifest.get("evaluation_metrics", {})
    )

    metrics = st.columns(4)

    metrics[0].metric(
        "Modelo seleccionado",
        str(manifest.get("model_name", "N/D"))
        .replace("_", " ")
        .title(),
    )

    metrics[1].metric(
        "Version",
        str(manifest.get("model_version", "N/D")),
    )

    mae = performance.get("mae")

    metrics[2].metric(
        "MAE local",
        f"{mae:.3f}" if isinstance(mae, (int, float)) else "N/D",
    )

    metrics[3].metric(
        "Estado",
        "Seleccionado" if is_operational_model else "Registrado",
    )

    if is_operational_model:
        st.write({
            "ejecucion_utc": inference.get("run_at_utc"),
            "hash_entrada": inference.get("input_sha256"),
            "filas_omitidas": inference.get(
                "rows_skipped_incomplete"
            ),
        })

    st.subheader("Registro del modelo")

    st.dataframe(
        pd.DataFrame([
            {
                "Campo": "Estado",
                "Valor": (
                    "Seleccionado"
                    if is_operational_model
                    else "Evaluado y registrado"
                ),
            },
            {
                "Campo": "Algoritmo",
                "Valor": manifest.get("model_name", "N/D"),
            },
            {
                "Campo": "Objetivo",
                "Valor": manifest.get("task", "N/D"),
            },
            {
                "Campo": "Creado UTC",
                "Valor": manifest.get("created_at_utc", "N/D"),
            },
            {
                "Campo": "Hash de datos",
                "Valor": manifest.get("data", {}).get(
                    "sha256", "N/D"
                ),
            },
        ]),
        width="stretch",
        hide_index=True,
    )

    st.subheader("Historial de modelos evaluados")

    model_metrics = read_csv(MODEL_METRICS_PATH)

    if not model_metrics.empty:
        model_metrics = model_metrics.rename(
            columns={
                "modelo": "Algoritmo",
                "mae": "MAE",
                "rmse": "RMSE",
                "r2": "R2",
            }
        )

        if "Algoritmo" in model_metrics.columns:
            model_metrics["Estado"] = (
                model_metrics["Algoritmo"]
                .map({
                    "random_forest": "Seleccionado",
                    "ridge": "Evaluado",
                    "baseline_persistencia": "Referencia",
                })
                .fillna("Evaluado")
            )

        st.dataframe(
            model_metrics,
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No hay metricas comparativas locales disponibles.")

    st.subheader("Historial de versiones registradas")

    registered_models = []

    for registered_path in sorted(
        MODEL_REGISTRY_PATH.glob("*/manifest.json")
    ):
        registered = read_json(registered_path)

        registered_models.append({
            "Version": registered.get(
                "model_version", registered_path.parent.name
            ),
            "Algoritmo": registered.get("model_name", "N/D"),
            "Estado": (
                "Seleccionado"
                if registered.get("model_version")
                == manifest.get("model_version")
                else registered.get("status", "Registrado")
            ),
            "Creado UTC": registered.get("created_at_utc", "N/D"),
            "Hash datos": str(
                registered.get("data", {}).get("sha256", "N/D")
            )[:12],
        })

    if registered_models:
        st.dataframe(
            pd.DataFrame(registered_models),
            width="stretch",
            hide_index=True,
        )

    st.subheader("Historial de ejecuciones")

    if is_operational_model:
        execution_row = {
            "Ejecucion UTC": inference.get("run_at_utc", "N/D"),
            "Version": inference.get("model_version", "N/D"),
            "Filas entrada": inference.get("rows_input", "N/D"),
            "Filas inferidas": inference.get(
                "rows_inferred", "N/D"
            ),
            "Estado": str(
                monitoring.get("status", "N/D")
            ).upper(),
            "MAE": performance.get("mae", "N/D"),
            "RMSE": performance.get("rmse", "N/D"),
        }
    else:
        execution_row = {
            "Ejecucion UTC": manifest.get(
                "created_at_utc", "N/D"
            ),
            "Version": manifest.get("model_version", "N/D"),
            "Filas entrada": manifest.get(
                "rows", {}
            ).get("features_input", "N/D"),
            "Filas inferidas": "No aplica",
            "Estado": "REGISTRADO",
            "MAE": performance.get("mae", "N/D"),
            "RMSE": performance.get("rmse", "N/D"),
        }

    st.dataframe(
        pd.DataFrame([execution_row]),
        width="stretch",
        hide_index=True,
    )

    st.subheader("Metricas y controles locales")

    st.dataframe(
        pd.DataFrame([
            {
                "Metrica": "MAE",
                "Valor": performance.get("mae"),
            },
            {
                "Metrica": "RMSE",
                "Valor": performance.get("rmse"),
            },
            {
                "Metrica": "P95 error absoluto",
                "Valor": performance.get(
                    "p95_error_absoluto"
                ),
            },
            {
                "Metrica": "Drift maximo",
                "Valor": monitoring.get(
                    "drift_max_mean_shift"
                ),
            },
        ]),
        width="stretch",
        hide_index=True,
    )

    checks = (
        monitoring.get("checks", [])
        if is_operational_model
        else []
    )

    if checks:
        checks_table = pd.DataFrame(checks)
        columns = [
            col
            for col in ["name", "value", "status", "detail"]
            if col in checks_table.columns
        ]

        st.dataframe(
            checks_table[columns],
            width="stretch",
            hide_index=True,
        )

    if is_operational_model:
        st.subheader("Predicciones historicas de Databricks")

        try:
            predicciones_db = obtener_predicciones_mlops()

            if predicciones_db.empty:
                st.info(
                    "La consulta no devolvio predicciones."
                )
            else:
                st.success(
                    "Datos consultados desde Databricks SQL."
                )

                st.caption(
                    "Fuente: workspace.tsi."
                    "pems_bay_predicciones_v2 | "
                    "Muestra de hasta 100 registros del test."
                )

                st.metric(
                    "Registros consultados",
                    len(predicciones_db),
                )

                st.dataframe(
                    predicciones_db,
                    width="stretch",
                    hide_index=True,
                )

        except Exception:
            st.warning(
                "Databricks no esta disponible. "
                "Se intentaran mostrar los datos locales."
            )

            predicciones_locales = read_csv(
                PREDICTIONS_PATH
            )

            if not predicciones_locales.empty:
                st.dataframe(
                    predicciones_locales.head(25),
                    width="stretch",
                    hide_index=True,
                )
            else:
                st.info(
                    "No hay predicciones locales disponibles."
                )

        st.subheader("Resumen exploratorio de anomalias")

        anomalies = read_csv(ANOMALY_SUMMARY_PATH)

        if not anomalies.empty:
            st.dataframe(
                anomalies,
                width="stretch",
                hide_index=True,
            )
        else:
            st.info(
                "No hay un resumen local de anomalias."
            )

        st.info(
            "Random Forest V2 fue seleccionado para el "
            "pronostico horario experimental del TSI en "
            "PEMS-BAY. Las predicciones son historicas, "
            "no inferencias en tiempo real. "
            "La validacion en Guadalajara esta pendiente."
        )

    else:
        st.info(
            f"{manifest.get('model_name', 'Modelo')} "
            "se registro como modelo comparativo. "
            "Random Forest permanece como modelo "
            "seleccionado del ciclo internacional."
        )

    render_phase_navigation("mlops")
