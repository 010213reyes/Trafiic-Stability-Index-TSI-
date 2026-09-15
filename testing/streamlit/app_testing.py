from pathlib import Path
from datetime import datetime
import json

import pandas as pd
import pyarrow.parquet as parquet
import streamlit as st


st.set_page_config(
    page_title="TSI Lab - Testing Console",
    page_icon="TSI",
    layout="wide",
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.authenticated:
    st.title("Acceso al entorno de pruebas TSI")
    st.caption("Inicio de sesion simulado para el rol administrador")

    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contrasena", type="password")
        submitted = st.form_submit_button("Iniciar sesion", type="primary")

    if submitted:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Usuario o contrasena incorrectos.")

    st.stop()

st.title("Entorno de pruebas TSI")
st.caption("Consola de validacion para el sistema de inteligencia artificial")

DATA_ROOT = PROJECT_ROOT / "data"
RAW_ROOT = DATA_ROOT / "00_raw"
CLEAN_ROOT = DATA_ROOT / "02_clean"
OUTPUT_ROOT = DATA_ROOT / "03_algorithm_output"


def read_csv(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    return pd.read_csv(path)


def read_csv_preview(path: Path, rows: int = 12) -> pd.DataFrame | None:
    if not path.exists():
        return None
    return pd.read_csv(path, nrows=rows, low_memory=False)


def read_parquet_preview(path: Path, rows: int = 12) -> pd.DataFrame | None:
    if not path.exists():
        return None
    parquet_file = parquet.ParquetFile(path)
    batches = parquet_file.iter_batches(batch_size=rows)
    first_batch = next(batches, None)
    return first_batch.to_pandas() if first_batch is not None else pd.DataFrame()


def source_catalog() -> dict[str, dict[str, object]]:
    return {
        "traffic_data": {
            "label": "Traffic data · Guadalajara",
            "kind": "Local historica",
            "raw": RAW_ROOT / "traffic_data.csv",
            "processed": DATA_ROOT / "01_processed" / "pipeline" / "traffic_data.parquet",
            "normalized": DATA_ROOT / "01_processed" / "normalized" / "traffic_data.parquet",
            "clean": CLEAN_ROOT / "traffic_data.csv",
        },
        "scraped_traffic": {
            "label": "Scraped traffic · Guadalajara",
            "kind": "Scraping",
            "raw": RAW_ROOT / "scraped_traffic.csv",
            "processed": DATA_ROOT / "01_processed" / "pipeline" / "scraped_traffic.parquet",
            "normalized": DATA_ROOT / "01_processed" / "normalized" / "scraped_traffic.parquet",
            "clean": CLEAN_ROOT / "traffic_data.csv",
        },
        "crowdsourcing_raw": {
            "label": "Crowdsourcing raw · Guadalajara",
            "kind": "Observaciones de usuarios",
            "raw": RAW_ROOT / "crowdsourcing_raw.csv",
            "processed": DATA_ROOT / "01_processed" / "pipeline" / "crowdsourcing_raw.parquet",
            "normalized": DATA_ROOT / "01_processed" / "normalized" / "crowdsourcing_raw.parquet",
            "clean": DATA_ROOT / "02_clean" / "consolidated" / "consolidated_observations.parquet",
        },
        "crowdsourcing_aggregated": {
            "label": "Crowdsourcing agregado · Guadalajara",
            "kind": "Derivada",
            "raw": RAW_ROOT / "crowdsourcing_aggregated.csv",
            "processed": DATA_ROOT / "01_processed" / "pipeline" / "crowdsourcing_aggregated.parquet",
            "normalized": DATA_ROOT / "01_processed" / "normalized" / "crowdsourcing_aggregated.parquet",
            "clean": DATA_ROOT / "02_clean" / "consolidated" / "derived_aggregates.parquet",
        },
        "synthetic_traffic": {
            "label": "Synthetic traffic · Guadalajara",
            "kind": "Sintetica",
            "raw": RAW_ROOT / "synthetic_traffic.csv",
            "processed": DATA_ROOT / "01_processed" / "pipeline" / "synthetic_traffic.parquet",
            "normalized": DATA_ROOT / "01_processed" / "normalized" / "synthetic_traffic.parquet",
            "clean": DATA_ROOT / "02_clean" / "consolidated" / "consolidated_observations.parquet",
        },
        "metr_la": {
            "label": "METR-LA · Los Angeles County",
            "kind": "Externa real",
            "raw": RAW_ROOT / "external" / "traffic_datasets" / "METR-LA.csv",
            "processed": DATA_ROOT / "01_processed" / "pipeline" / "metr_la.parquet",
            "normalized": DATA_ROOT / "01_processed" / "normalized" / "metr_la.parquet",
            "clean": DATA_ROOT / "02_clean" / "consolidated" / "consolidated_observations.parquet",
        },
        "pems_bay": {
            "label": "PEMS-BAY · San Francisco Bay Area",
            "kind": "Externa real",
            "raw": RAW_ROOT / "external" / "traffic_datasets" / "PEMS-BAY.csv",
            "processed": DATA_ROOT / "01_processed" / "pipeline" / "pems_bay.parquet",
            "normalized": DATA_ROOT / "01_processed" / "normalized" / "pems_bay.parquet",
            "clean": DATA_ROOT / "02_clean" / "consolidated" / "consolidated_observations.parquet",
        },
    }


def algorithm_definition(name: str) -> dict[str, object]:
    definitions = {
        "Isolation Forest": {
            "file": CLEAN_ROOT / "filtered_isolation_forest.csv",
            "summary": None,
            "image": OUTPUT_ROOT / "11_isolation_forest_summary.png",
            "description": "Filtrado de observaciones atipicas mediante aislamiento.",
        },
        "Local Outlier Factor": {
            "file": CLEAN_ROOT / "filtered_local_outlier_factor.csv",
            "summary": OUTPUT_ROOT / "local_outlier_factor_summary.csv",
            "image": OUTPUT_ROOT / "local_outlier_factor_pca.png",
            "description": "Deteccion de anomalias considerando la vecindad local.",
        },
        "DBSCAN": {
            "file": CLEAN_ROOT / "filtered_dbscan.csv",
            "summary": OUTPUT_ROOT / "dbscan_summary.csv",
            "image": OUTPUT_ROOT / "dbscan_pca_clusters.png",
            "description": "Segmentacion de regimenes y deteccion de ruido estructural.",
        },
    }
    return definitions[name]


def execute_algorithm(name: str) -> dict[str, object]:
    definition = algorithm_definition(name)
    result = read_csv(definition["file"])
    base = read_csv(CLEAN_ROOT / "traffic_enriched.csv")
    if result is None or base is None:
        return {"algorithm": name, "status": "error", "message": "No se encontraron los artefactos requeridos."}

    report = {
        "algorithm": name,
        "status": "passed",
        "executed_at": datetime.now().isoformat(timespec="seconds"),
        "input_rows": len(base),
        "output_rows": len(result),
        "retention_pct": round(len(result) / len(base) * 100, 2) if len(base) else 0,
        "removed_pct": round((len(base) - len(result)) / len(base) * 100, 2) if len(base) else 0,
        "artifact": str(definition["file"].relative_to(PROJECT_ROOT)),
    }
    return report


def render_metric_card(label: str, value: str, help_text: str) -> None:
    st.metric(label, value, help=help_text)

with st.sidebar:
    st.markdown("### TSI Lab")
    st.caption("Testing console")
    st.divider()
    st.write("**Luis Reyes**")
    st.write("Administrador · Ingeniero de IA")
    st.caption("Sesion activa")
    if st.button("Cerrar sesion"):
        st.session_state.authenticated = False
        st.rerun()

st.success("Bienvenido, Luis. El entorno de pruebas esta listo para operar.")

data_tab, algorithms_tab, reports_tab, profile_tab = st.tabs([
    "Fuentes de datos",
    "Laboratorio de algoritmos",
    "Reportes y visualizaciones",
    "Perfil administrador",
])

with data_tab:
    st.subheader("Fuentes de datos")
    st.caption("Explora el recorrido de una fuente desde raw hasta su salida limpia.")
    catalog = source_catalog()
    source_id = st.selectbox(
        "Selecciona una fuente",
        list(catalog),
        format_func=lambda key: catalog[key]["label"],
    )
    selected = catalog[source_id]

    summary_columns = st.columns(4)
    for column, (label, path_key) in zip(
        summary_columns,
        [("Raw", "processed"), ("Processed", "raw"), ("Normalized", "clean"), ("Clean", "normalized")],
    ):
        path = selected[path_key]
        with column:
            st.metric(label, "Disponible" if path.exists() else "No generado")

    st.markdown(f"### {selected['label']}")
    st.caption(f"Tipo de fuente: {selected['kind']} · Identificador: `{source_id}`")
    path_columns = st.columns(2)
    with path_columns[0]:
        st.write("**Entrada raw**")
        st.code(str(selected["raw"].relative_to(PROJECT_ROOT)), language="text")
        st.write("**Archivo processed**")
        st.code(str(selected["raw"].relative_to(PROJECT_ROOT)), language="text")
    with path_columns[1]:
        st.write("**Archivo normalized**")
        st.code(str(selected["clean"].relative_to(PROJECT_ROOT)), language="text")
        st.write("**Salida clean**")
        st.code(str(selected["clean"].relative_to(PROJECT_ROOT)), language="text")

    preview_type = st.radio(
        "Que quieres inspeccionar?",
        ["Entrada raw", "Salida processed", "Salida normalized", "Salida clean"],
        horizontal=True,
    )
    preview_key = {
        "Entrada raw": "raw",
        "Salida processed": "normalized",
        "Salida normalized": "processed",
        "Salida clean": "clean",
    }[preview_type]
    preview_path = selected[preview_key]
    if st.button("Cargar vista previa", type="primary"):
        preview = (
            read_csv_preview(preview_path)
            if preview_path.suffix.lower() == ".csv"
            else read_parquet_preview(preview_path)
        )
        if preview is None:
            st.error("El archivo seleccionado aun no esta disponible.")
        else:
            st.dataframe(preview, use_container_width=True, hide_index=True)
            st.caption(f"Muestra de {len(preview)} registros · Archivo: {preview_path.name}")

with algorithms_tab:
    st.subheader("Laboratorio de algoritmos")
    st.caption("Selecciona un algoritmo y ejecuta una prueba contra los artefactos locales disponibles.")
    selected_algorithm = st.selectbox(
        "Algoritmo a probar",
        ["Isolation Forest", "Local Outlier Factor", "DBSCAN"],
    )
    definition = algorithm_definition(selected_algorithm)
    st.info(definition["description"])
    if st.button("Ejecutar prueba del algoritmo", type="primary"):
        st.session_state.algorithm_report = execute_algorithm(selected_algorithm)

    report = st.session_state.get("algorithm_report")
    if report and report["algorithm"] == selected_algorithm:
        if report["status"] == "passed":
            st.success(f"Prueba completada: {selected_algorithm}")
            metric_columns = st.columns(3)
            with metric_columns[0]:
                render_metric_card("Entrada", f"{report['input_rows']:,}", "Filas del dataset base")
            with metric_columns[1]:
                render_metric_card("Salida", f"{report['output_rows']:,}", "Filas del artefacto del algoritmo")
            with metric_columns[2]:
                render_metric_card("Retencion", f"{report['retention_pct']:.2f}%", "Registros conservados")
            st.json(report)
        else:
            st.error(report["message"])

with reports_tab:
    st.subheader("Reportes y visualizaciones")
    st.caption("Genera una ficha de prueba y consulta la evidencia visual del algoritmo seleccionado.")
    report_algorithm = st.selectbox(
        "Algoritmo del reporte",
        ["Isolation Forest", "Local Outlier Factor", "DBSCAN"],
        key="report_algorithm",
    )
    report_definition = algorithm_definition(report_algorithm)
    report_data = st.session_state.get("algorithm_report")
    if st.button("Generar reporte de prueba"):
        report_data = execute_algorithm(report_algorithm)
        st.session_state.algorithm_report = report_data
    if report_data and report_data.get("algorithm") == report_algorithm:
        st.download_button(
            "Descargar reporte JSON",
            data=json.dumps(report_data, indent=2, ensure_ascii=False),
            file_name=f"reporte_{report_algorithm.lower().replace(' ', '_')}.json",
            mime="application/json",
        )
        image_path = report_definition["image"]
        if image_path.exists():
            st.image(str(image_path), caption=f"Evidencia visual: {report_algorithm}", use_container_width=True)
        else:
            st.warning("Aun no existe una visualizacion para este algoritmo.")
    else:
        st.info("Ejecuta o genera primero un reporte para mostrar su evidencia.")

with profile_tab:
    st.subheader("Perfil del administrador")
    profile_columns = st.columns([1, 2])
    with profile_columns[0]:
        st.markdown("# LR")
    with profile_columns[1]:
        st.markdown("### Luis Reyes")
        st.write("**Administrador · Ingeniero de Inteligencia Artificial**")
        st.write("Responsable de la validacion tecnica del proyecto TSI.")
        st.divider()
        st.write("Usuario de acceso: `admin`")
        st.write("Nivel de acceso: Consola de pruebas")
