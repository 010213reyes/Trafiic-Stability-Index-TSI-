from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

PROJECT_ROOT = Path(__file__).resolve().parents[3]
OBSERVATIONS_PATH = PROJECT_ROOT / "data" / "02_clean" / "dataset_clean" / "clean_observations.parquet"
AGGREGATES_PATH = PROJECT_ROOT / "data" / "02_clean" / "dataset_clean" / "clean_aggregates.parquet"
SQL_DIR = PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql"
DB_PATH = SQL_DIR / "tsi_stage.sqlite"
MANIFEST_PATH = SQL_DIR / "sql_load_manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Carga el dataset limpio de TSI hacia SQLite")
    parser.add_argument("--max-rows", type=int, default=None, help="Límite opcional para pruebas de carga")
    parser.add_argument("--db-path", type=str, default=str(DB_PATH), help="Ruta de la base SQLite destino")
    return parser.parse_args()


def stream_parquet_to_sql(path: Path, table_name: str, conn: sqlite3.Connection, batch_size: int = 100_000, max_rows: int | None = None) -> int:
    parquet_file = pq.ParquetFile(path)
    total_rows = 0
    first_batch = True
    remaining = max_rows

    for batch in parquet_file.iter_batches(batch_size=batch_size):
        frame = batch.to_pandas()
        if max_rows is not None:
            if remaining is not None and remaining <= 0:
                break
            frame = frame.head(remaining)
            remaining = None if remaining is None else max(remaining - len(frame), 0)

        if frame.empty:
            break

        frame.to_sql(table_name, conn, if_exists="replace" if first_batch else "append", index=False, chunksize=50_000)
        total_rows += len(frame)
        first_batch = False

    return total_rows


def load_dimensions(conn: sqlite3.Connection, observations: pd.DataFrame) -> dict[str, int]:
    segment_dim = observations[["segmento_id", "ciudad", "tipo_via"]].drop_duplicates().reset_index(drop=True)
    source_dim = observations[["fuente", "ciudad", "es_real"]].drop_duplicates().reset_index(drop=True)

    segment_dim.to_sql("dim_segmento", conn, if_exists="replace", index=False)
    source_dim.to_sql("dim_fuente", conn, if_exists="replace", index=False)
    return {
        "dim_segmento": int(len(segment_dim)),
        "dim_fuente": int(len(source_dim)),
    }


def load_aggregates(conn: sqlite3.Connection, path: Path, max_rows: int | None = None) -> int:
    if not path.exists():
        return 0
    frame = pd.read_parquet(path)
    if max_rows is not None:
        frame = frame.head(max_rows)
    if frame.empty:
        return 0
    frame.to_sql("fact_aggregates", conn, if_exists="replace", index=False, chunksize=50_000)
    return int(len(frame))


def main() -> None:
    args = parse_args()
    db_path = Path(args.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")

    try:
        observations_rows = stream_parquet_to_sql(OBSERVATIONS_PATH, "fact_observaciones", conn, max_rows=args.max_rows)

        obs_preview = pd.read_parquet(OBSERVATIONS_PATH)
        if args.max_rows is not None:
            obs_preview = obs_preview.head(args.max_rows)
        dimension_counts = load_dimensions(conn, obs_preview)
        aggregate_rows = load_aggregates(conn, AGGREGATES_PATH, max_rows=args.max_rows)

        manifest = {
            "pipeline": "sql_load",
            "executed_at_utc": datetime.now(timezone.utc).isoformat(),
            "database_path": str(db_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "source_dataset": str(OBSERVATIONS_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "limit_applied": args.max_rows,
            "tables": {
                "fact_observaciones": observations_rows,
                "dim_segmento": dimension_counts["dim_segmento"],
                "dim_fuente": dimension_counts["dim_fuente"],
                "fact_aggregates": aggregate_rows,
            },
            "notes": [
                "La tabla fact_observaciones almacena las mediciones del dataset limpio.",
                "Las dimensiones son generadas a partir del propio dataset limpio para mantener trazabilidad y consulta eficiente.",
                "Se recomienda crear índices adicionales en timestamp, segmento_id y fuente después de la carga inicial.",
            ],
        }
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({"database": str(db_path.relative_to(PROJECT_ROOT)).replace("\\", "/"), "fact_rows": observations_rows, "manifest": str(MANIFEST_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/")}, ensure_ascii=False))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
