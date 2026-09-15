from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
INPUT_DIR = PROJECT_ROOT / "data" / "02_clean" / "dataset_clean"
OUTPUT_DIR = INPUT_DIR

COLUMN_SQL_TYPES = {
    "timestamp": "TIMESTAMP",
    "ciudad": "VARCHAR(100)",
    "fuente": "VARCHAR(50)",
    "es_real": "BOOLEAN",
    "segmento_id": "VARCHAR(100)",
    "tipo_via": "VARCHAR(100)",
    "latitud": "DOUBLE",
    "longitud": "DOUBLE",
    "velocidad_kmh": "DOUBLE",
    "flujo_veh_h": "DOUBLE",
    "ocupacion_pct": "DOUBLE",
    "densidad_veh_km": "DOUBLE",
    "tiempo_viaje_seg": "DOUBLE",
    "calidad_registro": "VARCHAR(30)",
    "valor_fuente": "DOUBLE",
}


def build_entity(entity_name: str, input_path: Path, primary_key: str | None = None) -> dict[str, object]:
    frame = pd.read_parquet(input_path)
    columns = list(frame.columns)
    schema = [
        {
            "column": column,
            "sql_type": COLUMN_SQL_TYPES.get(column, "TEXT"),
            "nullable": bool(frame[column].isna().any()),
            "nulls": int(frame[column].isna().sum()),
        }
        for column in columns
    ]
    return {
        "entity_name": entity_name,
        "source_path": str(input_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "rows": int(len(frame)),
        "primary_key": primary_key,
        "columns": schema,
        "target_stage": "sql_load",
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    observations = INPUT_DIR / "clean_observations.parquet"
    sensor_catalog = INPUT_DIR / "clean_sensor_catalog.parquet"
    aggregates = INPUT_DIR / "clean_aggregates.parquet"

    entities = [
        build_entity("fact_observaciones", observations, primary_key="observation_id"),
        build_entity("dim_segmento", observations, primary_key="segmento_id"),
        build_entity("dim_fuente", observations, primary_key="fuente"),
        build_entity("dim_catalogo_sensores", sensor_catalog, primary_key="segmento_id"),
        build_entity("fact_aggregates", aggregates, primary_key="segmento_id"),
    ]

    manifest = {
        "pipeline": "sql_preparation",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_dataset": str(observations.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "entities": entities,
        "notes": [
            "fact_observaciones es la entidad principal para consultas temporales y segmentales.",
            "dim_segmento y dim_fuente deben cargarse como dimensiones referenciales.",
            "dim_catalogo_sensores se deja preparado para el catálogo espacial, aunque el dataset actual está vacío.",
            "fact_aggregates queda disponible como conjunto derivado para análisis y reportes agregados.",
        ],
    }

    output_path = OUTPUT_DIR / "sql_preparation_manifest.json"
    output_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        json.dumps(
            {
                "entities": len(entities),
                "source_rows": int(pd.read_parquet(observations).shape[0]),
                "output_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
