from __future__ import annotations

import io
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "00_raw" / "external"
OUTPUT_DIR = PROJECT_ROOT / "data" / "01_processed" / "external"
REPORT_DIR = PROJECT_ROOT / "data" / "01_processed" / "quality"

NUMERIC_COLUMNS = [
    "latitud",
    "longitud",
    "velocidad_kmh",
    "flujo_veh_h",
    "ocupacion_pct",
    "densidad_veh_km",
    "tiempo_viaje_seg",
    "congestion_longitud_m",
    "intensidad_fuente",
    "carga_fuente",
    "vmed_fuente",
    "error_fuente",
    "periodo_integracion_min",
]


def stabilize_types(frame: pd.DataFrame) -> pd.DataFrame:
    for column in NUMERIC_COLUMNS:
        if column in frame:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").astype("float64")
    for column in ["ciudad", "fuente", "segmento_id", "tipo_via", "calidad_registro", "direction_fuente", "region_fuente", "passage_fuente"]:
        if column in frame:
            frame[column] = frame[column].astype("string")
    return frame


def process_sao_paulo() -> dict:
    input_path = RAW_DIR / "sao_paulo" / "sao_paulo_traffic_jams_kaggle.zip"
    output_path = OUTPUT_DIR / "sao_paulo_cet.parquet"
    with zipfile.ZipFile(input_path) as archive:
        feather_name = next(name for name in archive.namelist() if name.endswith(".feather"))
        source = pd.read_feather(io.BytesIO(archive.read(feather_name)))

    processed = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(source["timestamp"], errors="coerce"),
            "ciudad": "Sao Paulo",
            "fuente": "sao_paulo_cet",
            "es_real": True,
            "segmento_id": source["segment"].astype("string"),
            "tipo_via": source["type"].astype("string"),
            "latitud": pd.NA,
            "longitud": pd.NA,
            "velocidad_kmh": pd.NA,
            "flujo_veh_h": pd.NA,
            "ocupacion_pct": pd.NA,
            "densidad_veh_km": pd.NA,
            "tiempo_viaje_seg": pd.NA,
            "congestion_longitud_m": pd.to_numeric(source["jam_size"], errors="coerce"),
            "calidad_registro": "advertencia",
            "direction_fuente": source["direction"].astype("string"),
            "region_fuente": source["region"].astype("string"),
            "passage_fuente": source["passage"].astype("string"),
        }
    )
    processed = stabilize_types(processed)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    processed.to_parquet(output_path, index=False, compression="zstd")
    return profile("sao_paulo_cet", input_path, output_path, processed, ["congestion_longitud_m"])


def process_istanbul() -> dict:
    input_path = RAW_DIR / "source_downloads" / "istanbul_traffic_index.csv"
    output_path = OUTPUT_DIR / "istanbul_traffic_index.parquet"
    source = pd.read_csv(input_path)
    timestamp = pd.to_datetime(source["trafficindexdate"], errors="coerce")
    processed = pd.DataFrame(
        {
            "timestamp": timestamp,
            "ciudad": "Istanbul",
            "fuente": "istanbul_traffic_index",
            "es_real": True,
            "segmento_id": "istanbul_aggregate_index",
            "tipo_via": "agregado",
            "latitud": pd.NA,
            "longitud": pd.NA,
            "velocidad_kmh": pd.NA,
            "flujo_veh_h": pd.NA,
            "ocupacion_pct": pd.NA,
            "densidad_veh_km": pd.NA,
            "tiempo_viaje_seg": pd.NA,
            "indice_congestion": pd.to_numeric(source["average_traffic_index"], errors="coerce"),
            "minimum_traffic_index": pd.to_numeric(source["minimum_traffic_index"], errors="coerce"),
            "maximum_traffic_index": pd.to_numeric(source["maximum_traffic_index"], errors="coerce"),
            "average_traffic_index": pd.to_numeric(source["average_traffic_index"], errors="coerce"),
            "calidad_registro": "advertencia",
        }
    )
    processed = stabilize_types(processed)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    processed.to_parquet(output_path, index=False, compression="zstd")
    return profile("istanbul_traffic_index", input_path, output_path, processed, ["indice_congestion"])


