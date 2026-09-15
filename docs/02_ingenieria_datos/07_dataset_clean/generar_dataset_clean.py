from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONSOLIDATED_DIR = PROJECT_ROOT / "data" / "02_clean" / "consolidated"
OUTPUT_DIR = PROJECT_ROOT / "data" / "02_clean" / "dataset_clean"

REQUIRED_COLUMNS = [
    "timestamp",
    "ciudad",
    "fuente",
    "es_real",
    "segmento_id",
    "tipo_via",
]


def freeze_dataset(frame: pd.DataFrame, dataset_name: str) -> tuple[Path, dict[str, object]]:
    clean = frame.copy()
    clean = clean.drop_duplicates().copy()
    clean = clean.dropna(subset=REQUIRED_COLUMNS, how="any").copy()
    clean["timestamp"] = pd.to_datetime(clean["timestamp"], errors="coerce")
    clean = clean.dropna(subset=["timestamp"]).copy()
    clean = clean.sort_values("timestamp").reset_index(drop=True)

    output_path = OUTPUT_DIR / f"{dataset_name}.parquet"
    clean.to_parquet(output_path, index=False, compression="zstd")

    manifest = {
        "dataset_name": dataset_name,
        "rows": int(len(clean)),
        "columns": list(clean.columns),
        "output_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "required_columns": REQUIRED_COLUMNS,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    return output_path, manifest


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    observations = pd.read_parquet(CONSOLIDATED_DIR / "consolidated_observations.parquet")
    aggregates = pd.read_parquet(CONSOLIDATED_DIR / "derived_aggregates.parquet")
    sensor_catalog = pd.read_parquet(CONSOLIDATED_DIR / "sensor_catalog.parquet")

    obs_path, obs_manifest = freeze_dataset(observations, "clean_observations")
    agg_path, agg_manifest = freeze_dataset(aggregates, "clean_aggregates")
    cat_path, cat_manifest = freeze_dataset(sensor_catalog, "clean_sensor_catalog")

    manifest = {
        "pipeline": "dataset_clean",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_sources": {
            "observations": str((CONSOLIDATED_DIR / "consolidated_observations.parquet").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "aggregates": str((CONSOLIDATED_DIR / "derived_aggregates.parquet").relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "sensor_catalog": str((CONSOLIDATED_DIR / "sensor_catalog.parquet").relative_to(PROJECT_ROOT)).replace("\\", "/"),
        },
        "outputs": {
            "observations": obs_manifest,
            "aggregates": agg_manifest,
            "sensor_catalog": cat_manifest,
        },
        "notes": [
            "Se congelan solo registros con la firma mínima requerida para análisis y modelado.",
            "Los agregados y catálogos espaciales se conservan como artefactos complementarios.",
            "Los registros con nulls obligatorios o timestamps inválidos quedan fuera del dataset limpio.",
        ],
    }

    (OUTPUT_DIR / "dataset_clean_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "clean_observations_rows": obs_manifest["rows"],
                "clean_aggregates_rows": agg_manifest["rows"],
                "clean_sensor_catalog_rows": cat_manifest["rows"],
                "output_dir": str(OUTPUT_DIR.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
