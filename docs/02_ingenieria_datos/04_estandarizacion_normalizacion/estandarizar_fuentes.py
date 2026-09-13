from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
INPUT_DIR = PROJECT_ROOT / "data" / "01_processed" / "pipeline"
OUTPUT_DIR = PROJECT_ROOT / "data" / "01_processed" / "normalized"

COMMON_COLUMNS = [
    "timestamp",
    "ciudad",
    "fuente",
    "es_real",
    "segmento_id",
    "tipo_via",
    "latitud",
    "longitud",
    "velocidad_kmh",
    "flujo_veh_h",
    "ocupacion_pct",
    "densidad_veh_km",
    "tiempo_viaje_seg",
    "calidad_registro",
]
OUTPUT_COLUMNS = COMMON_COLUMNS + ["valor_fuente"]

SOURCE_CONFIG = {
    "traffic_data": {"city": "Guadalajara", "is_real": True, "road_type": None},
    "scraped_traffic": {"city": "Guadalajara", "is_real": True, "road_type": None},
    "crowdsourcing_raw": {"city": "Guadalajara", "is_real": True, "road_type": None},
    "crowdsourcing_aggregated": {"city": "Guadalajara", "is_real": True, "road_type": None},
    "synthetic_traffic": {"city": "Guadalajara", "is_real": False, "road_type": None},
    "metr_la": {"city": "Los Angeles County", "is_real": True, "road_type": "autopista"},
    "pems_bay": {"city": "San Francisco Bay Area", "is_real": True, "road_type": "autopista"},
    "metr_la_sensor_locations": {"city": "Los Angeles County", "is_real": True, "road_type": "autopista"},
    "pems_bay_sensor_locations": {"city": "San Francisco Bay Area", "is_real": True, "road_type": "autopista"},
}


def empty_frame(size: int) -> pd.DataFrame:
    return pd.DataFrame({column: [pd.NA] * size for column in OUTPUT_COLUMNS})


def base_frame(source_id: str, size: int) -> pd.DataFrame:
    config = SOURCE_CONFIG[source_id]
    frame = empty_frame(size)
    frame["ciudad"] = config["city"]
    frame["fuente"] = source_id
    frame["es_real"] = config["is_real"]
    frame["tipo_via"] = config["road_type"]
    return frame


def normalize_local(source_id: str, source: pd.DataFrame) -> pd.DataFrame:
    frame = base_frame(source_id, len(source))
    frame["timestamp"] = pd.to_datetime(source["timestamp"], errors="coerce")

    if source_id in {"traffic_data", "scraped_traffic"}:
        frame["segmento_id"] = source["avenida"].astype("string")
        frame["latitud"] = pd.to_numeric(source["latitud"], errors="coerce")
        frame["longitud"] = pd.to_numeric(source["longitud"], errors="coerce")
        # Las unidades de estas columnas no están confirmadas en la fuente.
        frame["calidad_registro"] = "advertencia"
    elif source_id in {"crowdsourcing_raw", "crowdsourcing_aggregated"}:
        frame["segmento_id"] = source["road"].astype("string")
        if "latitude" in source:
            frame["latitud"] = pd.to_numeric(source["latitude"], errors="coerce")
            frame["longitud"] = pd.to_numeric(source["longitude"], errors="coerce")
        if "avg_speed" in source:
            frame["velocidad_kmh"] = pd.to_numeric(source["avg_speed"], errors="coerce")
        else:
            frame["velocidad_kmh"] = pd.to_numeric(source["speed_kmh"], errors="coerce")
        frame["calidad_registro"] = "valido"
    else:
        frame["segmento_id"] = source["road"].astype("string")
        frame["velocidad_kmh"] = pd.to_numeric(source["velocity_kmh"], errors="coerce")
        frame["flujo_veh_h"] = pd.to_numeric(source["flow_veh_h"], errors="coerce")
        frame["densidad_veh_km"] = pd.to_numeric(source["density_veh_km"], errors="coerce")
        frame["tiempo_viaje_seg"] = pd.to_numeric(source["wait_time_sec"], errors="coerce")
        frame["calidad_registro"] = "valido"

    return frame


def normalize_external(source_id: str, source: pd.DataFrame) -> pd.DataFrame:
    timestamp_column = source.columns[0]
    timestamps = pd.to_datetime(source[timestamp_column], errors="coerce")
    sensor_columns = list(source.columns[1:])
    values = source[sensor_columns].apply(pd.to_numeric, errors="coerce")
    long = values.copy()
    long.insert(0, "timestamp", timestamps)
    long = long.melt(id_vars="timestamp", var_name="segmento_id", value_name="source_value")
    frame = base_frame(source_id, len(long))
    frame["timestamp"] = long["timestamp"].to_numpy()
    frame["segmento_id"] = long["segmento_id"].astype("string").to_numpy()
    frame["valor_fuente"] = long["source_value"].to_numpy()
    # La unidad de velocidad de estos datasets no se convierte sin evidencia adicional.
    frame["calidad_registro"] = "advertencia"
    return frame


def normalize_sensor_locations(source_id: str, source: pd.DataFrame) -> pd.DataFrame:
    frame = base_frame(source_id, len(source))
    frame["segmento_id"] = source["sensor_id"].astype("string")
    frame["latitud"] = pd.to_numeric(source["latitude"], errors="coerce")
    frame["longitud"] = pd.to_numeric(source["longitude"], errors="coerce")
    frame["calidad_registro"] = "valido"
    return frame


def normalize_source(source_id: str) -> pd.DataFrame:
    source = pd.read_parquet(INPUT_DIR / f"{source_id}.parquet")
    if source_id in {"metr_la", "pems_bay"}:
        return normalize_external(source_id, source)
    if source_id in {"metr_la_sensor_locations", "pems_bay_sensor_locations"}:
        return normalize_sensor_locations(source_id, source)
    return normalize_local(source_id, source)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    reports = []
    for source_id in SOURCE_CONFIG:
        normalized = normalize_source(source_id)
        output_path = OUTPUT_DIR / f"{source_id}.parquet"
        normalized.to_parquet(output_path, index=False, compression="zstd")
        reports.append(
            {
                "source_id": source_id,
                "output_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                "rows": int(len(normalized)),
                "columns": list(normalized.columns),
                "null_cells": int(normalized.isna().sum().sum()),
                "invalid_timestamps": int(normalized["timestamp"].isna().sum()),
            }
        )

    manifest = {
        "pipeline": "standardize_and_normalize",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "common_columns": COMMON_COLUMNS,
        "sources": reports,
    }
    (OUTPUT_DIR / "normalization_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps({"sources": len(reports), "output": str(OUTPUT_DIR.relative_to(PROJECT_ROOT))}))


if __name__ == "__main__":
    main()
