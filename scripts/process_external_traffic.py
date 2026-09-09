#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Procesa las series externas de METR-LA y PEMS-BAY sin modificar los raw."""

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "00_raw" / "external" / "traffic_datasets"
PROCESSED_DIR = PROJECT_ROOT / "data" / "01_processed" / "external"


DATASETS = {
    "METR-LA": {
        "input": RAW_DIR / "METR-LA.csv",
        "output": PROCESSED_DIR / "metr_la.parquet",
        "city": "Los Angeles County",
        "road_type": "autopista",
    },
    "PEMS-BAY": {
        "input": RAW_DIR / "PEMS-BAY.csv",
        "output": PROCESSED_DIR / "pems_bay.parquet",
        "city": "San Francisco Bay Area",
        "road_type": "autopista",
    },
}


def standardize_dataset(name, config):
    dataframe = pd.read_csv(config["input"])
    original_timestamp = dataframe.columns[0]
    dataframe = dataframe.rename(columns={original_timestamp: "timestamp"})
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"], errors="coerce")

    sensor_columns = [column for column in dataframe.columns if column != "timestamp"]
    dataframe = dataframe.rename(
        columns={column: f"sensor_{column}" for column in sensor_columns}
    )
    sensor_columns = [column for column in dataframe.columns if column != "timestamp"]

    timestamp_delta = dataframe["timestamp"].sort_values().diff().dropna()
    interval_minutes = None
    if not timestamp_delta.empty:
        interval_minutes = float(
            timestamp_delta.dt.total_seconds().div(60).mode().iloc[0]
        )

    report = {
        "dataset": name,
        "city": config["city"],
        "tipo_via": config["road_type"],
        "source_file": str(config["input"].relative_to(PROJECT_ROOT)),
        "output_file": str(config["output"].relative_to(PROJECT_ROOT)),
        "rows": int(len(dataframe)),
        "sensor_count": int(len(sensor_columns)),
        "sensor_columns": sensor_columns,
        "start": dataframe["timestamp"].min().isoformat(),
        "end": dataframe["timestamp"].max().isoformat(),
        "dominant_interval_minutes": interval_minutes,
        "invalid_timestamps": int(dataframe["timestamp"].isna().sum()),
        "duplicate_timestamps": int(dataframe["timestamp"].duplicated().sum()),
        "missing_values": int(dataframe.isna().sum().sum()),
        "negative_values": int((dataframe[sensor_columns] < 0).sum().sum()),
    }

    config["output"].parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_parquet(config["output"], index=False, compression="zstd")
    return report


def main():
    reports = [standardize_dataset(name, config) for name, config in DATASETS.items()]
    report_path = PROCESSED_DIR / "external_traffic_quality.json"
    report_path.write_text(
        json.dumps(reports, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(reports, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()