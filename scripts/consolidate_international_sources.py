from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as parquet


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_DIR = PROJECT_ROOT / "data" / "02_clean" / "external"
OUTPUT_DIR = PROJECT_ROOT / "data" / "02_clean" / "consolidated"
BATCH_SIZE = 250_000

SOURCES = [
    ("istanbul_traffic_index", "indice_congestion", "indice_congestion"),
    ("sao_paulo_cet", "congestion_longitud_m", "congestion_longitud_m"),
    ("madrid_traffic_points", "intensidad", "intensidad_fuente"),
    ("metr_la", "velocidad_sensor", "valor_fuente"),
    ("pems_bay", "velocidad_sensor", "valor_fuente"),
]

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
    "metrica_principal",
    "valor_principal",
    "valor_fuente",
    "congestion_longitud_m",
    "indice_congestion",
    "intensidad_fuente",
    "carga_fuente",
    "vmed_fuente",
    "periodo_integracion_min",
]

NUMERIC_COLUMNS = [column for column in OUTPUT_COLUMNS if column not in {"timestamp", "ciudad", "fuente", "es_real", "segmento_id", "tipo_via", "calidad_registro", "metrica_principal"}]
OUTPUT_SCHEMA = pa.schema(
    [
        ("timestamp", pa.timestamp("ns")),
        ("ciudad", pa.string()),
        ("fuente", pa.string()),
        ("es_real", pa.bool_()),
        ("segmento_id", pa.string()),
        ("tipo_via", pa.string()),
        ("calidad_registro", pa.string()),
        ("metrica_principal", pa.string()),
        *[(column, pa.float64()) for column in NUMERIC_COLUMNS],
    ]
)


def normalize_batch(frame: pd.DataFrame, metric_name: str, metric_column: str) -> pa.Table:
    normalized = frame.reindex(columns=OUTPUT_COLUMNS).copy()
    normalized["metrica_principal"] = metric_name
    normalized["valor_principal"] = pd.to_numeric(frame.get(metric_column), errors="coerce")
    normalized["timestamp"] = pd.to_datetime(normalized["timestamp"], errors="coerce", utc=True).dt.tz_localize(None)
    for column in ["ciudad", "fuente", "segmento_id", "tipo_via", "calidad_registro", "metrica_principal"]:
        normalized[column] = normalized[column].astype("string")
    normalized["es_real"] = normalized["es_real"].astype("boolean")
    for column in NUMERIC_COLUMNS:
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce").astype("float64")
    return pa.Table.from_pandas(normalized, schema=OUTPUT_SCHEMA, preserve_index=False)


def consolidate() -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "international_observations.parquet"
    writer = parquet.ParquetWriter(output_path, OUTPUT_SCHEMA, compression="zstd")
    source_reports = []
    try:
        for source_id, metric_name, metric_column in SOURCES:
            input_path = CLEAN_DIR / f"{source_id}_clean.parquet"
            source_file = parquet.ParquetFile(input_path)
            rows = 0
            for batch in source_file.iter_batches(batch_size=BATCH_SIZE):
                table = normalize_batch(batch.to_pandas(), metric_name, metric_column)
                writer.write_table(table)
                rows += table.num_rows
            source_reports.append(
                {
                    "source_id": source_id,
                    "input_path": str(input_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                    "rows": rows,
                    "metrica_principal": metric_name,
                }
            )
    finally:
        writer.close()
    return {
        "output_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "rows": sum(item["rows"] for item in source_reports),
        "sources": source_reports,
    }


def main() -> None:
    consolidated = consolidate()
    manifest = {
        "pipeline": "international_clean_consolidation",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "sql_status": "pendiente_hasta_curso_sql",
        "timestamp_rule": "El consolidado almacena timestamp en UTC sin zona embebida; la zona horaria original permanece en el contrato de cada fuente.",
        "metric_separation_rule": "No comparar directamente velocidad, indice de congestion, longitud de congestion e intensidad sin una transformacion documentada.",
        "consolidated_output": consolidated,
    }
    manifest_path = OUTPUT_DIR / "international_consolidation_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"rows": consolidated["rows"], "sources": len(consolidated["sources"]), "manifest": str(manifest_path.relative_to(PROJECT_ROOT))}, ensure_ascii=False))


if __name__ == "__main__":
    main()