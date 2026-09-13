from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as parquet


PROJECT_ROOT = Path(__file__).resolve().parents[3]
INPUT_DIR = PROJECT_ROOT / "data" / "01_processed" / "normalized"
QUALITY_REPORT = PROJECT_ROOT / "data" / "01_processed" / "quality" / "quality_report.json"
OUTPUT_DIR = PROJECT_ROOT / "data" / "02_clean" / "consolidated"
BATCH_SIZE = 100_000

OBSERVATION_SOURCES = [
    "traffic_data",
    "scraped_traffic",
    "crowdsourcing_raw",
    "synthetic_traffic",
    "metr_la",
    "pems_bay",
]
AGGREGATE_SOURCES = ["crowdsourcing_aggregated"]
CATALOG_SOURCES = ["metr_la_sensor_locations", "pems_bay_sensor_locations"]
OUTPUT_COLUMNS = [
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
    "valor_fuente",
]
OUTPUT_SCHEMA = pa.schema(
    [
        ("timestamp", pa.timestamp("ns")),
        ("ciudad", pa.string()),
        ("fuente", pa.string()),
        ("es_real", pa.bool_()),
        ("segmento_id", pa.string()),
        ("tipo_via", pa.string()),
        ("latitud", pa.float64()),
        ("longitud", pa.float64()),
        ("velocidad_kmh", pa.float64()),
        ("flujo_veh_h", pa.float64()),
        ("ocupacion_pct", pa.float64()),
        ("densidad_veh_km", pa.float64()),
        ("tiempo_viaje_seg", pa.float64()),
        ("calidad_registro", pa.string()),
        ("valor_fuente", pa.float64()),
    ]
)


def normalize_batch(batch: pa.RecordBatch) -> pa.Table:
    frame = batch.to_pandas()
    frame = frame.reindex(columns=OUTPUT_COLUMNS)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
    for column in ["ciudad", "fuente", "segmento_id", "tipo_via", "calidad_registro"]:
        frame[column] = frame[column].astype("string")
    frame["es_real"] = frame["es_real"].astype("boolean")
    for column in [
        "latitud",
        "longitud",
        "velocidad_kmh",
        "flujo_veh_h",
        "ocupacion_pct",
        "densidad_veh_km",
        "tiempo_viaje_seg",
        "valor_fuente",
    ]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return pa.Table.from_pandas(frame, schema=OUTPUT_SCHEMA, preserve_index=False)


def consolidate_sources(source_ids: list[str], output_name: str) -> list[dict[str, object]]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / output_name
    source_reports = []
    writer = parquet.ParquetWriter(output_path, OUTPUT_SCHEMA, compression="zstd")
    try:
        for source_id in source_ids:
            input_path = INPUT_DIR / f"{source_id}.parquet"
            source_file = parquet.ParquetFile(input_path)
            rows = 0
            for batch in source_file.iter_batches(batch_size=BATCH_SIZE):
                table = normalize_batch(batch)
                writer.write_table(table)
                rows += table.num_rows
            source_reports.append(
                {
                    "source_id": source_id,
                    "input_path": str(input_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                    "rows": rows,
                }
            )
    finally:
        writer.close()
    return [{"output_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"), "sources": source_reports}]


def consolidate_catalogs() -> dict[str, object]:
    output_path = OUTPUT_DIR / "sensor_catalog.parquet"
    frames = []
    for source_id in CATALOG_SOURCES:
        frame = pd.read_parquet(INPUT_DIR / f"{source_id}.parquet")
        frames.append(frame)
    catalog = pd.concat(frames, ignore_index=True)
    catalog.to_parquet(output_path, index=False, compression="zstd")
    return {
        "output_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "sources": CATALOG_SOURCES,
        "rows": int(len(catalog)),
    }


def main() -> None:
    quality = json.loads(QUALITY_REPORT.read_text(encoding="utf-8"))
    quality_status = {item["source_id"]: item["status"] for item in quality["sources"]}
    observations = consolidate_sources(OBSERVATION_SOURCES, "consolidated_observations.parquet")
    aggregates = consolidate_sources(AGGREGATE_SOURCES, "derived_aggregates.parquet")
    catalog = consolidate_catalogs()
    manifest = {
        "pipeline": "integration_and_consolidation",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "observation_output": observations[0],
        "aggregate_output": aggregates[0],
        "catalog_output": catalog,
        "quality_status_by_source": quality_status,
        "excluded_from_observations": {
            "crowdsourcing_aggregated": "Se conserva separado para evitar duplicar crowdsourcing_raw.",
            "sensor_locations": "Se conserva como catálogo espacial.",
        },
    }
    (OUTPUT_DIR / "consolidation_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps({"observation_sources": len(OBSERVATION_SOURCES), "aggregate_sources": len(AGGREGATE_SOURCES), "catalog_sources": len(CATALOG_SOURCES)}))


if __name__ == "__main__":
    main()
