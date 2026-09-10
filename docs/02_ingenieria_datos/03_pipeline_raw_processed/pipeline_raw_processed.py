from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "00_raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "01_processed" / "pipeline"

SOURCE_FILES = {
    "traffic_data": RAW_DIR / "traffic_data.csv",
    "scraped_traffic": RAW_DIR / "scraped_traffic.csv",
    "crowdsourcing_raw": RAW_DIR / "crowdsourcing_raw.csv",
    "crowdsourcing_aggregated": RAW_DIR / "crowdsourcing_aggregated.csv",
    "synthetic_traffic": RAW_DIR / "synthetic_traffic.csv",
    "metr_la": RAW_DIR / "external" / "traffic_datasets" / "METR-LA.csv",
    "pems_bay": RAW_DIR / "external" / "traffic_datasets" / "PEMS-BAY.csv",
    "metr_la_sensor_locations": RAW_DIR / "external" / "sensor_metadata" / "metr_la_sensor_locations.csv",
    "pems_bay_sensor_locations": RAW_DIR / "external" / "sensor_metadata" / "pems_bay_sensor_locations.csv",
}


def read_source(source_id: str, path: Path) -> pd.DataFrame:
    if source_id == "pems_bay_sensor_locations":
        return pd.read_csv(path, header=None, names=["sensor_id", "latitude", "longitude"])
    return pd.read_csv(path, low_memory=False)


def process_source(source_id: str, path: Path) -> dict[str, object]:
    dataframe = read_source(source_id, path)
    output_path = PROCESSED_DIR / f"{source_id}.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_parquet(output_path, index=False, compression="zstd")

    timestamp_column = next(
        (
            column
            for column in dataframe.columns
            if str(column).lower() in {"timestamp", "time", "datetime"}
        ),
        None,
    )
    if timestamp_column is None and source_id in {"metr_la", "pems_bay"}:
        timestamp_column = dataframe.columns[0]
    timestamp_series = (
        pd.to_datetime(dataframe[timestamp_column], errors="coerce")
        if timestamp_column
        else pd.Series(dtype="datetime64[ns]")
    )

    return {
        "source_id": source_id,
        "source_path": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "processed_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "rows": int(len(dataframe)),
        "columns": int(len(dataframe.columns)),
        "timestamp_column": timestamp_column or "",
        "invalid_timestamps": int(timestamp_series.isna().sum()) if timestamp_column else "",
        "min_timestamp": timestamp_series.min().isoformat() if timestamp_column and timestamp_series.notna().any() else "",
        "max_timestamp": timestamp_series.max().isoformat() if timestamp_column and timestamp_series.notna().any() else "",
    }


def main() -> None:
    manifest = {
        "pipeline": "raw_to_processed",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": ".",
        "sources": [process_source(source_id, path) for source_id, path in SOURCE_FILES.items()],
    }
    manifest_path = PROCESSED_DIR / "pipeline_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"sources": len(manifest["sources"]), "manifest": str(manifest_path.relative_to(PROJECT_ROOT))}))


if __name__ == "__main__":
    main()