def process_madrid() -> dict:
    input_path = RAW_DIR / "madrid" / "historico_2022_12.zip"
    output_path = OUTPUT_DIR / "madrid_traffic_points.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = None
    total_rows = 0
    invalid_timestamps = 0
    null_cells = 0
    columns = []
    with zipfile.ZipFile(input_path) as archive:
        csv_name = next(name for name in archive.namelist() if name.endswith(".csv"))
        with archive.open(csv_name) as handle:
            for source in pd.read_csv(handle, sep=";", encoding="latin1", chunksize=250_000):
                timestamps = pd.to_datetime(source["fecha"], errors="coerce")
                processed = pd.DataFrame(
                    {
                        "timestamp": timestamps,
                        "ciudad": "Madrid",
                        "fuente": "madrid_traffic_points",
                        "es_real": True,
                        "segmento_id": source["id"].astype("string"),
                        "tipo_via": source["tipo_elem"].astype("string"),
                        "latitud": pd.NA,
                        "longitud": pd.NA,
                        "velocidad_kmh": pd.NA,
                        "flujo_veh_h": pd.to_numeric(source["intensidad"], errors="coerce"),
                        "ocupacion_pct": pd.to_numeric(source["ocupacion"], errors="coerce"),
                        "densidad_veh_km": pd.NA,
                        "tiempo_viaje_seg": pd.NA,
                        "calidad_registro": "advertencia",
                        "intensidad_fuente": pd.to_numeric(source["intensidad"], errors="coerce"),
                        "carga_fuente": pd.to_numeric(source["carga"], errors="coerce"),
                        "vmed_fuente": pd.to_numeric(source["vmed"], errors="coerce"),
                        "error_fuente": pd.to_numeric(source["error"], errors="coerce"),
                        "periodo_integracion_min": pd.to_numeric(source["periodo_integracion"], errors="coerce"),
                    }
                )
                processed = stabilize_types(processed)
                table = pa.Table.from_pandas(processed, preserve_index=False)
                if writer is None:
                    writer = pq.ParquetWriter(output_path, table.schema, compression="zstd")
                writer.write_table(table)
                total_rows += len(processed)
                invalid_timestamps += int(timestamps.isna().sum())
                null_cells += int(processed.isna().sum().sum())
                columns = list(processed.columns)
    if writer is not None:
        writer.close()
    report = {
        "source_id": "madrid_traffic_points",
        "input_path": str(input_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "output_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "rows": total_rows,
        "columns": columns,
        "null_cells": null_cells,
        "invalid_timestamps": invalid_timestamps,
        "quality": "advertencia",
        "notes": ["vmed_fuente se conserva sin convertir hasta confirmar unidad", "intensidad_fuente se conserva junto a flujo_veh_h como mapeo provisional"],
    }
    return report


def profile(source_id: str, input_path: Path, output_path: Path, frame: pd.DataFrame, observed_columns: list[str]) -> dict:
    return {
        "source_id": source_id,
        "input_path": str(input_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "output_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "null_cells": int(frame.isna().sum().sum()),
        "invalid_timestamps": int(frame["timestamp"].isna().sum()),
        "observed_columns": observed_columns,
        "quality": "advertencia",
    }


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    reports = [process_istanbul(), process_sao_paulo(), process_madrid()]
    report = {
        "pipeline": "international_sources_raw_to_processed",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": reports,
    }
    output = REPORT_DIR / "international_sources_quality.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"sources": len(reports), "rows": {item["source_id"]: item["rows"] for item in reports}, "report": str(output.relative_to(PROJECT_ROOT))}, ensure_ascii=False))


if __name__ == "__main__":
    main()