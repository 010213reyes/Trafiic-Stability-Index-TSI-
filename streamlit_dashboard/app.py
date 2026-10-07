from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pyarrow.parquet as parquet
import streamlit as st


st.set_page_config(
    page_title="TSI | Avance del proyecto",
    page_icon="TSI",
    layout="wide",
)


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


ROOT = project_root()
DATA = ROOT / "data"
DOCS = ROOT / "docs" / "02_ingenieria_datos" / "sql"

CONTRACT_PATH = DATA / "00_raw" / "external" / "international_sources_contract.json"
QUALITY_PATH = DATA / "02_clean" / "external" / "international_clean_quality.json"
CONSOLIDATION_PATH = DATA / "02_clean" / "consolidated" / "international_consolidation_manifest.json"
OBSERVATIONS_PATH = DATA / "02_clean" / "consolidated" / "international_observations.parquet"
SQL_PLAN_PATH = DOCS / "00_planificacion" / "12_plan_fase_sql.md"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def parquet_row_count(path: Path) -> int | None:
    if not path.exists():
        return None
    return parquet.ParquetFile(path).metadata.num_rows


def parquet_preview(path: Path, rows: int = 12) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    parquet_file = parquet.ParquetFile(path)
    batch = next(parquet_file.iter_batches(batch_size=rows), None)
    return batch.to_pandas() if batch is not None else pd.DataFrame()


def exists_label(path: Path) -> str:
    return "Disponible" if path.exists() else "Pendiente"


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Acceso al dashboard TSI")
    st.caption("Demostracion del avance de la nueva investigacion")
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


contract = read_json(CONTRACT_PATH)
quality = read_json(QUALITY_PATH)
clean_sources = quality.get("sources", [])
quality_by_source = {item["source_id"]: item for item in clean_sources}
source_rows = []

for source in contract.get("sources", []):
    source_quality = quality_by_source.get(source["source_id"], {})
    source_rows.append(
        {
            "Ciudad": source["city"],
            "Fuente": source["source_id"],
            "Rol": source["role"],
            "Metrica": source["observed_variables"][1] if len(source["observed_variables"]) > 1 else source["observed_variables"][0],
            "Registros CLEAN": source_quality.get("output_rows", "N/D"),
            "Calidad": source_quality.get("status", "Pendiente"),
        }
    )


st.title("Traffic Stability Index")
st.caption("Demostracion visual del avance de la nueva investigacion multiciudad")
st.info(
    "Esta aplicacion muestra unicamente el avance de la nueva investigacion: fuentes internacionales, "
    "ingenieria RAW-PROCESSED-CLEAN-CONSOLIDATED y organizacion de la fase SQL."
)

total_rows = parquet_row_count(OBSERVATIONS_PATH)
metric_a, metric_b, metric_c, metric_d = st.columns(4)
with metric_a:
    st.metric("Fuentes aprobadas", len(source_rows))
with metric_b:
    st.metric("Fuentes CLEAN", len(clean_sources))
with metric_c:
    st.metric("Observaciones consolidadas", f"{total_rows:,}" if total_rows else "N/D")
with metric_d:
    st.metric("SQL", "Diseno listo" if SQL_PLAN_PATH.exists() else "Pendiente")

pipeline_tab, sources_tab, sql_tab = st.tabs(["Avance del pipeline", "Fuentes internacionales", "Fase SQL"])

