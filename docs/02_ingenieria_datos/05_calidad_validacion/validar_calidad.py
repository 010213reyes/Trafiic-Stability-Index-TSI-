from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow.parquet as parquet


PROJECT_ROOT = Path(__file__).resolve().parents[3]
INPUT_DIR = PROJECT_ROOT / "data" / "01_processed" / "normalized"
OUTPUT_DIR = PROJECT_ROOT / "data" / "01_processed" / "quality"
BATCH_SIZE = 100_000
MAX_REJECTED_ROWS = 5_000

COMMON_COLUMNS = {
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
}
REQUIRED_COLUMNS = {
    "timestamp",
    "ciudad",
    "fuente",
    "es_real",
    "segmento_id",
    "tipo_via",
}
METADATA_SOURCES = {"metr_la_sensor_locations", "pems_bay_sensor_locations"}

NUMERIC_RANGES = {
    "latitud": (-90, 90),
    "longitud": (-180, 180),
    "velocidad_kmh": (0, 200),
    "flujo_veh_h": (0, None),
    "ocupacion_pct": (0, 100),
    "densidad_veh_km": (0, None),
    "tiempo_viaje_seg": (0, None),
    "valor_fuente": (0, None),
}


def add_rejections(
    rejected: list[dict[str, object]],
    source_id: str,
    row_numbers: pd.Series,
    reasons: pd.Series,
) -> None:
    mask = reasons.ne("")
    for row_number, reason in zip(row_numbers[mask].tolist(), reasons[mask].tolist()):
        if len(rejected) >= MAX_REJECTED_ROWS:
            return
        rejected.append(
            {
                "source_id": source_id,
                "row_number": int(row_number),
                "reason": reason,
            }
        )


def validate_file(path: Path, rejected: list[dict[str, object]]) -> dict[str, object]:
    source_id = path.stem
    parquet_file = parquet.ParquetFile(path)
    columns = set(parquet_file.schema_arrow.names)
    missing_columns = sorted(COMMON_COLUMNS - columns)
    is_metadata = source_id in METADATA_SOURCES
    required_columns = REQUIRED_COLUMNS - {"timestamp"} if is_metadata else REQUIRED_COLUMNS
    missing_required = sorted(required_columns - columns)

    report: dict[str, object] = {
        "source_id": source_id,
        "path": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "rows": parquet_file.metadata.num_rows,
        "columns": parquet_file.schema_arrow.names,
        "missing_common_columns": missing_columns,
        "missing_required_columns": missing_required,
        "null_counts": {},
        "invalid_timestamps": 0,
        "duplicate_rows": 0,
        "range_violations": {},
        "rejected_rows": 0,
        "status": "valido",
    }

    null_counts = {column: 0 for column in columns}
    range_violations = {column: 0 for column in NUMERIC_RANGES if column in columns}
    invalid_timestamps = 0
    duplicate_rows = 0
    row_offset = 0
    missing_required_values = 0

    for batch in parquet_file.iter_batches(batch_size=BATCH_SIZE):
        frame = batch.to_pandas()
        row_numbers = pd.Series(range(row_offset + 1, row_offset + len(frame) + 1))
        row_offset += len(frame)

        for column in columns:
            null_counts[column] += int(frame[column].isna().sum())

        invalid = pd.Series(False, index=frame.index)
        reasons = pd.Series("", index=frame.index, dtype="string")

        if "timestamp" in frame and not is_metadata:
            parsed = pd.to_datetime(frame["timestamp"], errors="coerce")
            bad_timestamp = parsed.isna()
            invalid_timestamps += int(bad_timestamp.sum())
            invalid |= bad_timestamp
            reasons.loc[bad_timestamp] = "timestamp_invalido"

        for column in required_columns:
            if column not in frame:
                continue
            missing = frame[column].isna()
            missing_required_values += int(missing.sum())
            invalid |= missing
            reasons.loc[missing & reasons.eq("")] = f"nulo_obligatorio:{column}"

        duplicate = frame.duplicated(keep=False)
        duplicate_rows += int(duplicate.sum())
        invalid |= duplicate
        reasons.loc[duplicate & reasons.eq("")] = "fila_duplicada"

        for column, (minimum, maximum) in NUMERIC_RANGES.items():
            if column not in frame:
                continue
            values = pd.to_numeric(frame[column], errors="coerce")
            bad_range = values.notna() & ((minimum is not None) & (values < minimum))
            if maximum is not None:
                bad_range |= values.notna() & (values > maximum)
            range_violations[column] += int(bad_range.sum())
            invalid |= bad_range
            reasons.loc[bad_range & reasons.eq("")] = f"rango_invalido:{column}"

        add_rejections(rejected, source_id, row_numbers, reasons)

    report["null_counts"] = null_counts
    report["invalid_timestamps"] = invalid_timestamps
    report["duplicate_rows"] = duplicate_rows
    report["missing_required_values"] = missing_required_values
    report["range_violations"] = range_violations
    report["rejected_rows_sampled"] = sum(1 for item in rejected if item["source_id"] == source_id)

    if missing_required or missing_required_values or invalid_timestamps or duplicate_rows or any(range_violations.values()):
        report["status"] = "advertencia"
    return report


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rejected: list[dict[str, object]] = []
    reports = [
        validate_file(path, rejected)
        for path in sorted(INPUT_DIR.glob("*.parquet"))
    ]
    quality_report = {
        "pipeline": "quality_validation",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_directory": str(INPUT_DIR.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "batch_size": BATCH_SIZE,
        "max_rejected_rows_sample": MAX_REJECTED_ROWS,
        "sources": reports,
    }
    (OUTPUT_DIR / "quality_report.json").write_text(
        json.dumps(quality_report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    pd.DataFrame(rejected).to_csv(OUTPUT_DIR / "rejected_rows.csv", index=False)
    print(json.dumps({"sources": len(reports), "rejected_sample": len(rejected)}))


if __name__ == "__main__":
    main()
