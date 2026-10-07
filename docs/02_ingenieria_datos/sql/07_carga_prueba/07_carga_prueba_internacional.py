from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow.parquet as parquet


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_ROOT = PROJECT_ROOT / "data"
CONTRACT_PATH = DATA_ROOT / "00_raw" / "external" / "international_sources_contract.json"
OBSERVATIONS_PATH = DATA_ROOT / "02_clean" / "consolidated" / "international_observations.parquet"
SQL_DIR = PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql"
DEFAULT_DB_PATH = SQL_DIR / "tsi_international_stage.sqlite"
DEFAULT_MANIFEST_PATH = SQL_DIR / "sql07_international_load_manifest.json"

FACT_COLUMNS = [
    "timestamp",
    "ciudad_id",
    "fuente_id",
    "segmento_id",
    "metrica_principal",
    "valor_principal",
    "velocidad_kmh",
    "flujo_veh_h",
    "ocupacion_pct",
    "densidad_veh_km",
    "tiempo_viaje_seg",
    "congestion_longitud_m",
    "indice_congestion",
    "intensidad_fuente",
    "carga_fuente",
    "vmed_fuente",
    "calidad_registro",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Carga una muestra internacional para SQL-07")
    parser.add_argument("--rows-per-source", type=int, default=1000)
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--manifest-path", default=str(DEFAULT_MANIFEST_PATH))
    return parser.parse_args()


def read_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def sample_by_source(rows_per_source: int) -> pd.DataFrame:
    parquet_file = parquet.ParquetFile(OBSERVATIONS_PATH)
    selected: list[pd.DataFrame] = []
    counts: dict[str, int] = {}

    for batch in parquet_file.iter_batches(batch_size=100_000):
        frame = batch.to_pandas()
        for source_id, source_frame in frame.groupby("fuente", sort=False):
            remaining = rows_per_source - counts.get(source_id, 0)
            if remaining <= 0:
                continue
            sample = source_frame.head(remaining)
            selected.append(sample)
            counts[source_id] = counts.get(source_id, 0) + len(sample)
        if counts and all(value >= rows_per_source for value in counts.values()) and len(counts) == 5:
            break

    if not selected:
        raise ValueError("No se encontraron observaciones en el consolidado internacional.")

    sample = pd.concat(selected, ignore_index=True)
    missing_sources = [source_id for source_id, count in counts.items() if count < rows_per_source]
    if missing_sources:
        raise ValueError(f"Fuentes con muestra incompleta: {missing_sources}")
    return sample


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE dim_ciudad (
            ciudad_id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            pais TEXT NOT NULL,
            region TEXT,
            zona_horaria TEXT NOT NULL,
            es_ciudad_objetivo INTEGER NOT NULL DEFAULT 0,
            UNIQUE (nombre, pais)
        );

        CREATE TABLE dim_fuente (
            fuente_id INTEGER PRIMARY KEY,
            ciudad_id INTEGER NOT NULL REFERENCES dim_ciudad(ciudad_id),
            nombre TEXT NOT NULL,
            tipo_fuente TEXT NOT NULL,
            origen_url TEXT,
            licencia TEXT,
            rol_dato TEXT NOT NULL,
            es_real INTEGER NOT NULL,
            frecuencia_documentada TEXT,
            UNIQUE (ciudad_id, nombre)
        );

        CREATE TABLE dim_segmento (
            segmento_id INTEGER PRIMARY KEY,
            ciudad_id INTEGER NOT NULL REFERENCES dim_ciudad(ciudad_id),
            fuente_id INTEGER NOT NULL REFERENCES dim_fuente(fuente_id),
            codigo_segmento TEXT NOT NULL,
            nombre_segmento TEXT,
            tipo_via TEXT NOT NULL,
            latitud REAL,
            longitud REAL,
            UNIQUE (fuente_id, codigo_segmento)
        );

        CREATE TABLE fact_observaciones (
            observacion_id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            ciudad_id INTEGER NOT NULL REFERENCES dim_ciudad(ciudad_id),
            fuente_id INTEGER NOT NULL REFERENCES dim_fuente(fuente_id),
            segmento_id INTEGER NOT NULL REFERENCES dim_segmento(segmento_id),
            metrica_principal TEXT NOT NULL,
            valor_principal REAL NOT NULL,
            velocidad_kmh REAL,
            flujo_veh_h REAL,
            ocupacion_pct REAL,
            densidad_veh_km REAL,
            tiempo_viaje_seg REAL,
            congestion_longitud_m REAL,
            indice_congestion REAL,
            intensidad_fuente REAL,
            carga_fuente REAL,
            vmed_fuente REAL,
            calidad_registro TEXT NOT NULL
        );

        CREATE TABLE calidad_observacion (
            calidad_id INTEGER PRIMARY KEY,
            observacion_id INTEGER NOT NULL REFERENCES fact_observaciones(observacion_id),
            tipo_problema TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            severidad TEXT NOT NULL,
            fecha_revision TEXT NOT NULL
        );

        CREATE TABLE fact_agregado (
            agregado_id INTEGER PRIMARY KEY,
            ciudad_id INTEGER NOT NULL REFERENCES dim_ciudad(ciudad_id),
            fuente_id INTEGER NOT NULL REFERENCES dim_fuente(fuente_id),
            segmento_id INTEGER REFERENCES dim_segmento(segmento_id),
            periodo_inicio TEXT NOT NULL,
            periodo_fin TEXT NOT NULL,
            metrica TEXT NOT NULL,
            valor_agregado REAL NOT NULL,
            cantidad_observaciones INTEGER NOT NULL
        );

        CREATE TABLE log_cargas (
            carga_id INTEGER PRIMARY KEY,
            fuente_id INTEGER REFERENCES dim_fuente(fuente_id),
            archivo_origen TEXT NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT,
            filas_leidas INTEGER NOT NULL DEFAULT 0,
            filas_insertadas INTEGER NOT NULL DEFAULT 0,
            filas_rechazadas INTEGER NOT NULL DEFAULT 0,
            estado TEXT NOT NULL,
            mensaje TEXT
        );

        CREATE INDEX ix_fact_timestamp ON fact_observaciones(timestamp);
        CREATE INDEX ix_fact_ciudad_timestamp ON fact_observaciones(ciudad_id, timestamp);
        CREATE INDEX ix_fact_fuente_timestamp ON fact_observaciones(fuente_id, timestamp);
        """
    )


def build_dimensions(conn: sqlite3.Connection, observations: pd.DataFrame, contract: dict) -> tuple[dict, dict, dict]:
    contract_by_source = {item["source_id"]: item for item in contract["sources"]}
    source_ids = sorted(observations["fuente"].unique())
    city_names = sorted(observations["ciudad"].unique())
    city_ids = {city: index for index, city in enumerate(city_names, start=1)}
    source_id_map = {source: index for index, source in enumerate(source_ids, start=1)}

    for city in city_names:
        source = next(item for item in contract["sources"] if item["city"] == city)
        conn.execute(
            "INSERT INTO dim_ciudad VALUES (?, ?, ?, ?, ?, ?)",
            (city_ids[city], city, source["country"], None, source["timezone"], int(city == "Guadalajara")),
        )

    for source_id in source_ids:
        source = contract_by_source[source_id]
        source_observations = observations.loc[observations["fuente"] == source_id]
        conn.execute(
            "INSERT INTO dim_fuente VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                source_id_map[source_id],
                city_ids[source["city"]],
                source_id,
                "fuente_internacional",
                source.get("source_url"),
                source.get("license"),
                source["role"],
                int(bool(source_observations["es_real"].iloc[0])),
                source.get("time_resolution"),
            ),
        )

    segment_frame = observations[["fuente", "ciudad", "segmento_id", "tipo_via", "latitud", "longitud"]].drop_duplicates(
        ["fuente", "segmento_id"]
    )
    segment_ids = {}
    for segment_id, row in enumerate(segment_frame.itertuples(index=False), start=1):
        segment_ids[(row.fuente, row.segmento_id)] = segment_id
        road_type = row.tipo_via if pd.notna(row.tipo_via) else "no_especificado"
        conn.execute(
            "INSERT INTO dim_segmento VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                segment_id,
                city_ids[row.ciudad],
                source_id_map[row.fuente],
                row.segmento_id,
                row.segmento_id,
                road_type,
                row.latitud,
                row.longitud,
            ),
        )

    return city_ids, source_id_map, segment_ids


def load_facts(conn: sqlite3.Connection, observations: pd.DataFrame, city_ids: dict, source_ids: dict, segment_ids: dict) -> None:
    rows = []
    for observation_id, row in enumerate(observations.itertuples(index=False), start=1):
        values = row._asdict()
        rows.append(
            (
                observation_id,
                pd.Timestamp(values["timestamp"]).isoformat(),
                city_ids[values["ciudad"]],
                source_ids[values["fuente"]],
                segment_ids[(values["fuente"], values["segmento_id"])],
                values["metrica_principal"],
                values["valor_principal"],
                values["velocidad_kmh"],
                values["flujo_veh_h"],
                values["ocupacion_pct"],
                values["densidad_veh_km"],
                values["tiempo_viaje_seg"],
                values["congestion_longitud_m"],
                values["indice_congestion"],
                values["intensidad_fuente"],
                values["carga_fuente"],
                values["vmed_fuente"],
                values["calidad_registro"],
            )
        )
    placeholders = ", ".join("?" for _ in range(18))
    conn.executemany(f"INSERT INTO fact_observaciones VALUES ({placeholders})", rows)


def validate(conn: sqlite3.Connection) -> dict:
    checks = {
        "fact_rows": conn.execute("SELECT COUNT(*) FROM fact_observaciones").fetchone()[0],
        "city_rows": conn.execute("SELECT COUNT(*) FROM dim_ciudad").fetchone()[0],
        "source_rows": conn.execute("SELECT COUNT(*) FROM dim_fuente").fetchone()[0],
        "segment_rows": conn.execute("SELECT COUNT(*) FROM dim_segmento").fetchone()[0],
        "foreign_key_violations": len(conn.execute("PRAGMA foreign_key_check").fetchall()),
        "required_nulls": conn.execute(
            """SELECT COUNT(*) FROM fact_observaciones
               WHERE timestamp IS NULL OR ciudad_id IS NULL OR fuente_id IS NULL
               OR segmento_id IS NULL OR metrica_principal IS NULL OR valor_principal IS NULL
               OR calidad_registro IS NULL"""
        ).fetchone()[0],
        "duplicate_observation_ids": conn.execute(
            "SELECT COUNT(*) - COUNT(DISTINCT observacion_id) FROM fact_observaciones"
        ).fetchone()[0],
    }
    checks["status"] = "passed" if all(value == 0 for key, value in checks.items() if key.endswith("violations") or key.endswith("nulls") or key.startswith("duplicate")) else "failed"
    return checks


def main() -> None:
    args = parse_args()
    if args.rows_per_source <= 0:
        raise ValueError("--rows-per-source debe ser mayor que cero")

    observations = sample_by_source(args.rows_per_source)
    contract = read_contract()
    db_path = Path(args.db_path)
    manifest_path = Path(args.manifest_path)
    db_path.unlink(missing_ok=True)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        create_schema(conn)
        city_ids, source_ids, segment_ids = build_dimensions(conn, observations, contract)
        load_facts(conn, observations, city_ids, source_ids, segment_ids)
        now = datetime.now(timezone.utc).isoformat()
        for source_id, source_db_id in source_ids.items():
            source_rows = int((observations["fuente"] == source_id).sum())
            conn.execute(
                "INSERT INTO log_cargas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (None, source_db_id, str(OBSERVATIONS_PATH.relative_to(PROJECT_ROOT)), now, now, source_rows, source_rows, 0, "completada", "SQL-07 carga de prueba"),
            )
        checks = validate(conn)
        conn.commit()
    finally:
        conn.close()

    manifest = {
        "pipeline": "sql07_international_load_test",
        "executed_at_utc": now,
        "source_dataset": str(OBSERVATIONS_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "database_path": str(db_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "rows_per_source": args.rows_per_source,
        "source_rows": observations.groupby("fuente").size().astype(int).to_dict(),
        "tables": {
            "dim_ciudad": checks["city_rows"],
            "dim_fuente": checks["source_rows"],
            "dim_segmento": checks["segment_rows"],
            "fact_observaciones": checks["fact_rows"],
            "log_cargas": len(source_ids),
        },
        "validation": checks,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()