with pipeline_tab:
    st.subheader("Avance demostrable")
    pipeline = pd.DataFrame(
        [
            {"Etapa": "RAW", "Estado": "Completada", "Evidencia": "Archivos originales y contrato de fuentes"},
            {"Etapa": "PROCESSED", "Estado": "Completada", "Evidencia": "Parquet por fuente"},
            {"Etapa": "CLEAN", "Estado": "Completada", "Evidencia": "Reporte de calidad internacional"},
            {"Etapa": "CONSOLIDATED", "Estado": "Completada", "Evidencia": "international_observations.parquet"},
            {"Etapa": "SQL", "Estado": "En organizacion", "Evidencia": "Modelo conceptual, logico y fisico documentado"},
            {"Etapa": "ANALISIS", "Estado": "Siguiente", "Evidencia": "EDA multiciudad despues de la base SQL"},
        ]
    )
    st.dataframe(pipeline, use_container_width=True, hide_index=True)

    st.subheader("Artefactos actuales")
    artifacts = pd.DataFrame(
        [
            {"Artefacto": "Contrato internacional", "Ruta": str(CONTRACT_PATH.relative_to(ROOT)), "Estado": exists_label(CONTRACT_PATH)},
            {"Artefacto": "Calidad CLEAN", "Ruta": str(QUALITY_PATH.relative_to(ROOT)), "Estado": exists_label(QUALITY_PATH)},
            {"Artefacto": "Consolidado internacional", "Ruta": str(OBSERVATIONS_PATH.relative_to(ROOT)), "Estado": exists_label(OBSERVATIONS_PATH)},
            {"Artefacto": "Manifiesto de consolidacion", "Ruta": str(CONSOLIDATION_PATH.relative_to(ROOT)), "Estado": exists_label(CONSOLIDATION_PATH)},
            {"Artefacto": "Plan de fase SQL", "Ruta": str(SQL_PLAN_PATH.relative_to(ROOT)), "Estado": exists_label(SQL_PLAN_PATH)},
        ]
    )
    st.dataframe(artifacts, use_container_width=True, hide_index=True)

with sources_tab:
    st.subheader("Fuentes internacionales aprobadas")
    st.dataframe(pd.DataFrame(source_rows), use_container_width=True, hide_index=True)
    st.caption("Las metricas se mantienen separadas: velocidad, intensidad, indice y longitud de congestion no son equivalentes.")

    if source_rows:
        selected_city = st.selectbox("Selecciona una ciudad para ver su contrato", [row["Ciudad"] for row in source_rows])
        selected = next(row for row in contract["sources"] if row["city"] == selected_city)
        st.write(
            {
                "ciudad": selected["city"],
                "pais": selected["country"],
                "zona_horaria": selected["timezone"],
                "rol": selected["role"],
                "variables": selected["observed_variables"],
                "estado": selected["status"],
            }
        )
        dataset_path = DATA / "02_clean" / "external" / f"{selected['source_id']}_clean.parquet"
        st.markdown("#### Muestra del dataset CLEAN")
        st.caption(f"Archivo: {dataset_path.relative_to(ROOT)} | Registros disponibles: {parquet_row_count(dataset_path) or 'N/D'}")
        preview = parquet_preview(dataset_path)
        if preview.empty:
            st.warning("No existe un dataset CLEAN local para esta fuente.")
        else:
            st.dataframe(preview, use_container_width=True, hide_index=True)

with sql_tab:
    st.subheader("Organizacion de la base SQL")
    st.write("La base SQL todavia no carga el consolidado completo. Esta pantalla demuestra el diseno previo a la implementacion.")
    sql_steps = pd.DataFrame(
        [
            {"Subfase": "SQL-01", "Estado": "Completada", "Salida": "Preguntas y limites"},
            {"Subfase": "SQL-02", "Estado": "Completada", "Salida": "Modelo conceptual"},
            {"Subfase": "SQL-03", "Estado": "Completada", "Salida": "Modelo logico"},
            {"Subfase": "SQL-04", "Estado": "Completada", "Salida": "Politica de metricas"},
            {"Subfase": "SQL-05", "Estado": "Completada", "Salida": "Modelo fisico MySQL"},
            {"Subfase": "SQL-06", "Estado": "Completada", "Salida": "Guia de diagrama EER"},
            {"Subfase": "SQL-07", "Estado": "Completada", "Salida": "Carga internacional de prueba validada"},
            {"Subfase": "SQL-08", "Estado": "Siguiente", "Salida": "Carga controlada del consolidado"},
        ]
    )
    st.dataframe(sql_steps, use_container_width=True, hide_index=True)
    st.warning("La carga SQL y las consultas de validacion se realizaran despues de revisar el modelo visual en MySQL Workbench.")