from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "00_raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "01_processed"

SOURCE_DEFINITIONS = [
    {
        "source_id": "traffic_data",
        "path": "data/00_raw/traffic_data.csv",
        "source_type": "historical",
        "city": "Guadalajara",
        "is_real": True,
        "origin": "Scraping_Traffic.ipynb",
        "processed_output": "data/01_processed/traffic_data_normalized.parquet",
        "clean_output": "data/02_clean/traffic_data.csv",
    },
    {
        "source_id": "scraped_traffic",
        "path": "data/00_raw/scraped_traffic.csv",
        "source_type": "scraping",
        "city": "Guadalajara",
        "is_real": True,
        "origin": "Scraping_Traffic.ipynb",
        "processed_output": "data/01_processed/scraped_traffic_normalized.parquet",
        "clean_output": "data/02_clean/traffic_data.csv",
    },
    {
        "source_id": "crowdsourcing_raw",
        "path": "data/00_raw/crowdsourcing_raw.csv",
        "source_type": "crowdsourcing",
        "city": "Guadalajara",
        "is_real": True,
        "origin": "03_Crowdsourcing_Collection.ipynb",
        "processed_output": "data/01_processed/crowdsourcing_normalized.parquet",
        "clean_output": "data/02_clean/historical_consolidated.csv",
    },
    {
        "source_id": "crowdsourcing_aggregated",
        "path": "data/00_raw/crowdsourcing_aggregated.csv",
        "source_type": "derived",
        "city": "Guadalajara",
        "is_real": True,
        "origin": "03_Crowdsourcing_Collection.ipynb; crowdsourcing_raw.csv",
        "processed_output": "data/01_processed/crowdsourcing_aggregated_normalized.parquet",
        "clean_output": "data/02_clean/historical_consolidated.csv",
    },
    {
        "source_id": "synthetic_traffic",
        "path": "data/00_raw/synthetic_traffic.csv",
        "source_type": "synthetic",
        "city": "Guadalajara",
        "is_real": False,
        "origin": "01_Synthetic_Traffic_Data.ipynb",
        "processed_output": "data/01_processed/synthetic_traffic_normalized.parquet",
        "clean_output": "data/02_clean/traffic_enriched.csv",
    },
    {
        "source_id": "metr_la",
        "path": "data/00_raw/external/traffic_datasets/METR-LA.csv",
        "source_type": "external_real",
        "city": "Los Angeles County",
        "is_real": True,
        "origin": "Zenodo 5724362; DCRNN sensor graph",
        "processed_output": "data/01_processed/external/metr_la.parquet",
        "clean_output": "data/02_clean/external/metr_la_clean.parquet",
    },
    {
        "source_id": "pems_bay",
        "path": "data/00_raw/external/traffic_datasets/PEMS-BAY.csv",
        "source_type": "external_real",
        "city": "San Francisco Bay Area",
        "is_real": True,
        "origin": "Zenodo 5724362; DCRNN sensor graph",
        "processed_output": "data/01_processed/external/pems_bay.parquet",
        "clean_output": "data/02_clean/external/pems_bay_clean.parquet",
    },
    {
        "source_id": "metr_la_sensor_locations",
        "path": "data/00_raw/external/sensor_metadata/metr_la_sensor_locations.csv",
        "source_type": "sensor_metadata",
        "city": "Los Angeles County",
        "is_real": True,
        "origin": "DCRNN sensor graph",
        "processed_output": "data/01_processed/external/metr_la_sensor_locations.csv",
        "clean_output": "data/02_clean/external/metr_la_sensor_locations.csv",
    },
    {
        "source_id": "pems_bay_sensor_locations",
        "path": "data/00_raw/external/sensor_metadata/pems_bay_sensor_locations.csv",
        "source_type": "sensor_metadata",
        "city": "San Francisco Bay Area",
        "is_real": True,
        "origin": "DCRNN sensor graph",
        "processed_output": "data/01_processed/external/pems_bay_sensor_locations.csv",
        "clean_output": "data/02_clean/external/pems_bay_sensor_locations.csv",
    },
]


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def inspect_source(definition: dict[str, object]) -> dict[str, object]:
    relative_path = str(definition["path"])
    path = PROJECT_ROOT / relative_path
    frame = (
        pd.read_csv(path, header=None, names=["sensor_id", "latitude", "longitude"])
        if definition["source_id"] == "pems_bay_sensor_locations"
        else read_csv(path)
    )
    timestamp_column = next(
        (column for column in frame.columns if column.lower() in {"timestamp", "time", "datetime"}),
        None,
    )
    timestamps = pd.to_datetime(frame[timestamp_column], errors="coerce") if timestamp_column else pd.Series(dtype="datetime64[ns]")
    return {
        **definition,
        "format": path.suffix.lower().lstrip("."),
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "column_names": "|".join(str(column) for column in frame.columns),
        "null_cells": int(frame.isna().sum().sum()),
        "duplicate_rows": int(frame.duplicated().sum()),
        "timestamp_column": timestamp_column or "",
        "invalid_timestamps": int(timestamps.isna().sum()) if timestamp_column else "",
        "min_timestamp": timestamps.min().isoformat() if timestamp_column and timestamps.notna().any() else "",
        "max_timestamp": timestamps.max().isoformat() if timestamp_column and timestamps.notna().any() else "",
        "file_bytes": int(path.stat().st_size),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    inventory = [inspect_source(definition) for definition in SOURCE_DEFINITIONS]
    lineage = [
        {
            "source_id": row["source_id"],
            "source_path": row["path"],
            "origin": row["origin"],
            "processed_output": row["processed_output"],
            "clean_output": row["clean_output"],
            "pipeline_stage": "raw -> processed -> clean",
            "is_real": row["is_real"],
            "notes": "Fuente derivada" if row["source_type"] == "derived" else "",
        }
        for row in inventory
    ]
    write_csv(PROCESSED_DIR / "data_inventory.csv", inventory)
    write_csv(PROCESSED_DIR / "data_lineage.csv", lineage)
    print(json.dumps({"inventory_rows": len(inventory), "lineage_rows": len(lineage)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
