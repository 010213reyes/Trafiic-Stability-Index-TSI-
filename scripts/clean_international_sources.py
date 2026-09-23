from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "data" / "01_processed" / "external"
NORMALIZED_DIR = PROJECT_ROOT / "data" / "01_processed" / "normalized"
OUTPUT_DIR = PROJECT_ROOT / "data" / "02_clean" / "external"
REPORT_DIR = PROJECT_ROOT / "data" / "02_clean" / "external"
BATCH_SIZE = 250_000

SOURCE_RULES = {
    "istanbul_traffic_index": {
        "numeric_nonnegative": ["indice_congestion", "minimum_traffic_index", "maximum_traffic_index", "average_traffic_index"],
    },
    "sao_paulo_cet": {
        "numeric_nonnegative": ["congestion_longitud_m"],
    },
    "madrid_traffic_points": {
        "numeric_nonnegative": ["flujo_veh_h", "carga_fuente", "vmed_fuente", "error_fuente", "periodo_integracion_min"],
        "bounded": {"ocupacion_pct": (0, 100)},
    },
    "metr_la": {"numeric_nonnegative": ["valor_fuente"]},
    "pems_bay": {"numeric_nonnegative": ["valor_fuente"]},
}


def clean_batch(source_id: str, frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    rules = SOURCE_RULES[source_id]
    parsed_timestamp = pd.to_datetime(frame["timestamp"], errors="coerce")
    invalid_timestamp = parsed_timestamp.isna()
    frame = frame.loc[~invalid_timestamp].copy()
    frame["timestamp"] = parsed_timestamp.loc[frame.index]

    negative_mask = pd.Series(False, index=frame.index)
    for column in rules.get("numeric_nonnegative", []):
        if column in frame:
            values = pd.to_numeric(frame[column], errors="coerce")
            negative_mask |= values.notna() & values.lt(0)
    for column, (minimum, maximum) in rules.get("bounded", {}).items():
        if column in frame:
            values = pd.to_numeric(frame[column], errors="coerce")
            negative_mask |= values.notna() & ((values < minimum) | (values > maximum))
    frame = frame.loc[~negative_mask].copy()
    duplicate_mask = frame.duplicated(keep="first")
    frame = frame.loc[~duplicate_mask].copy()
    frame["calidad_registro"] = frame["calidad_registro"].fillna("advertencia")
    return frame, {
        "invalid_timestamps": int(invalid_timestamp.sum()),
        "range_violations": int(negative_mask.sum()),
        "duplicate_rows": int(duplicate_mask.sum()),
    }


def clean_source(source_id: str) -> dict[str, object]:
    input_dir = NORMALIZED_DIR if source_id in {"metr_la", "pems_bay"} else INPUT_DIR
    input_path = input_dir / f"{source_id}.parquet"
    output_path = OUTPUT_DIR / f"{source_id}_clean.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    parquet_file = pq.ParquetFile(input_path)
    writer = None
    input_rows = 0
    output_rows = 0
    counters = {"invalid_timestamps": 0, "range_violations": 0, "duplicate_rows": 0}
    for batch in parquet_file.iter_batches(batch_size=BATCH_SIZE):
        frame = batch.to_pandas()
        input_rows += len(frame)
        cleaned, batch_counts = clean_batch(source_id, frame)
        for key, value in batch_counts.items():
            counters[key] += value
        if cleaned.empty:
            continue
        table = pa.Table.from_pandas(cleaned, preserve_index=False)
        if writer is None:
            writer = pq.ParquetWriter(output_path, table.schema, compression="zstd")
        writer.write_table(table)
        output_rows += len(cleaned)
    if writer is not None:
        writer.close()
    return {
        "source_id": source_id,
        "input_path": str(input_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "output_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "input_rows": input_rows,
        "output_rows": output_rows,
        **counters,
        "status": "valido" if not any(counters.values()) else "advertencia",
    }


def main() -> None:
    reports = [clean_source(source_id) for source_id in SOURCE_RULES]
    report = {
        "pipeline": "international_sources_processed_to_clean",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "batch_size": BATCH_SIZE,
        "sources": reports,
    }
    report_path = REPORT_DIR / "international_clean_quality.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"sources": len(reports), "rows": {item["source_id"]: item["output_rows"] for item in reports}, "report": str(report_path.relative_to(PROJECT_ROOT))}, ensure_ascii=False))


if __name__ == "__main__":
    main()