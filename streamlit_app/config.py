from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pyarrow.parquet as parquet


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SQL_DOCS = ROOT / "docs" / "02_ingenieria_datos" / "sql"

CONTRACT_PATH = DATA / "00_raw" / "external" / "international_sources_contract.json"
QUALITY_PATH = DATA / "02_clean" / "external" / "international_clean_quality.json"
CONSOLIDATION_PATH = DATA / "02_clean" / "consolidated" / "international_consolidation_manifest.json"
OBSERVATIONS_PATH = DATA / "02_clean" / "consolidated" / "international_observations.parquet"
SQL_PLAN_PATH = SQL_DOCS / "00_planificacion" / "12_plan_fase_sql.md"

EXPERIMENT_PATH = DATA / "04_model_output" / "results" / "resumen_experimento_internacional.json"
VALIDATION_PATH = DATA / "04_model_output" / "validation" / "metricas_por_fuente.csv"
MODEL_MANIFEST_PATH = DATA / "05_mlops" / "model_registry" / "rf_tsi_internacional_v1.0.0" / "manifest.json"
INFERENCE_METADATA_PATH = DATA / "05_mlops" / "inference" / "predicciones_tsi.json"
PREDICTIONS_PATH = DATA / "05_mlops" / "inference" / "predicciones_tsi.csv"
MONITORING_PATH = DATA / "05_mlops" / "monitoring" / "reporte_monitoreo.json"
ANOMALY_SUMMARY_PATH = DATA / "04_model_output" / "anomalies" / "resumen_anomalias.csv"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


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
